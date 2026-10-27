import math,random,statistics,unittest
from count_release import Budget,count_bits,laplace_quantile,laplace_noise,log_density_ratio,clip_public

class PrivacyMechanismTests(unittest.TestCase):
    def test_count_sensitivity_exhaustive_neighbor_model(self):
        import itertools
        for n in range(6):
            for bits in itertools.product([0,1],repeat=n):
                for extra in [0,1]:self.assertLessEqual(abs(count_bits(bits)-count_bits(bits+(extra,))),1)
    def test_inverse_cdf_known_points_and_symmetry(self):
        self.assertAlmostEqual(laplace_quantile(.25,2),-2*math.log(2))
        self.assertAlmostEqual(laplace_quantile(.75,2),2*math.log(2))
        self.assertEqual(laplace_quantile(.5,2),0)
        for u in [.01,.1,.3,.49]:self.assertAlmostEqual(laplace_quantile(u,3),-laplace_quantile(1-u,3))
    def test_density_ratio_bound_and_wrong_scale_counterexample(self):
        for epsilon in [.1,.5,1,3]:
            scale=1/epsilon
            for z in range(-100,101):
                self.assertLessEqual(abs(log_density_ratio(z,10,11,scale)),epsilon+1e-12)
        self.assertGreater(log_density_ratio(-100,10,11,1),.5)
    def test_budget_exact_composition_and_failed_request_state(self):
        b=Budget(1_000_000)
        for _ in range(10):b.release([1,0,1],100_000,rng=random.Random(4))
        self.assertEqual((b.spent,b.remaining),(1_000_000,0))
        with self.assertRaises(ValueError):b.release([1],1)
        self.assertEqual(b.spent,1_000_000)
    def test_repeated_known_seed_is_not_a_private_release(self):
        a=Budget(1_000_000).release([1,1],500_000,rng=random.Random(5))
        b=Budget(1_000_000).release([1,1,1],500_000,rng=random.Random(5))
        self.assertEqual(b-a,1)
    def test_sampler_distribution_check_under_fixed_synthetic_rng(self):
        rng=random.Random(2026);samples=[laplace_noise(2,rng) for _ in range(30000)]
        self.assertLess(abs(statistics.mean(samples)),.06)
        self.assertLess(abs(statistics.pvariance(samples)-8),.35)
        self.assertLess(abs(statistics.mean(abs(x) for x in samples)-2),.04)
    def test_public_clipping_and_invalid_inputs(self):
        self.assertEqual([clip_public(x,0,100) for x in [-10,10,110]],[0,10,100])
        for u,scale in [(0,1),(1,1),(.5,0),(math.nan,1),(.01,1e308)]:
            with self.assertRaises(ValueError):laplace_quantile(u,scale)
        for bits in [[2],[.5],['1']]:
            with self.assertRaises(ValueError):count_bits(bits)
        for amount in [True,0,-1]:
            with self.assertRaises(ValueError):Budget(amount)
    def test_bad_random_source_spends_reserved_budget_without_output(self):
        class EndpointRNG:
            def random(self):return 0
        b=Budget(1_000_000)
        with self.assertRaises(ValueError):b.release([1],100_000,rng=EndpointRNG())
        self.assertEqual(b.spent,100_000)

if __name__=='__main__':unittest.main(verbosity=2)
