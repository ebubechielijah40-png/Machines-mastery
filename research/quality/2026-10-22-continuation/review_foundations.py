"""Independent finite probes of the continuation's foundational mechanisms.

This file is a reviewer artifact, not a replacement curriculum test suite.
Run from any directory; JSON goes to stdout. It imports only local repository
models, retains deterministic seeds and compares alternative mathematical forms.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import random
import sys

ROOT = Path(__file__).resolve().parents[3]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def determinant(a):
    """Leibniz definition, deliberately unlike Gaussian elimination."""
    n = len(a)
    result = F()
    for permutation in itertools.permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i+1, n))
        term = F((-1)**inversions)
        for i, j in enumerate(permutation):
            term *= a[i][j]
        result += term
    return result


def run():
    linear_path = 'foundations/mathematics/core/linear.py'
    discrete_path = 'foundations/mathematics/core/discrete.py'
    probability_path = 'foundations/statistics/probability-inference/probability.py'
    linear = module('reviewed_linear', linear_path)
    discrete = module('reviewed_discrete', discrete_path)
    probability = module('reviewed_probability', probability_path)
    rng = random.Random(20261023)
    checks = []
    max_linear_error = max_scaled_error = 0.
    systems = 0
    while systems < 200:
        a = [[rng.randrange(-4, 5) for _ in range(3)] for _ in range(3)]
        b = [rng.randrange(-6, 7) for _ in range(3)]
        denominator = determinant(a)
        if not denominator:
            continue
        expected = []
        for col in range(3):
            replacement = [[b[i] if j == col else a[i][j] for j in range(3)] for i in range(3)]
            expected.append(determinant(replacement)/denominator)
        ordinary = linear.solve(a, b)
        factors = [1e-200, 1e100, 1e200]
        scaled = linear.solve([[v*factors[i] for v in row] for i, row in enumerate(a)],
                              [v*factors[i] for i, v in enumerate(b)])
        for actual, rescaled, oracle in zip(ordinary, scaled, expected):
            error = abs(actual-float(oracle))
            scaled_error = abs(rescaled-float(oracle))
            assert math.isclose(actual, float(oracle), rel_tol=1e-10, abs_tol=1e-10)
            assert math.isclose(rescaled, float(oracle), rel_tol=1e-10, abs_tol=1e-10)
            max_linear_error = max(max_linear_error, error)
            max_scaled_error = max(max_scaled_error, scaled_error)
        systems += 1
    checks.append({'name': '3x3 exact determinant/Cramer oracle', 'cases': systems,
                   'max_absolute_error': max_linear_error,
                   'max_row_scaled_absolute_error': max_scaled_error,
                   'row_scale_factors': factors})
    for _ in range(200):
        a = [[F(rng.randrange(-8, 9), 4) for _ in range(3)] for _ in range(4)]
        b = [F(rng.randrange(-8, 9), 4) for _ in range(4)]
        x = [F(rng.randrange(-8, 9), 4) for _ in range(3)]
        # Different form: differentiate the expanded quadratic Hx+c.
        h = [[sum(a[i][j]*a[i][k] for i in range(4)) for k in range(3)] for j in range(3)]
        c = [-sum(a[i][j]*b[i] for i in range(4)) for j in range(3)]
        oracle = [sum(h[j][k]*x[k] for k in range(3))+c[j] for j in range(3)]
        _, gradient = linear.quadratic_loss_gradient(
            [[float(v) for v in row] for row in a], list(map(float, b)), list(map(float, x)))
        assert gradient == list(map(float, oracle))  # dyadic inputs keep these small sums exact
    checks.append({'name': 'gradient versus exact expanded quadratic', 'cases': 200})
    assert linear.dot([1j, 1], [1j, 1]) == 2
    assert linear.matvec([[1j]], [1j]) == [-1]
    try:
        linear.solve([[1]], [1], rtol=.1+0j)
    except ValueError:
        pass
    else:
        raise AssertionError('complex tolerance must reject as ValueError')
    checks.append({'name': 'Hermitian dot versus ordinary matrix product and corrected rtol contract', 'status': 'PASS'})
    for _ in range(1000):
        a, b = rng.randrange(-10**12, 10**12), rng.randrange(-10**12, 10**12)
        gcd, s, t = discrete.extended_gcd(a, b)
        assert gcd == math.gcd(a, b) == s*a+t*b
        base, exponent, modulus = rng.randrange(-40, 41), rng.randrange(51), rng.randrange(1, 1001)
        assert discrete.modular_power(base, exponent, modulus) == pow(base, exponent, modulus)
    checks.append({'name': 'Bezout identity/library gcd and modular-power oracle', 'cases_each': 1000})
    for n in range(1001):
        for p in range(1, 41):
            pages = discrete.page_count(n, p)
            assert (pages == 0 if n == 0 else (pages-1)*p < n <= pages*p)
    checks.append({'name': 'page capacity and minimality inequalities', 'cases': 40040})
    for n in range(1, 1001):
        assert probability.wilson(0, n)[0] == 0
        assert probability.wilson(n, n)[1] == 1
    for n in [1, 2, 10, 13, 100]:
        assert probability.coverage(n, 0) == 1
        assert probability.coverage(n, 1) == 1
    checks.append({'name': 'corrected score-interval exact parameter endpoints',
                   'n_values': 1000, 'deterministic_coverage_cases': 10})
    max_endpoint_error = 0.
    with localcontext() as context:
        context.prec = 70
        for _ in range(200):
            n = rng.randrange(1, 10**6+1)
            k = rng.randrange(n+1)
            z = rng.choice([.1, .5, 1.959963984540054, 3., 10.])
            nd, kd, zd = Decimal(n), Decimal(k), Decimal.from_float(z)
            qa, qb, qc = nd+zd*zd, -(2*kd+zd*zd), kd*kd/nd
            discriminant = qb*qb-4*qa*qc
            oracle = [max(0., float((-qb-discriminant.sqrt())/(2*qa))),
                      min(1., float((-qb+discriminant.sqrt())/(2*qa)))]
            actual = probability.wilson(k, n, z)
            for endpoint, expected in zip(actual, oracle):
                error = abs(endpoint-expected)
                assert error < 2e-14
                max_endpoint_error = max(max_endpoint_error, error)
    checks.append({'name': 'score interval versus 70-digit quadratic roots',
                   'cases': 200, 'max_absolute_endpoint_error': max_endpoint_error})
    for _ in range(40):
        n = rng.randrange(2, 7)
        k = rng.randrange(1, n)
        data = [F(rng.randrange(-2, 3)) for _ in range(n)]
        observed = abs(sum(data[:k])/k-sum(data[k:])/(n-k))
        extreme = total = 0
        # Enumerate labeled permutations, unlike the implementation's combinations.
        for order in itertools.permutations(range(n)):
            statistic = abs(sum(data[i] for i in order[:k])/k-sum(data[i] for i in order[k:])/(n-k))
            extreme += statistic >= observed
            total += 1
        result = probability.permutation_test(data[:k], data[k:])
        assert result['p_value'] == F(extreme, total)
    checks.append({'name': 'permutation test versus all labeled permutations', 'cases': 40})
    return {'reviewer': 'independent research workstream', 'seed': 20261023,
            'python': sys.version, 'platform': platform.platform(), 'status': 'PASS',
            'reviewed_code_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                                    for p in [linear_path, discrete_path, probability_path]},
            'checks': checks,
            'limits': 'Finite probes are not universal stability/coverage proofs. Lesson review is separate. No unexecuted physical data or broad-domain completion is implied.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
