"""Original bounded mean/variance/percentile-bootstrap teaching implementation."""
import itertools
import math
import random


def _sample(xs):
    xs = list(xs)
    if not xs or any(type(x) not in (int, float) or not math.isfinite(x) for x in xs):
        raise ValueError('nonempty finite numeric sample required')
    return xs


def mean(xs):
    xs = _sample(xs)
    return math.fsum(xs) / len(xs)


def variance(xs):
    xs = _sample(xs)
    if len(xs) < 2:
        raise ValueError('sample variance requires at least two observations')
    m = mean(xs)
    return math.fsum((x - m)**2 for x in xs) / (len(xs) - 1)


def empirical_quantile(xs, p):
    xs = sorted(_sample(xs))
    if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('quantile probability must be in [0,1]')
    # Left inverse of the finite empirical CDF; no linear interpolation.
    return xs[max(0, math.ceil(p * len(xs)) - 1)]


def bootstrap_means(xs, reps=2000, seed=1):
    xs = _sample(xs)
    if type(reps) is not int or not 2 <= reps <= 100_000:
        raise ValueError('bootstrap repetitions must be integer 2..100000')
    if len(xs) > 10_000:
        raise ValueError('sample exceeds the teaching limit')
    rng = random.Random(seed)
    n = len(xs)
    return [math.fsum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(reps)]


def bootstrap_mean_ci(xs, reps=2000, seed=1, alpha=.05):
    if type(alpha) not in (int, float) or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('alpha must lie strictly between 0 and 1')
    draws = bootstrap_means(xs, reps, seed)
    return empirical_quantile(draws, alpha / 2), empirical_quantile(draws, 1 - alpha / 2)


def exact_bootstrap_means(xs):
    """Enumerate all n**n ordered resamples, equally weighted, only for n<=6."""
    xs = _sample(xs)
    n = len(xs)
    if n > 6:
        raise ValueError('exact enumeration is bounded to six observations')
    return [math.fsum(row) / n for row in itertools.product(xs, repeat=n)]


def binomial_probabilities(n, p):
    if type(n) is not int or not 1 <= n <= 200 or type(p) not in (int, float) or not 0 <= p <= 1:
        raise ValueError('bounded n=1..200 and probability required')
    return [math.comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)]


def discrete_quantile(probabilities, p):
    if not 0 <= p <= 1:
        raise ValueError('probability required')
    total = 0.0
    for k, mass in enumerate(probabilities):
        total += mass
        if total >= p:
            return k
    return len(probabilities) - 1  # Floating CDF sum can fall a few ulps below 1.


def exact_bernoulli_percentile_coverage(n, p, alpha=.05):
    """Exact finite-sum coverage of the *ideal* percentile bootstrap at true p.

    Conditional on observed k, the empirical Bernoulli model has probability k/n.
    No Monte Carlo bootstrap approximation is involved in this calculation.
    """
    if type(alpha) not in (int, float) or not 0 < alpha < 1:
        raise ValueError('alpha must lie strictly between 0 and 1')
    population = binomial_probabilities(n, p)
    rows = []
    for k, mass in enumerate(population):
        conditional = binomial_probabilities(n, k / n)
        low = discrete_quantile(conditional, alpha / 2) / n
        high = discrete_quantile(conditional, 1 - alpha / 2) / n
        rows.append({'observed_successes': k, 'sample_probability': mass,
                     'interval': [low, high], 'covers_true_p': low <= p <= high})
    coverage = math.fsum(row['sample_probability'] for row in rows if row['covers_true_p'])
    return {'n': n, 'true_p': p, 'alpha': alpha, 'coverage': coverage,
            'zero_success_probability': population[0], 'cases': rows}
