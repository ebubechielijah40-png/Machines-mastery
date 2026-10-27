import itertools
import math
import random
import unittest
from fractions import Fraction
from discriminative import (Logistic, CircularCNN, ScalarRNN, Standardizer,
                            sigmoid, binary_loss, batch_step, metrics, correlate2d)
from generative import GaussianMixture, Bigram


class ModelTests(unittest.TestCase):
    def test_stable_binary_loss_and_derivative(self):
        self.assertAlmostEqual(binary_loss(0, 0), math.log(2))
        for y in (0, 1):
            for z in (-1000, -100, -1.3, 0, .8, 100, 1000):
                self.assertTrue(math.isfinite(binary_loss(z, y)))
                self.assertAlmostEqual(binary_loss(z, y), binary_loss(-z, 1-y))
        for bad in (float('inf'), float('nan'), True, '3', 10**1000):
            with self.assertRaises(ValueError): binary_loss(bad, 1)
        for bad in (True, 2, .5):
            with self.assertRaises(ValueError): binary_loss(1, bad)

    def test_all_parameter_gradients_against_central_differences(self):
        rng = random.Random(1934)
        cases = [(Logistic(3), (1.2, -.7, .3)),
                 (Logistic(3, .2), (1.2, -.7, .3)),
                 (CircularCNN(2, 3, 'mean'), (1.2, -.7, .3, .6, -.2)),
                 (CircularCNN(2, 3, 'max'), (1.2, -.7, .3, .6, -.2)),
                 (ScalarRNN(), (.5, -.3, 1.1, 0.2))]
        for model, x in cases:
            for _ in range(6):
                p = tuple(rng.uniform(-.7, .7) for _ in range(model.parameter_count))
                _, grad = model.loss_grad(p, x, 1)
                for j, g in enumerate(grad):
                    step = 1e-5
                    a, b = list(p), list(p)
                    a[j] += step; b[j] -= step
                    fd = (model.loss_grad(a, x, 1)[0] - model.loss_grad(b, x, 1)[0]) / (2*step)
                    self.assertAlmostEqual(g, fd, delta=2e-7, msg=(type(model).__name__, j))

    def test_logistic_hand_values_and_gradient(self):
        m = Logistic(2)
        loss, grad = m.loss_grad((0, 0, 0), (3, -2), 1)
        self.assertAlmostEqual(loss, math.log(2))
        self.assertEqual(grad, (-1.5, 1, -.5))
        self.assertEqual(m.logit((2, -1, .5), (3, -2)), 8.5)

    def test_cnn_equivariance_invariance_and_kernel_orientation(self):
        x = (1, .3, -.8, 1.7, 0)
        p = (.7, -.1, .3, -.2, .5, -.4, .1, .2, .6, -.3, .1)
        for pooling in ('mean', 'max'):
            m = CircularCNN(2, 3, pooling)
            features, z = m.features(p, x), m.logit(p, x)
            _, g = m.loss_grad(p, x, 1)
            for shift in range(len(x)):
                rot = x[shift:] + x[:shift]
                f = m.features(p, rot)
                for a, b in zip(f, features):
                    for u, v in zip(a, b[shift:] + b[:shift]): self.assertAlmostEqual(u, v)
                self.assertAlmostEqual(m.logit(p, rot), z)
                for u, v in zip(m.loss_grad(p, rot, 1)[1], g): self.assertAlmostEqual(u, v)
        m = CircularCNN(1, 2)
        self.assertAlmostEqual(m.features((1, 2, 0, 1, 0), (1, 2, 3))[0][0], math.tanh(5))

    def test_2d_correlation_against_exact_patch_dot_products(self):
        image = ((2, 1, 0), (3, -1, 4), (0, 2, 5))
        kernel = ((1, -2), (0, 3))
        self.assertEqual(correlate2d(image, kernel), ((-3, 13), (11, 6)))
        rng = random.Random(4321)
        for h, w, kh, kw, pad, stride in itertools.product((2, 3), (2, 4), (1, 2), (1, 2), (0, 1), (1, 2)):
            a = [[rng.randint(-4, 4) for _ in range(w)] for _ in range(h)]
            b = [[rng.randint(-3, 3) for _ in range(kw)] for _ in range(kh)]
            padded = [[0] * (w + 2*pad) for _ in range(h + 2*pad)]
            for i in range(h):
                for j in range(w): padded[i+pad][j+pad] = a[i][j]
            oracle = tuple(tuple(float(sum((Fraction(padded[i+u][j+v])*b[u][v]
                                            for u in range(kh) for v in range(kw)), Fraction()))
                                 for j in range(0, w+2*pad-kw+1, stride))
                           for i in range(0, h+2*pad-kh+1, stride))
            self.assertEqual(correlate2d(a, b, pad, stride), oracle)

    def test_rnn_backward_input_chain_and_causal_prefix(self):
        m, p, x = ScalarRNN(), (.7, .8, .1, 1.2, -.3), (.4, -.2, .9, 0)
        loss, _, dx = m.gradients(p, x, 1)
        for j, derivative in enumerate(dx):
            a, b = list(x), list(x);a[j] += 1e-5;b[j] -= 1e-5
            fd = (binary_loss(m.logit(p, a), 1)-binary_loss(m.logit(p, b), 1)) / 2e-5
            self.assertAlmostEqual(derivative, fd, delta=1e-8)
        states = m.states(p, x)
        product = (sigmoid(m.logit(p, x))-1)*p[3]*p[0]
        for j, h in enumerate(states): product *= (1-h*h)*(p[1] if j else 1)
        self.assertAlmostEqual(dx[0], product)
        self.assertEqual(m.states(p, x)[:2], m.states(p, x[:2] + (-1, .5))[:2])

    def test_exploding_recurrent_adjoint_is_controlled(self):
        with self.assertRaises(ValueError):
            ScalarRNN().loss_grad((1, 1e6, 0, 1, 0), (0,)*256, 1)

    def test_standardizer_train_only_constant_and_generator(self):
        scaler = Standardizer.fit(iter([(1, 4), (3, 4)]))
        self.assertEqual(scaler.means, (2, 4));self.assertEqual(scaler.scales, (1, 1))
        self.assertEqual(scaler.transform((3, 4)), (1, 0))
        self.assertEqual(scaler.transform((100, 10)), (98, 6))
        self.assertEqual(scaler.means, (2, 4))
        with self.assertRaises(ValueError):Standardizer.fit([])
        with self.assertRaises(ValueError):scaler.transform([1])

    def test_update_clipping_repeated_batches_and_no_mutation(self):
        m, p = Logistic(2), (0, 0, 0)
        updated, r = batch_step(m, iter(p), iter([((3, 4), 1)]), .2, clip=1)
        self.assertAlmostEqual(math.dist(p, updated), .2)
        self.assertLess(r['clipping_scale'], 1)
        self.assertEqual(p, (0, 0, 0))
        a = batch_step(m, p, [((3, 4), 1)], .1)[0]
        b = batch_step(m, p, [((3, 4), 1)]*4, .1)[0]
        self.assertEqual(a, b)
        old = p
        with self.assertRaises(ValueError):batch_step(m, p, [((3, 4), True)], .1)
        self.assertEqual(old, p)
        with self.assertRaises(ValueError):batch_step(m, p, [], .1)

    def test_training_reduces_actual_objective(self):
        model = Logistic(1);p = (0, 0)
        data = [((-2,), 0), ((-1,), 0), ((1,), 1), ((2,), 1)]
        before = metrics(model, p, data)
        for _ in range(80):p, _ = batch_step(model, p, data, .2)
        after = metrics(model, p, data)
        self.assertLess(after['nll'], before['nll']/5)
        self.assertEqual(after['accuracy'], 1)

    def test_invalid_shapes_and_bounded_contracts(self):
        for m, p, x in [(Logistic(2), (0, 0, 0), (1,)),
                         (CircularCNN(1, 3), (0,)*6, (1,)),
                         (ScalarRNN(), (0,)*5, ())]:
            with self.assertRaises(ValueError):m.logit(p, x)
        with self.assertRaises(ValueError):CircularCNN(pooling='attention')
        with self.assertRaises(ValueError):ScalarRNN(5.0)
        for a, b in [([], [[1]]), ([[1], [1, 2]], [[1]]), ([[1]], [[1, 2]])]:
            with self.assertRaises(ValueError):correlate2d(a, b)


