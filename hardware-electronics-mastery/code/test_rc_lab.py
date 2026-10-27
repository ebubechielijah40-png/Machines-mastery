"""Tests physical invariants, numerical failure modes, and input boundaries."""
import math
import unittest

from rc_lab import (loaded_parameters, rc_charge, rc_response, simulate,
                    time_constant, time_to_threshold)


class RCTests(unittest.TestCase):
    def test_initial_state_and_equilibrium(self):
        self.assertEqual(rc_response(3.3, 10_000, 10e-6, 0, 1.2), 1.2)
        self.assertAlmostEqual(rc_response(1.2, 10_000, 10e-6, 100, 1.2), 1.2)
        self.assertAlmostEqual(rc_charge(3.3, 10_000, 10e-6, 100), 3.3)

    def test_reference_case_and_threshold_inverse(self):
        tau = time_constant(10_000, 10e-6)
        self.assertAlmostEqual(tau, 0.1)
        self.assertAlmostEqual(rc_charge(3.3, 10_000, 10e-6, tau),
                               3.3 * (1 - math.exp(-1)))
        for fraction in (1e-12, 0.1, 0.5, 0.9, 1 - 1e-12):
            voltage = fraction * 3.3
            t = time_to_threshold(3.3, 10_000, 10e-6, voltage)
            self.assertAlmostEqual(rc_charge(3.3, 10_000, 10e-6, t), voltage)

    def test_small_charge_not_lost_to_subtraction(self):
        self.assertGreater(rc_charge(1, 1, 1, 1e-20), 0)
        self.assertAlmostEqual(rc_charge(1, 1, 1, 1e-20) / 1e-20, 1)

    def test_discharge_signed_and_precharged(self):
        for initial, final in ((5, 0), (5, 3.3), (-5, -3.3), (-3, 2)):
            points = simulate(final, 1000, 1e-6, 0.0001, 100,
                              v_initial=initial, method="exact")
            for _, voltage in points:
                self.assertLessEqual(min(initial, final), voltage + 1e-14)
                self.assertGreaterEqual(max(initial, final), voltage - 1e-14)
            expected = final + (initial - final) * math.exp(-1)
            self.assertAlmostEqual(rc_response(final, 1000, 1e-6, 0.001,
                                               initial), expected)

    def test_rescaling_time_and_capacitance(self):
        original = rc_charge(3.3, 10_000, 10e-6, 0.05)
        self.assertAlmostEqual(rc_charge(3.3, 10_000, 20e-6, 0.10), original)
        self.assertAlmostEqual(rc_charge(3.3, 20_000, 10e-6, 0.10), original)

    def test_analytic_ode_residual(self):
        # Different calculation: a central difference must satisfy C dv/dt=i_R.
        r, c, t, h, supply = 10_000, 10e-6, 0.035, 1e-6, 3.3
        dvdt = (rc_charge(supply, r, c, t + h) -
                rc_charge(supply, r, c, t - h)) / (2 * h)
        current = (supply - rc_charge(supply, r, c, t)) / r
        self.assertAlmostEqual(c * dvdt, current, places=10)

    def test_energy_balance_by_numerical_quadrature(self):
        # Independent midpoint integration of resistor loss and source work.
        supply, r, c = 3.3, 10_000, 10e-6
        end, n = 1.0, 20_000
        dt = end / n
        source_energy = 0.0
        resistor_energy = 0.0
        for i in range(n):
            voltage = rc_charge(supply, r, c, (i + 0.5) * dt)
            current = (supply - voltage) / r
            source_energy += supply * current * dt
            resistor_energy += current * current * r * dt
        stored = 0.5 * c * rc_charge(supply, r, c, end) ** 2
        self.assertLess(abs(source_energy - resistor_energy - stored), 1e-11)

    def test_meter_loading_parameters(self):
        final, r_effective, c_total = loaded_parameters(3.3, 100_000, 1e-6,
                                                       1_000_000, 100e-12)
        self.assertAlmostEqual(final, 3.0)
        self.assertAlmostEqual(r_effective, 1 / (1 / 100_000 + 1 / 1_000_000))
        self.assertAlmostEqual(c_total, 1.0001e-6)
        self.assertLess(time_constant(r_effective, c_total), 0.1)

    def test_euler_convergence_at_fixed_horizon(self):
        exact = rc_charge(3.3, 10_000, 10e-6, 0.1)
        for method in ("euler", "backward-euler"):
            errors = [abs(simulate(3.3, 10_000, 10e-6, 0.1/n, n,
                                   method=method)[-1][1] - exact)
                      for n in (20, 40, 80)]
            self.assertGreater(errors[0] / errors[1], 1.9)
            self.assertLess(errors[0] / errors[1], 2.1)
            self.assertGreater(errors[1] / errors[2], 1.9)
            self.assertLess(errors[1] / errors[2], 2.1)

    def test_euler_physical_range_and_instability(self):
        stable = simulate(3.3, 1, 1, 0.5, 10)
        self.assertTrue(all(0 <= voltage <= 3.3 for _, voltage in stable))
        overshoot = simulate(3.3, 1, 1, 1.5, 10)
        self.assertGreater(overshoot[1][1], 3.3)
        marginal = simulate(3.3, 1, 1, 2, 10)
        self.assertAlmostEqual(marginal[-1][1], 0)
        unstable = simulate(3.3, 1, 1, 2.5, 10)
        self.assertGreater(abs(unstable[-1][1] - 3.3), 3.3)
        implicit = simulate(3.3, 1, 1, 2.5, 10, method="backward-euler")
        self.assertTrue(all(0 <= voltage <= 3.3 for _, voltage in implicit))

    def test_bad_model_inputs(self):
        for value in (0, -1, math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    time_constant(value, 1)
                with self.assertRaises(ValueError):
                    time_constant(1, value)
        for t in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                rc_charge(3.3, 1, 1, t)
        for r, c in ((1e308, 1e308), (1e-300, 1e-300)):
            with self.assertRaises(ValueError):
                time_constant(r, c)
        for value in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                rc_charge(value, 1, 1, 1)
        for threshold in (-1, 0, 3.3, 4, math.nan, math.inf):
            with self.assertRaises(ValueError):
                time_to_threshold(3.3, 1, 1, threshold)
        with self.assertRaises(ValueError):
            time_to_threshold(1, -1, 1, 0.5)
        with self.assertRaises(ValueError):
            loaded_parameters(3.3, 1, 1, -1)
        with self.assertRaises(ValueError):
            loaded_parameters(3.3, 1, 1, 1, -1)

    def test_simulation_contract(self):
        self.assertEqual(simulate(1, 1, 1, 0.1, 0), [(0.0, 0.0)])
        with self.assertRaises(ValueError):
            simulate(1, 1, 1, 0, 5)
        for steps in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                simulate(1, 1, 1, 0.1, steps)
        with self.assertRaises(ValueError):
            simulate(1, 1, 1, 0.1, 5, method="magic")


def run():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RCTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("rc_lab: PASS")


if __name__ == "__main__":
    run()
