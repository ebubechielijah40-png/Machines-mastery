import cmath
import math
import random
import unittest
from noise import *


class NoiseTests(unittest.TestCase):
    def assertMatrix(self, a, b):
        for i in range(2):
            for j in range(2):self.assertAlmostEqual(abs(a[i][j]-b[i][j]), 0, places=10)

    def test_density_outer_product_and_mixture_are_different(self):
        coherent = pure(math.sqrt(.8), 1j*math.sqrt(.2))
        mixed = density(((.8, 0), (0, .2)))
        for a,b in zip(z_probabilities(coherent), z_probabilities(mixed)):
            self.assertAlmostEqual(a,b)
        self.assertAlmostEqual(purity(coherent), 1)
        self.assertAlmostEqual(purity(mixed), .68)
        self.assertAlmostEqual(coherent[0][1].imag, -.4)

    def test_x_measurement_exposes_unseen_coherence(self):
        plus = pure(1/math.sqrt(2), 1/math.sqrt(2))
        mixed = density(((.5, 0), (0, .5)))
        self.assertAlmostEqual(z_probabilities(channel(plus, [H]))[0], 1)
        self.assertAlmostEqual(z_probabilities(channel(mixed, [H]))[0], .5)

    def test_phase_flip_closed_form_and_purity_counterexample(self):
        rho = pure(math.sqrt(.6), cmath.exp(.7j)*math.sqrt(.4))
        for p in [0, .1, .5, .9, 1]:
            result = phase_flip(rho, p)
            self.assertAlmostEqual(abs(result[0][1]-(1-2*p)*rho[0][1]), 0)
            self.assertAlmostEqual(result[0][0].real, .6)
        self.assertAlmostEqual(purity(phase_flip(rho, 1)), 1)

    def test_amplitude_damping_matches_independent_entry_formula(self):
        rho = pure(math.sqrt(.7), -1j*math.sqrt(.3))
        for gamma in [0, .01, .4, 1]:
            expected = ((rho[0][0]+gamma*rho[1][1], math.sqrt(1-gamma)*rho[0][1]),
                        (math.sqrt(1-gamma)*rho[1][0], (1-gamma)*rho[1][1]))
            self.assertMatrix(relax(rho, gamma), expected)
        self.assertMatrix(relax(rho, 1), pure(1, 0))

    def test_random_states_channel_validity_and_pure_state_agreement(self):
        rng = random.Random(17)
        for _ in range(100):
            x = rng.random(); angle = rng.uniform(-math.pi, math.pi)
            a, b = math.sqrt(x), math.sqrt(1-x)*cmath.exp(1j*angle)
            rho = pure(a, b)
            self.assertMatrix(channel(rho, [H]), pure((a+b)/math.sqrt(2), (a-b)/math.sqrt(2)))
            for result in [bit_flip(rho, rng.random()), phase_flip(rho, rng.random()), relax(rho, rng.random())]:
                self.assertAlmostEqual(sum(z_probabilities(result)), 1)
                self.assertGreaterEqual(purity(result), .5-1e-10)
                self.assertLessEqual(purity(result), 1+1e-10)

    def test_every_single_bit_error_recovers_complex_superposition(self):
        encoded = encode(math.sqrt(.3), 1j*math.sqrt(.7))
        for mask, expected in [(0,(0,0)), (1,(1,0)), (2,(1,1)), (4,(0,1))]:
            branches = recover(flip_mask(encoded, mask))
            self.assertEqual(len(branches), 1)
            outcome, p, result = branches[0]
            self.assertEqual(outcome, expected);self.assertAlmostEqual(p, 1)
            for a,b in zip(encoded,result):self.assertAlmostEqual(abs(a-b), 0)

    def test_all_eight_masks_and_logical_noise_formula(self):
        original = encode(math.sqrt(.2), cmath.exp(.3j)*math.sqrt(.8))
        logical = pure(original[0], original[7])
        for mask in range(8):
            result = recover(flip_mask(original, mask))[0][2]
            expected = original if mask.bit_count() <= 1 else flip_mask(original,7)
            for a,b in zip(result,expected):self.assertAlmostEqual(abs(a-b),0)
        for p in [0,.01,.1,.4,.5,.8,1]:
            q=3*p*p-2*p*p*p
            self.assertAlmostEqual(logical_error_probability(p),q)
            self.assertMatrix(corrected_bit_noise(original[0],original[7],p),bit_flip(logical,q))

    def test_phase_error_survives_and_syndrome_measurement_branches(self):
        encoded=encode(1/math.sqrt(2),1/math.sqrt(2))
        result=recover(phase_error(encoded,0))[0]
        self.assertEqual(result[0],(0,0))
        self.assertAlmostEqual(abs(sum(a.conjugate()*b for a,b in zip(encoded,result[2]))),0)
        # |000>+|001> has two distinct parity outcomes, not one coherent branch.
        branches=recover(vector((1/math.sqrt(2),1/math.sqrt(2),0,0,0,0,0,0)))
        self.assertEqual(len(branches),2)
        for _,p,_ in branches:self.assertAlmostEqual(p,.5)

    def test_invalid_states_channels_and_probabilities(self):
        for bad in [((1,0),(0,1)), ((.5,1),(1,.5)), ((.5,1j),(1j,.5)), ((float('nan'),0),(0,0))]:
            with self.assertRaises(ValueError):density(bad)
        with self.assertRaises(ValueError):channel(pure(1,0),[scale(I,2)])
        with self.assertRaises(ValueError):pure(1,1)
        for p in [-.1,1.1,float('nan'),True]:
            with self.assertRaises(ValueError):phase_flip(pure(1,0),p)
        with self.assertRaises(ValueError):flip_mask(encode(1,0),8)

    def test_large_finite_inputs_are_controlled_rejections(self):
        with self.assertRaises(ValueError):pure(1e308,0)
        with self.assertRaises(ValueError):pure(10**1000,0)
        with self.assertRaises(ValueError):vector([1e308]+[0]*7)
        with self.assertRaises(ValueError):phase_flip(pure(1,0),10**1000)

if __name__=='__main__':unittest.main(verbosity=2)