class GenerativeTests(unittest.TestCase):
    def test_mixture_posterior_hand_case_and_label_permutation(self):
        a = GaussianMixture((.25, .75), (-1, 1), (1, 1))
        self.assertAlmostEqual(a.posterior(0)[0], .25)
        for x in (-100, -1, 0, 1, 100):
            self.assertAlmostEqual(sum(a.posterior(x)), 1)
            b = GaussianMixture(a.weights[::-1], a.means[::-1], a.variances[::-1])
            self.assertAlmostEqual(a.nll([x]), b.nll([x]))
            for u, v in zip(a.posterior(x), b.posterior(x)[::-1]):self.assertAlmostEqual(u, v)

    def test_em_one_component_exact_moment_oracle(self):
        a = GaussianMixture((1,), (17,), (100,))
        b = a.em_step([-2, 0, 2], 1e-4)
        self.assertEqual(b.weights, (1,));self.assertEqual(b.means, (0,))
        self.assertAlmostEqual(b.variances[0], float(Fraction(8, 3)))

    def test_em_monotonic_likelihood_floor_and_frozen_inputs(self):
        rng = random.Random(193)
        x = [rng.gauss(-2, .3) for _ in range(40)] + [rng.gauss(2, .5) for _ in range(60)]
        a = GaussianMixture((.5, .5), (-1, 1), (2, 2))
        for _ in range(15):
            b = a.em_step(x, .01)
            self.assertLessEqual(b.nll(x), a.nll(x) + 1e-12)
            self.assertTrue(all(v >= .01 for v in b.variances));a = b
        self.assertAlmostEqual(a.weights[0], .4, places=5)
        c = GaussianMixture((.5,.5),(1,1),(1,1)).em_step([1,1,1], .01)
        self.assertEqual(c.variances, (.01,.01))
        self.assertLess(c.nll([1]), 0)  # Density >1 is legal; density is not point mass.

    def test_mixture_sampling_and_controlled_dead_component(self):
        m = GaussianMixture((.5, .5), (-1, 1), (.1, .1))
        self.assertEqual(m.sample(8, 9), m.sample(8, 9))
        self.assertEqual(m.sample(0), ())
        m = GaussianMixture((.5,.5),(-100,100),(1e-4,1e-4))
        with self.assertRaises(ValueError):m.em_step([-100], 1e-4)
        for w, mu, v in [((0,1),(0,1),(1,1)),((.5,.6),(0,1),(1,1)),((1,),(0,),(0,)),((1,),(True,),(1,))]:
            with self.assertRaises(ValueError):GaussianMixture(w,mu,v)

    def test_bigram_exact_counts_likelihood_and_no_cross_document_transition(self):
        m = Bigram.fit(iter(['ab','aa']), ('a','b'), 1)
        self.assertEqual(m.counts, ((1,1,1),(0,0,1),(2,0,0)))
        self.assertEqual(m.distribution(None), (.6,.2,.2))
        self.assertEqual(m.distribution('a'), (1/3,1/3,1/3))
        expected = -math.log(Fraction(3,5)*Fraction(1,3)*Fraction(1,2))/3
        self.assertAlmostEqual(m.nll(['ab']), expected)
        self.assertEqual(m.counts[1][0], 0)
        self.assertTrue(math.isfinite(m.nll(['bb'])))

    def test_bigram_caps_generator_immutability_and_unknown_rejection(self):
        counts = [[1,2],[3,4]];m=Bigram(('a',), counts, 1)
        counts[0][0] = 999
        self.assertEqual(m.counts[0][0], 1)
        fitted = Bigram.fit(['aaaa'], ['a'], .001)
        self.assertEqual(fitted.sample(5, 123), fitted.sample(5,123))
        self.assertLessEqual(len(fitted.sample(0, 1)['text']), 0)
        for call in [lambda:Bigram.fit([], ['a']),lambda:Bigram.fit(['x'],['a']),
                     lambda:Bigram.fit(['a'],['a'],0),lambda:Bigram([[]], [[0]],1),
                     lambda:fitted.nll(['?']),lambda:fitted.distribution(True)]:
            with self.assertRaises(ValueError):call()


if __name__ == '__main__':unittest.main(verbosity=2)
