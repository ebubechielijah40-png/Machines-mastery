import math
import random
import unittest
from fractions import Fraction
from materials import (BondLaw, Bar, fit_extension, infer_modulus, infer_two_lengths,
                       parallel_compliance, series_compliance, relative_standard_uncertainty)


class MaterialTests(unittest.TestCase):
    def test_equilibrium_depth_curvature(self):
        for m in range(2, 21):
            b = BondLaw(1e-19, 2e-10, m)
            self.assertAlmostEqual(b.energy_J(b.spacing_m)/b.depth_J, -1)
            self.assertEqual(b.required_force_N(b.spacing_m), 0)
            self.assertAlmostEqual(b.tangent_N_per_m(b.spacing_m)/b.stiffness_N_per_m, 1)
            for ratio in (.9, .99, 1.01, 1.1):
                self.assertGreater(b.energy_J(b.spacing_m*ratio), -b.depth_J)

    def test_derivatives_independent_central_differences(self):
        b = BondLaw(1e-19, 2e-10, 8)
        h = b.spacing_m*1e-5
        for ratio in (.8, .95, 1.05, 1.3, 2):
            r = ratio*b.spacing_m
            f = (b.energy_J(r+h) - b.energy_J(r-h))/(2*h)
            k = (b.required_force_N(r+h) - b.required_force_N(r-h))/(2*h)
            self.assertTrue(math.isclose(f, b.required_force_N(r), rel_tol=2e-8))
            self.assertTrue(math.isclose(k, b.tangent_N_per_m(r), rel_tol=2e-8))

    def test_force_peak_and_control_stability(self):
        for m in (2, 5, 8, 20):
            b = BondLaw(2e-19, 3e-10, m); r = b.force_peak_separation_m()
            self.assertGreater(b.tangent_N_per_m(r*.999), 0)
            self.assertLess(b.tangent_N_per_m(r*1.001), 0)
            peak = b.required_force_N(r)
            self.assertLess(b.required_force_N(r*.999), peak)
            self.assertLess(b.required_force_N(r*1.001), peak)

    def test_bar_work_and_scaling(self):
        b = Bar(.1, 1e-6, 200e9)
        response = b.response(50)
        self.assertAlmostEqual(response['extension_m'], 25e-6)
        self.assertAlmostEqual(response['stress_Pa'], 50e6)
        self.assertAlmostEqual(response['strain'], .00025)
        self.assertAlmostEqual(response['stored_energy_J'], .000625)
        for factor in (2, 3, 10):
            self.assertAlmostEqual(Bar(.1*factor, 1e-6, 200e9).response(50)['extension_m'], factor*25e-6)
            self.assertAlmostEqual(Bar(.1, 1e-6*factor, 200e9).response(50)['extension_m'], 25e-6/factor)
        self.assertEqual(b.response(0)['stored_energy_J'], 0)
        self.assertGreater(b.response(-50)['stored_energy_J'], 0)
        with self.assertRaises(ValueError): b.response(3000)

    def test_series_parallel_against_fraction_oracle(self):
        rng = random.Random(842)
        for _ in range(100):
            c = [Fraction(rng.randrange(1, 20), rng.randrange(1, 20)) for _ in range(rng.randrange(1, 8))]
            self.assertAlmostEqual(series_compliance([float(x) for x in c]), float(sum(c)))
            self.assertAlmostEqual(parallel_compliance([float(x) for x in c]), float(1/sum(1/x for x in c)))

    def test_fit_intercept_and_orthogonality(self):
        x = [0, 10, 20, 30, 40, 50]
        y = [2e-6 + 6e-7*f for f in x]
        fit = fit_extension(iter(x), iter(y))
        self.assertAlmostEqual(fit.slope_m_per_N, 6e-7)
        self.assertAlmostEqual(fit.intercept_m, 2e-6)
        self.assertAlmostEqual(sum(fit.residuals_m), 0)
        self.assertAlmostEqual(sum(a*b for a, b in zip(x, fit.residuals_m)), 0)
        self.assertLess(fit.slope_standard_uncertainty_m_per_N, 1e-20)

    def test_fit_small_exact_rational_oracle(self):
        rng = random.Random(511)
        for _ in range(100):
            x = list(range(rng.randrange(3, 12)))
            y = [Fraction(rng.randrange(-20, 21), 7) for _ in x]
            mean_x, mean_y = Fraction(sum(x),len(x)), sum(y)/len(y)
            slope = sum((a-mean_x)*(b-mean_y) for a,b in zip(x,y))/sum((a-mean_x)**2 for a in x)
            fit = fit_extension(x, [float(v) for v in y])
            self.assertAlmostEqual(fit.slope_m_per_N, float(slope), places=12)
            self.assertAlmostEqual(fit.intercept_m, float(mean_y-slope*mean_x), places=12)

    def test_identification_and_frame_bias(self):
        area, e, frame = 1e-6, 200e9, 1e-7
        s1, s2 = .1/area/e + frame, .2/area/e + frame
        self.assertAlmostEqual(infer_modulus(.1, area, s1)/e, 5/6)
        self.assertAlmostEqual(infer_modulus(.1, area, s1, frame)/e, 1)
        fit = infer_two_lengths(.1, s1, .2, s2, area)
        self.assertAlmostEqual(fit['modulus_Pa']/e, 1)
        self.assertAlmostEqual(fit['frame_compliance_m_per_N']/frame, 1)
        alternate_e, alternate_frame = 250e9, 2e-7
        self.assertAlmostEqual(.1/area/alternate_e+alternate_frame, s1)

    def test_uncertainty_assumptions_and_diagnostic_negative_frame(self):
        self.assertAlmostEqual(relative_standard_uncertainty(1,.01,2,.04,4,.12), math.sqrt(.0014))
        self.assertLess(infer_two_lengths(.1,1e-7,.2,3e-7,1e-6)['frame_compliance_m_per_N'],0)

    def test_invalid_inputs(self):
        for value in (True, None, '1', float('nan'), float('inf'), 10**1000):
            with self.assertRaises(ValueError): BondLaw(value,1)
            with self.assertRaises(ValueError): Bar(1,value,1)
            with self.assertRaises(ValueError): fit_extension([0,1,2],[0,1,value])
        for x,y in [([],[]),([1,1,1],[1,2,3]),([0,1,2],[1,2])]:
            with self.assertRaises(ValueError): fit_extension(x,y)
        for fn in (series_compliance,parallel_compliance):
            for values in ([],[0],[1,-1],None,range(10001)):
                with self.assertRaises(ValueError): fn(values)
        for args in ((1,1,1,1),(1,0,1,0)):
            with self.assertRaises(ValueError): infer_modulus(*args)
        with self.assertRaises(ValueError): infer_two_lengths(1,1,1,2,1)
        with self.assertRaises(ValueError): series_compliance([1e308,1e308])
        with self.assertRaises(ValueError): BondLaw(1e296,1e308,8).ideal_chain_modulus_Pa()
        b=BondLaw(1e-19,2e-10)
        for r in (0,1e-15,1):
            with self.assertRaises(ValueError): b.energy_J(r)

if __name__ == '__main__': unittest.main(verbosity=2)
