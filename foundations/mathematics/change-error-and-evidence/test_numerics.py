import math
from fractions import Fraction
import unittest
from numerics import difference, summarize, speed_uncertainty


class NumericalTests(unittest.TestCase):
    def test_polynomials_with_independent_exact_derivative(self):
        for x in [-3.0, 0.0, 2.0, 10.0]:
            with self.subTest(x=x):
                self.assertAlmostEqual(difference(lambda t: t*t, x, 0.125), 2*x)
                self.assertAlmostEqual(difference(lambda t: t*t, x, 0.125, 'forward'), 2*x+0.125)

    def test_linear_and_constant_units(self):
        self.assertAlmostEqual(difference(lambda t: 3*t+2, 1.5, 0.25), 3)
        self.assertEqual(difference(lambda t: 5, 1.5, 0.25), 0)

    def test_small_step_is_rejected_not_false_zero(self):
        with self.assertRaisesRegex(ValueError, 'distinguishable'):
            difference(lambda x: x*x, 1.0, 1e-20)

    def test_bad_steps_domains_methods_and_nonfinite_evaluation(self):
        for args in [(1,0,'central'), (1,-1,'central'), (math.inf,1,'forward'), (1,math.nan,'central'),(1,1,'other')]:
            with self.assertRaises(ValueError): difference(lambda x:x, *args)
        with self.assertRaises(ValueError): difference(lambda x: math.nan, 1, .1)
        with self.assertRaises(ValueError): difference(lambda x: x, 1e308, 1e308)

    def test_absolute_value_counterexample_is_a_valid_numeric_output(self):
        # Central differences alone cannot diagnose differentiability.
        self.assertEqual(difference(abs, 0, .125), 0)
        self.assertEqual(difference(abs, 0, .125, 'forward'), 1)

    def test_variance_exact_fraction_oracle_with_large_offset(self):
        integers = [10**9+i for i in [1,2,3,4]]
        mean = sum(map(Fraction, integers))/len(integers)
        var = sum((Fraction(x)-mean)**2 for x in integers)/(len(integers)-1)
        got = summarize(iter(integers))
        self.assertEqual(got.mean, float(mean))
        self.assertAlmostEqual(got.sample_variance, float(var), places=14)
        self.assertAlmostEqual(got.sem, math.sqrt(float(var)/4))

    def test_variance_translation_and_scaling(self):
        data = [1.,3.,7.,9.]
        a,b = summarize(data),summarize([2*x+100 for x in data])
        self.assertAlmostEqual(b.mean, 2*a.mean+100)
        self.assertAlmostEqual(b.sample_variance, 4*a.sample_variance)
        self.assertAlmostEqual(b.sem, 2*a.sem)

    def test_constant_and_invalid_samples(self):
        self.assertEqual(summarize([2,2]).sem, 0)
        for data in [[], [1], [1,math.nan], [math.inf,1]]:
            with self.assertRaises(ValueError): summarize(data)

    def test_hand_calculated_uncertainty_and_covariance(self):
        v,u = speed_uncertainty(10,2,.1,.02)
        self.assertEqual(v,5)
        self.assertAlmostEqual(u,math.sqrt(.005))
        self.assertEqual(speed_uncertainty(10,2,.1,.02,1)[1], 0)
        self.assertAlmostEqual(speed_uncertainty(10,2,.1,.02,-1)[1], .1)

    def test_uncertainty_units_transform(self):
        # Expressing distance in cm makes both numeric output components 100x.
        v,u = speed_uncertainty(10,2,.1,.02)
        a,b = speed_uncertainty(1000,2,10,.02)
        self.assertAlmostEqual(a,100*v)
        self.assertAlmostEqual(b,100*u)
        for args in [(10,0,.1,.02,0), (10,2,-.1,.02,0), (10,2,.1,.02,2)]:
            with self.assertRaises(ValueError): speed_uncertainty(*args)

    def test_uncertainty_representable_at_extreme_input_scales(self):
        for scale in [1e-200, 1e200]:
            v,u = speed_uncertainty(scale, scale, 0, scale/100)
            self.assertEqual(v, 1)
            self.assertAlmostEqual(u, .01)
        self.assertTrue(math.isclose(speed_uncertainty(1e160,1e160,0,.01)[1],1e-162))


if __name__ == '__main__': unittest.main()
