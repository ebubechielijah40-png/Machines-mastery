from collections import Counter
import math
import unittest
from stats_lab import (bootstrap_mean_ci, bootstrap_means, empirical_quantile,
                       exact_bernoulli_percentile_coverage, exact_bootstrap_means,
                       mean, variance)


class StatisticsTests(unittest.TestCase):
    def test_hand_mean_sample_variance_and_generator(self):
        self.assertEqual(mean(iter([1, 2, 3])), 2)
        self.assertEqual(variance([1, 2, 3]), 1)
        self.assertEqual(variance([0, 1]), .5)

    def test_exact_bootstrap_distribution_and_variance_oracle(self):
        draws = exact_bootstrap_means([0, 1])
        self.assertEqual(Counter(draws), Counter({0: 1, .5: 2, 1: 1}))
        self.assertEqual(mean(draws), .5)
        conditional_variance = sum((x - .5)**2 for x in draws) / 4
        self.assertEqual(conditional_variance, .125)
        self.assertEqual(conditional_variance, variance([0, 1]) * (2 - 1) / 2**2)

    def test_empirical_quantile_declared_inverse_cdf(self):
        self.assertEqual(empirical_quantile([0, .5, .5, 1], .25), 0)
        self.assertEqual(empirical_quantile([0, .5, .5, 1], .5), .5)
        self.assertEqual(empirical_quantile([0, .5, .5, 1], 0), 0)
        self.assertEqual(empirical_quantile([0, .5, .5, 1], 1), 1)

    def test_seeded_sampling_tracks_small_exact_distribution(self):
        first = bootstrap_means([0, 1], 10000, seed=7)
        self.assertEqual(first, bootstrap_means([0, 1], 10000, seed=7))
        counts = Counter(first)
        for value, probability in [(0, .25), (.5, .5), (1, .25)]:
            self.assertLess(abs(counts[value] / len(first) - probability), .02)

    def test_constant_sample_degeneracy_and_affine_equivariance(self):
        self.assertEqual(bootstrap_mean_ci([0]*5, 100, 2), (0, 0))
        x = [1, 2, 4, 8]
        low, high = bootstrap_mean_ci(x, 500, 9)
        changed = bootstrap_mean_ci([3*v+7 for v in x], 500, 9)
        self.assertEqual(changed, (3*low+7, 3*high+7))

    def test_exact_coverage_failure_has_independent_upper_bound(self):
        result = exact_bernoulli_percentile_coverage(5, .1)
        self.assertLessEqual(result['coverage'], 1-.9**5 + 1e-14)
        self.assertEqual(result['cases'][0]['interval'], [0, 0])
        self.assertFalse(result['cases'][0]['covers_true_p'])
        self.assertAlmostEqual(sum(row['sample_probability'] for row in result['cases']), 1)

    def test_boundary_validation(self):
        for xs in [[], [math.nan], [math.inf], [True], ['one']]:
            with self.assertRaises(ValueError): mean(xs)
        with self.assertRaises(ValueError): variance([1])
        for alpha in [0, 1, -.2, math.nan, True]:
            with self.assertRaises(ValueError): bootstrap_mean_ci([0, 1], alpha=alpha)
        for reps in [0, 1, 1.5, True, 100001]:
            with self.assertRaises(ValueError): bootstrap_mean_ci([0, 1], reps=reps)
        with self.assertRaises(ValueError): exact_bootstrap_means(range(7))


def run():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(StatisticsTests)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        raise SystemExit(1)


if __name__ == '__main__':
    run()
