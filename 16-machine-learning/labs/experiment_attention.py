"""Deterministic mechanism experiment; not a translation/model reproduction.

Run from repository root. Prints JSON; measured timing varies by machine.
"""
import json
import math
import platform
import random
import sys
import time
from attention import CausalCache, attention_backward, causal_attention, identity, scaled_dot_attention, softmax


def max_difference(left, right):
    return max(abs(a-b) for x, y in zip(left, right) for a, b in zip(x, y))


def run():
    rng = random.Random(2718)
    tokens = [[rng.uniform(-1,1) for _ in range(4)] for _ in range(32)]
    matrices = [identity(4)]*3
    start = time.perf_counter()
    full, _ = causal_attention(tokens, *matrices)
    full_seconds = time.perf_counter() - start
    cache = CausalCache(*matrices)
    cached = [cache.step(token)[0] for token in tokens]
    changed = [x[:] for x in tokens]
    changed[-1] = [99., -99., 50., -50.]
    mutation, _ = causal_attention(changed, *matrices)
    width_cases = []
    for width in (1, 4, 16, 64):
        q = [1.]*width
        keys = [[1.]*width, [0.]*width]
        _, scaled = scaled_dot_attention(q, keys, [[1.], [0.]])
        _, unscaled = scaled_dot_attention(q, keys, [[1.], [0.]], scale=False)
        width_cases.append({'width':width,'scaled_first_weight':scaled[0], 'unscaled_first_weight':unscaled[0]})
    q, keys, values, g = [0.3,-0.7], [[0.2,0.8],[-0.5,0.4]], [[0.4,1.2],[-0.3,0.6]], [0.6,-0.4]
    dq, _, _ = attention_backward(q, keys, values, g)
    errors = []
    for j in range(2):
        old = q[j]
        def loss(delta):
            q[j] = old+delta
            result, _ = scaled_dot_attention(q, keys, values)
            return sum(a*b for a,b in zip(result,g))
        observed = (loss(1e-6)-loss(-1e-6))/(2e-6)
        q[j] = old
        errors.append(abs(dq[j]-observed))
    n = len(tokens)
    return {'environment':{'python':sys.version, 'platform':platform.platform()},'seed':2718,
        'sequence_length':n,'head_width':4,'full_causal_seconds':full_seconds,
        'cache_vs_full_max_absolute_error':max_difference(full,cached),
        'future_mutation_prefix_max_absolute_error':max_difference(full[:-1],mutation[:-1]),
        'query_gradient_max_central_difference_error':max(errors),
        'wrong_post_softmax_mask_row_sum':sum(softmax([0.,0.,20.])[:2]),
        'width_concentration':width_cases,
        'derived_operation_counts':{'cached_generation_score_pairs':n*(n+1)//2,
          'recompute_all_prefix_outputs_score_pairs':n*(n+1)*(n+2)//6,
          'cached_projection_vectors':3*n,'recompute_all_prefixes_projection_vectors':3*n*(n+1)//2},
        'scope':'single head mechanism; no model trained; no paper benchmark reproduced'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, allow_nan=False))
