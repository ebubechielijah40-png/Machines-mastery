"""Original finite bigram model and bounded one-dimensional Gaussian-mixture EM."""
from dataclasses import dataclass
import math
import random
from discriminative import number, vector, integer


def logsumexp(values):
    values = tuple(values)
    if not values or not all(math.isfinite(x) for x in values):
        raise ValueError('finite nonempty log scores required')
    m = max(values)
    return m + math.log(math.fsum(math.exp(x - m) for x in values))


@dataclass(frozen=True)
class GaussianMixture:
    weights: tuple
    means: tuple
    variances: tuple

    def __post_init__(self):
        w, m, v = vector(self.weights, 8), vector(self.means, 8), tuple(self.variances)
        if len(w) != len(m) or len(w) != len(v) or not 1 <= len(w) <= 8:
            raise ValueError('mixture shapes must agree')
        if any(x <= 0 for x in w) or not math.isclose(math.fsum(w), 1, abs_tol=1e-12, rel_tol=0):
            raise ValueError('positive weights must sum to one')
        clean = []
        for x in v:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                raise ValueError('positive finite variances required')
            try:
                x = float(x)
            except OverflowError:
                raise ValueError('variance not representable') from None
            if not math.isfinite(x) or not 1e-12 <= x <= 1e12:
                raise ValueError('variance outside bounded teaching domain')
            clean.append(x)
        object.__setattr__(self, 'weights', w)
        object.__setattr__(self, 'means', m)
        object.__setattr__(self, 'variances', tuple(clean))

    def log_scores(self, x):
        x = number(x)
        return tuple(math.log(w) - .5 * (math.log(2 * math.pi) + math.log(v) + (x - m) ** 2 / v)
                     for w, m, v in zip(self.weights, self.means, self.variances))

    def posterior(self, x):
        scores = self.log_scores(x)
        # max-shift normalization avoids cancellation in log-density subtraction
        # for a shared large negative offset.
        top = max(scores)
        raw = tuple(math.exp(s - top) for s in scores)
        total = math.fsum(raw)
        return tuple(s / total for s in raw)

    def nll(self, values):
        values = tuple(number(x) for x in values)
        if not 1 <= len(values) <= 4096:
            raise ValueError('nonempty bounded observations required')
        return -math.fsum(logsumexp(self.log_scores(x)) for x in values) / len(values)

    def em_step(self, values, variance_floor=1e-4):
        values = tuple(number(x) for x in values)
        if not 1 <= len(values) <= 4096:
            raise ValueError('nonempty bounded observations required')
        floor = number(variance_floor)
        if not 1e-12 <= floor <= 1e6 or any(v < floor for v in self.variances):
            raise ValueError('initial variance must respect the declared positive floor')
        responsibility = tuple(self.posterior(x) for x in values)
        mass = tuple(math.fsum(r[j] for r in responsibility) for j in range(len(self.weights)))
        if any(n == 0 for n in mass):
            raise ValueError('zero effective component mass; restart or simplify explicitly')
        means = tuple(math.fsum(r[j] * x for r, x in zip(responsibility, values)) / mass[j]
                      for j in range(len(mass)))
        variances = tuple(max(floor, math.fsum(r[j] * (x - means[j]) ** 2
                                              for r, x in zip(responsibility, values)) / mass[j])
                          for j in range(len(mass)))
        return GaussianMixture(tuple(n / len(values) for n in mass), means, variances)

    def sample(self, count, seed=0):
        count = integer(count, 0, 4096)
        rng, result = random.Random(seed), []
        for _ in range(count):
            target, component, total = rng.random(), len(self.weights) - 1, 0.0
            for j, w in enumerate(self.weights):
                total += w
                if target < total:
                    component = j
                    break
            # Original explicit Box-Muller transformation of two uniform draws.
            z = math.sqrt(-2 * math.log(1 - rng.random())) * math.cos(2 * math.pi * rng.random())
            result.append(number(self.means[component] + math.sqrt(self.variances[component]) * z))
        return tuple(result)


