"""Inspectable scalar-list attention, local derivatives and incremental decoding.

Pure Python; no training, fused kernels, batching, padding or production guarantees.
Weights use row vectors: (d_input, d_projection). Causality is exclusion before
normalization. Non-finite inputs/intermediates raise ValueError.
"""
from math import exp, fsum, isfinite, sqrt


def _vector(values, label):
    if not values or any(not isinstance(x, (int, float)) or not isfinite(x) for x in values):
        raise ValueError(label + ' must be nonempty finite numbers')


def _matrix(rows, label):
    if not rows:
        raise ValueError(label + ' must be nonempty')
    for row in rows:
        _vector(row, label)
    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError(label + ' must be rectangular')


def _sum(values):
    try:
        result = fsum(values)
    except (OverflowError, ValueError) as exc:
        raise ValueError('non-finite intermediate') from exc
    if not isfinite(result):
        raise ValueError('non-finite intermediate')
    return result


def matvec(vector, weights):
    """vector length d_in, weights shape (d_in, d_out)."""
    _vector(vector, 'vector')
    _matrix(weights, 'weights')
    if len(weights) != len(vector):
        raise ValueError('incompatible dimensions')
    return [_sum(v * weights[i][j] for i, v in enumerate(vector))
            for j in range(len(weights[0]))]


def softmax(scores):
    """Finite-score stable softmax; an empty/all-masked row is an error."""
    _vector(scores, 'scores')
    maximum = max(scores)
    weights = [exp(x - maximum) for x in scores]
    total = fsum(weights)
    return [x / total for x in weights]


def scaled_dot_attention(query, keys, values, scale=True):
    """One query over already permitted keys; return (output, weights).

    Masking belongs to the caller's selection of keys/values. This avoids
    pretending that post-softmax zeroing enforces a normalized causal mask.
    """
    _vector(query, 'query')
    _matrix(keys, 'keys')
    _matrix(values, 'values')
    if len(keys) != len(values) or len(query) != len(keys[0]):
        raise ValueError('query/key/value dimensions do not match')
    divisor = sqrt(len(query)) if scale else 1.0
    scores = [_sum(a * b for a, b in zip(query, key)) / divisor for key in keys]
    weights = softmax(scores)
    output = [_sum(weight * row[j] for weight, row in zip(weights, values))
              for j in range(len(values[0]))]
    return output, weights


def attention_backward(query, keys, values, output_gradient, scale=True):
    """VJP dL/d(q,K,V), holding permitted-key selection fixed.

    output_gradient is dL/do. This differentiates the isolated operation, not
    the projection matrices or a whole Transformer. See DERIVATION.md.
    """
    _, weights = scaled_dot_attention(query, keys, values, scale)
    _vector(output_gradient, 'output gradient')
    if len(output_gradient) != len(values[0]):
        raise ValueError('output gradient width mismatch')
    dweights = [_sum(g * v for g, v in zip(output_gradient, row)) for row in values]
    weighted_mean = _sum(a * da for a, da in zip(weights, dweights))
    dscores = [a * (da - weighted_mean) for a, da in zip(weights, dweights)]
    divisor = sqrt(len(query)) if scale else 1.0
    dquery = [_sum(ds * key[j] for ds, key in zip(dscores, keys)) / divisor
              for j in range(len(query))]
    dkeys = [[ds * q / divisor for q in query] for ds in dscores]
    dvalues = [[a * g for g in output_gradient] for a in weights]
    for vector in [dquery, *dkeys, *dvalues]:
        _vector(vector, 'gradient')
    return dquery, dkeys, dvalues


def causal_attention(tokens, w_q, w_k, w_v, scale=True):
    """Return (outputs, n-by-n weights) for a single causal attention head."""
    _matrix(tokens, 'tokens')
    q = [matvec(x, w_q) for x in tokens]
    k = [matvec(x, w_k) for x in tokens]
    v = [matvec(x, w_v) for x in tokens]
    result, matrix = [], []
    for i, query in enumerate(q):
        out, visible = scaled_dot_attention(query, k[:i + 1], v[:i + 1], scale)
        result.append(out)
        matrix.append(visible + [0.0] * (len(tokens) - i - 1))
    return result, matrix


class CausalCache:
    """One head, one sequence, fixed projections; only projected K/V retained.

    Own one instance per sequence and clear it before unrelated inputs. Cache
    memory grows with context. This class has no concurrency or capacity policy.
    """
    def __init__(self, w_q, w_k, w_v, scale=True):
        for name, weights in [('queries', w_q), ('keys', w_k), ('values', w_v)]:
            _matrix(weights, name)
        if len({len(w_q), len(w_k), len(w_v)}) != 1 or len(w_q[0]) != len(w_k[0]):
            raise ValueError('projection dimensions do not match')
        self.w_q = [list(row) for row in w_q]
        self.w_k = [list(row) for row in w_k]
        self.w_v = [list(row) for row in w_v]
        self.scale = scale
        self.keys, self.values = [], []

    def clear(self):
        self.keys.clear()
        self.values.clear()

    def step(self, token):
        query = matvec(token, self.w_q)
        key = matvec(token, self.w_k)
        value = matvec(token, self.w_v)
        # Validate the operation before committing state, including overflow.
        out, weights = scaled_dot_attention(query, self.keys + [key], self.values + [value], self.scale)
        self.keys.append(key)
        self.values.append(value)
        return out, weights


def identity(n):
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError('n must be a positive integer')
    return [[float(i == j) for j in range(n)] for i in range(n)]


if __name__ == '__main__':
    tokens = [[1., 0.], [0., 1.], [1., 1.]]
    values, weights = causal_attention(tokens, identity(2), identity(2), identity(2))
    print('outputs:', values)
    print('attention weights:', weights)
