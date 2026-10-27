"""Original, bounded binary models with explicit analytic reverse derivatives.

No numerical/ML dependency. Parameters are immutable tuples; an update is returned
only after every proposed value is checked. These are teaching mechanisms, not
untrusted-input services or optimized training kernels.
"""
from dataclasses import dataclass
import math


def number(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError('expected a real numeric scalar, not bool')
    try:
        x = float(x)
    except (OverflowError, ValueError):
        raise ValueError('scalar is not representable') from None
    if not math.isfinite(x) or abs(x) > 1e6:
        raise ValueError('finite teaching scalars must have magnitude <= 1e6')
    return x


def vector(xs, maximum=256):
    values = tuple(number(x) for x in xs)
    if not 1 <= len(values) <= maximum:
        raise ValueError('vector length outside teaching bounds')
    return values


def integer(x, lo, hi):
    if type(x) is not int or not lo <= x <= hi:
        raise ValueError('integer outside teaching bounds')
    return x


def sigmoid(z):
    z = number(z)
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    a = math.exp(z)
    return a / (1 + a)


def binary_loss(z, y):
    z = number(z)
    if type(y) is not int or y not in (0, 1):
        raise ValueError('binary label must be integer 0 or 1')
    # Avoid raw exp(z), log(sigmoid(z)) and catastrophic inf-inf arithmetic.
    return max(z, 0) - y * z + math.log1p(math.exp(-abs(z)))


def parameters(values, count):
    values = vector(values)
    if len(values) != count:
        raise ValueError('wrong parameter count')
    return values


@dataclass(frozen=True)
class Standardizer:
    means: tuple
    scales: tuple

    def __post_init__(self):
        means, scales = vector(self.means, 64), vector(self.scales, 64)
        if len(means) != len(scales) or any(x <= 0 for x in scales):
            raise ValueError('scale must be positive and shapes must match')
        object.__setattr__(self, 'means', means)
        object.__setattr__(self, 'scales', scales)

    @classmethod
    def fit(cls, training_rows):
        rows = tuple(vector(x, 64) for x in training_rows)
        if not 1 <= len(rows) <= 4096 or any(len(x) != len(rows[0]) for x in rows):
            raise ValueError('nonempty rectangular training batch required')
        means = tuple(math.fsum(x[j] for x in rows) / len(rows) for j in range(len(rows[0])))
        scales = tuple(math.sqrt(math.fsum((x[j] - means[j]) ** 2 for x in rows) / len(rows)) or 1.0
                       for j in range(len(means)))
        return cls(means, scales)

    def transform(self, row):
        row = vector(row, 64)
        if len(row) != len(self.means):
            raise ValueError('wrong feature shape')
        return tuple(number((x - m) / s) for x, m, s in zip(row, self.means, self.scales))


@dataclass(frozen=True)
class Logistic:
    dimension: int
    l2: float = 0.0

    def __post_init__(self):
        integer(self.dimension, 1, 64)
        coefficient = number(self.l2)
        if coefficient < 0:
            raise ValueError('nonnegative L2 coefficient required')
        object.__setattr__(self, 'l2', coefficient)

    @property
    def parameter_count(self):
        return self.dimension + 1

    def logit(self, p, x):
        p, x = parameters(p, self.parameter_count), vector(x, 64)
        if len(x) != self.dimension:
            raise ValueError('wrong feature shape')
        return number(math.fsum(w * a for w, a in zip(p[:-1], x)) + p[-1])

    def loss_grad(self, p, x, y):
        x = vector(x, 64)
        z = self.logit(p, x)
        loss, d = binary_loss(z, y), sigmoid(z) - y
        p = parameters(p, self.parameter_count)
        loss += .5 * self.l2 * math.fsum(w * w for w in p[:-1])
        return loss, tuple(d * a + self.l2 * w for a, w in zip(x, p[:-1])) + (d,)


@dataclass(frozen=True)
class CircularCNN:
    """1D circular cross-correlation -> tanh -> global mean -> binary logit."""
    filters: int = 2
    kernel_size: int = 3
    pooling: str = 'mean'

    def __post_init__(self):
        integer(self.filters, 1, 8)
        integer(self.kernel_size, 1, 16)
        if self.pooling not in ('mean', 'max'):
            raise ValueError('pooling must be mean or max')

    @property
    def parameter_count(self):
        return self.filters * (self.kernel_size + 2) + 1

    def features(self, p, x):
        p, x = parameters(p, self.parameter_count), vector(x)
        if len(x) < self.kernel_size:
            raise ValueError('ring must contain at least one kernel width')
        width = self.kernel_size + 1
        return tuple(tuple(math.tanh(math.fsum(p[f * width + j] * x[(i + j) % len(x)]
                                                  for j in range(self.kernel_size)) + p[f * width + self.kernel_size])
                           for i in range(len(x))) for f in range(self.filters))

    def logit(self, p, x):
        p = parameters(p, self.parameter_count)
        features = self.features(p, x)
        offset = self.filters * (self.kernel_size + 1)
        return number(p[-1] + math.fsum(p[offset + f] * (math.fsum(row) / len(row) if self.pooling == 'mean' else max(row))
                                       for f, row in enumerate(features)))

    def loss_grad(self, p, x, y):
        p, x = parameters(p, self.parameter_count), vector(x)
        features = self.features(p, x)
        width, n = self.kernel_size + 1, len(x)
        offset = self.filters * width
        z = number(p[-1] + math.fsum(p[offset + f] * (math.fsum(row) / n if self.pooling == 'mean' else max(row))
                                    for f, row in enumerate(features)))
        loss, d = binary_loss(z, y), sigmoid(z) - y
        grads = [0.0] * len(p)
        grads[-1] = d
        for f, row in enumerate(features):
            pooled = math.fsum(row) / n if self.pooling == 'mean' else max(row)
            grads[offset + f] = d * pooled
            winner = row.index(pooled) if self.pooling == 'max' else None
            for i, h in enumerate(row):
                share = 1 / n if self.pooling == 'mean' else float(i == winner)
                delta = d * p[offset + f] * (1 - h * h) * share
                grads[f * width + self.kernel_size] += delta
                for j in range(self.kernel_size):
                    grads[f * width + j] += delta * x[(i + j) % n]
        return loss, tuple(grads)


@dataclass(frozen=True)
class ScalarRNN:
    """Five parameters: input, recurrent, hidden bias, output, output bias."""
    parameter_count: int = 5

    def __post_init__(self):
        if type(self.parameter_count) is not int or self.parameter_count != 5:
            raise ValueError('this scalar recurrence has exactly five parameters')

    def states(self, p, x):
        p, x = parameters(p, 5), vector(x)
        h, result = 0.0, []
        for a in x:
            h = math.tanh(p[0] * a + p[1] * h + p[2])
            result.append(h)
        return tuple(result)

    def logit(self, p, x):
        p = parameters(p, 5)
        return number(p[3] * self.states(p, x)[-1] + p[4])

    def gradients(self, p, x, y):
        p, x = parameters(p, 5), vector(x)
        h = self.states(p, x)
        z = number(p[3] * h[-1] + p[4])
        loss, d = binary_loss(z, y), sigmoid(z) - y
        grads = [0.0, 0.0, 0.0, d * h[-1], d]
        dx, dh = [0.0] * len(x), d * p[3]
        for i in reversed(range(len(x))):
            a = dh * (1 - h[i] * h[i])
            grads[0] += a * x[i]
            grads[1] += a * (h[i - 1] if i else 0.0)
            grads[2] += a
            dx[i] = a * p[0]
            dh = a * p[1] if i else 0.0
            if not all(math.isfinite(v) for v in (*grads, dx[i], dh)):
                raise ValueError('nonfinite recurrent adjoint; shorten or rescale the declared model')
        return loss, tuple(grads), tuple(dx)

    def loss_grad(self, p, x, y):
        loss, grads, _ = self.gradients(p, x, y)
        return loss, grads


def batch_step(model, p, examples, rate, clip=None):
    """Mean gradient; optional whole-vector clipping; all-or-nothing returned update."""
    p = parameters(p, model.parameter_count)
    rate = number(rate)
    if rate <= 0:
        raise ValueError('positive step required')
    if clip is not None:
        clip = number(clip)
        if clip <= 0:
            raise ValueError('positive norm bound required')
    examples = tuple(examples)
    if not 1 <= len(examples) <= 4096:
        raise ValueError('nonempty bounded batch required')
    results = [model.loss_grad(p, x, y) for x, y in examples]
    loss = math.fsum(row[0] for row in results) / len(results)
    grad = tuple(math.fsum(row[1][j] for row in results) / len(results) for j in range(len(p)))
    norm = math.hypot(*grad)
    if not math.isfinite(norm):
        raise ValueError('nonfinite gradient norm')
    scale = min(1.0, clip / norm) if clip is not None and norm else 1.0
    updated = tuple(number(w - rate * scale * g) for w, g in zip(p, grad))
    return updated, dict(loss=loss, gradient_norm=norm, clipping_scale=scale)


def metrics(model, p, examples):
    examples = tuple(examples)
    if not 1 <= len(examples) <= 4096:
        raise ValueError('nonempty bounded evaluation required')
    losses = [binary_loss(model.logit(p, x), y) for x, y in examples]
    probabilities = [sigmoid(model.logit(p, x)) for x, _ in examples]
    return dict(count=len(examples), nll=math.fsum(losses) / len(examples),
                accuracy=sum(int(q >= .5) == y for q, (_, y) in zip(probabilities, examples)) / len(examples),
                brier=math.fsum((q - y) ** 2 for q, (_, y) in zip(probabilities, examples)) / len(examples))


def correlate2d(image, kernel, padding=0, stride=1):
    """Literal zero-padded 2D cross-correlation, one input/output channel."""
    integer(padding, 0, 16)
    integer(stride, 1, 16)
    image, kernel = tuple(vector(row, 32) for row in image), tuple(vector(row, 32) for row in kernel)
    if not 1 <= len(image) <= 32 or not 1 <= len(kernel) <= 32:
        raise ValueError('bounded nonempty matrices required')
    if any(len(row) != len(image[0]) for row in image) or any(len(row) != len(kernel[0]) for row in kernel):
        raise ValueError('rectangular matrices required')
    height, width = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    oh, ow = (height + 2 * padding - kh) // stride + 1, (width + 2 * padding - kw) // stride + 1
    if oh < 1 or ow < 1:
        raise ValueError('kernel does not fit padded input')
    def pixel(i, j):
        return image[i][j] if 0 <= i < height and 0 <= j < width else 0.0
    return tuple(tuple(number(math.fsum(kernel[u][v] * pixel(i * stride + u - padding, j * stride + v - padding)
                                       for u in range(kh) for v in range(kw)))
                       for j in range(ow)) for i in range(oh))