@dataclass(frozen=True)
class Bigram:
    alphabet: tuple
    counts: tuple
    alpha: float = 1.0

    def __post_init__(self):
        alphabet = tuple(self.alphabet)
        if not 1 <= len(alphabet) <= 64 or any(type(x) is not str or len(x) != 1 for x in alphabet) or len(set(alphabet)) != len(alphabet):
            raise ValueError('alphabet must contain distinct single characters')
        alpha = number(self.alpha)
        if not 0 < alpha <= 100:
            raise ValueError('positive bounded smoothing required')
        counts = tuple(tuple(row) for row in self.counts)
        n = len(alphabet) + 1
        if len(counts) != n or any(len(row) != n for row in counts) or any(type(x) is not int or not 0 <= x <= 10**8 for row in counts for x in row):
            raise ValueError('nonnegative square count table required')
        object.__setattr__(self, 'alphabet', alphabet)
        object.__setattr__(self, 'counts', counts)
        object.__setattr__(self, 'alpha', alpha)

    @classmethod
    def fit(cls, documents, alphabet, alpha=1.0):
        alphabet = tuple(alphabet)
        # Validate configuration without depending on malformed element hashing.
        if not 1 <= len(alphabet) <= 64 or any(type(x) is not str or len(x) != 1 for x in alphabet) or len(set(alphabet)) != len(alphabet):
            raise ValueError('distinct single character alphabet required')
        documents = tuple(documents)
        if not 1 <= len(documents) <= 4096:
            raise ValueError('nonempty bounded document collection required')
        index, n = {c: i for i, c in enumerate(alphabet)}, len(alphabet)
        counts = [[0] * (n + 1) for _ in range(n + 1)]
        for doc in documents:
            if type(doc) is not str or len(doc) > 512 or any(c not in index for c in doc):
                raise ValueError('bounded in-vocabulary text required')
            previous = n  # row n is BOS; column n is EOS, never an emitted character
            for c in doc:
                current = index[c]
                counts[previous][current] += 1
                previous = current
            counts[previous][n] += 1
        return cls(alphabet, tuple(tuple(r) for r in counts), alpha)

    def distribution(self, previous=None):
        if previous is None:
            row = self.counts[-1]
        else:
            if type(previous) is not str or previous not in self.alphabet:
                raise ValueError('previous state outside alphabet')
            row = self.counts[self.alphabet.index(previous)]
        den = sum(row) + self.alpha * len(row)
        return tuple((c + self.alpha) / den for c in row)

    def nll(self, documents):
        documents = tuple(documents)
        if not 1 <= len(documents) <= 4096:
            raise ValueError('nonempty bounded evaluation collection required')
        total, tokens = 0.0, 0
        for doc in documents:
            if type(doc) is not str or len(doc) > 512 or any(c not in self.alphabet for c in doc):
                raise ValueError('bounded in-vocabulary text required')
            previous = None
            for c in doc:
                total -= math.log(self.distribution(previous)[self.alphabet.index(c)])
                previous = c
                tokens += 1
            total -= math.log(self.distribution(previous)[-1])
            tokens += 1
        return total / tokens

    def sample(self, max_tokens=64, seed=0):
        integer(max_tokens, 0, 512)
        rng, previous, text = random.Random(seed), None, []
        for _ in range(max_tokens + 1):
            target, total = rng.random(), 0.0
            probabilities = self.distribution(previous)
            chosen = len(probabilities) - 1
            for j, q in enumerate(probabilities):
                total += q
                if target < total:
                    chosen = j
                    break
            if chosen == len(self.alphabet):
                return dict(text=''.join(text), terminated=True)
            if len(text) == max_tokens:
                break
            previous = self.alphabet[chosen]
            text.append(previous)
        return dict(text=''.join(text), terminated=False)
