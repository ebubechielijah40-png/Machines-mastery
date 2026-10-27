"""Independent finite differences, Decimal arithmetic and cache contract tests."""
from decimal import Decimal, localcontext
import math
import random
import unittest
from attention import (CausalCache, attention_backward, causal_attention, identity,
                       matvec, scaled_dot_attention, softmax)


class AttentionDerivativesTests(unittest.TestCase):
    def test_decimal_two_key_oracle(self):
        # Oracle computes direct exp(score), without production softmax/matvec.
        q = [0.25, -0.75]
        keys = [[0.5, 0.25], [-0.25, 1.0]]
        values = [[2.0, -1.0], [4.0, 3.0]]
        actual, weights = scaled_dot_attention(q, keys, values)
        with localcontext() as ctx:
            ctx.prec = 50
            divisor = Decimal(2).sqrt()
            scores = [sum(Decimal(a) * Decimal(b) for a, b in zip(q, key)) / divisor for key in keys]
            exponentials = [score.exp() for score in scores]
            probabilities = [e / sum(exponentials) for e in exponentials]
            expected = [sum(a * Decimal(v[j]) for a, v in zip(probabilities, values)) for j in range(2)]
        for observed, oracle in zip(actual, expected):
            self.assertAlmostEqual(observed, float(oracle), places=13)
        for observed, oracle in zip(weights, probabilities):
            self.assertAlmostEqual(observed, float(oracle), places=13)

    def test_all_local_gradients_by_central_difference(self):
        q, keys, values, g = [0.3, -0.7], [[0.2, 0.8], [-0.5, 0.4], [0.9, -0.1]], [[0.4, 1.2], [-0.3, 0.6], [0.7, -0.9]], [0.6, -0.4]
        for scale in (True, False):
            analytic = attention_backward(q, keys, values, g, scale)
            groups = [q, *keys, *values]
            derivatives = [analytic[0], *analytic[1], *analytic[2]]
            def loss():
                out, _ = scaled_dot_attention(q, keys, values, scale)
                return sum(a * b for a, b in zip(out, g))
            for vector, gradient in zip(groups, derivatives):
                for j in range(len(vector)):
                    old = vector[j]
                    h = 1e-6
                    vector[j] = old + h
                    plus = loss()
                    vector[j] = old - h
                    minus = loss()
                    vector[j] = old
                    self.assertAlmostEqual(gradient[j], (plus - minus) / (2*h), delta=1e-8)

    def test_single_key_routing_has_zero_query_key_gradient(self):
        dq, dk, dv = attention_backward([2., 4.], [[3., 5.]], [[7.]], [2.])
        self.assertEqual(dq, [0., 0.])
        self.assertEqual(dk, [[0., 0.]])
        self.assertEqual(dv, [[2.]])

    def test_uniform_keys_produce_mean_values(self):
        out, weights = scaled_dot_attention([4., -5.], [[0.,0.]] * 3, [[1.], [2.], [9.]])
        self.assertAlmostEqual(out[0], 4.)
        self.assertEqual(weights, [1/3]*3)

    def test_translation_of_logits_leaves_distribution(self):
        expected = softmax([-1., 2., 3.])
        actual = softmax([9999., 10002., 10003.])
        for a, b in zip(expected, actual):
            self.assertAlmostEqual(a, b, places=14)

    def test_cache_matches_full_prefixes_rectangular_values(self):
        rng = random.Random(2718)
        tokens = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(9)]
        wq = [[0.2, -0.1], [0.5, 0.3], [-0.4, 0.7]]
        wk = [[0.4, 0.3], [-0.2, 0.6], [0.1, -0.5]]
        wv = [[1.], [-0.5], [0.25]]
        cache = CausalCache(wq, wk, wv)
        for i, token in enumerate(tokens):
            observed, weights = cache.step(token)
            all_out, all_weights = causal_attention(tokens[:i+1], wq, wk, wv)
            for a, b in zip(observed, all_out[-1]):
                self.assertAlmostEqual(a, b, places=14)
            self.assertEqual(weights, all_weights[-1])
        cache.clear()
        self.assertEqual(cache.step(tokens[0])[1], [1.])

    def test_projection_mutation_does_not_change_cache(self):
        matrix = identity(2)
        cache = CausalCache(matrix, matrix, matrix)
        matrix[0][0] = 100.
        self.assertEqual(cache.step([1., 0.])[0], [1., 0.])

    def test_invalid_step_leaves_state_unchanged(self):
        cache = CausalCache(identity(2), identity(2), identity(2))
        cache.step([1., 0.])
        with self.assertRaises(ValueError):
            cache.step([math.inf, 1.])
        self.assertEqual(len(cache.keys), 1)
        self.assertEqual(len(cache.values), 1)

    def test_invalid_shapes_and_nonfinite_values(self):
        cases = [([], [[1.]], [[1.]]), ([1.], [], []), ([1.], [[1.]], [[1.], [2.]]),
                 ([1.], [[1.]], [[math.nan]]), ([math.inf], [[1.]], [[1.]]),
                 ([1.], [[1.], [2.,3.]], [[1.], [2.]])]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                scaled_dot_attention(*args)
        with self.assertRaises(ValueError):
            matvec([1.], [[math.inf]])
        with self.assertRaises(ValueError):
            scaled_dot_attention([1e308], [[1e308]], [[1.]])
        with self.assertRaises(ValueError):
            CausalCache([[1.]], [[1., 2.]], [[1.]])

    def test_mask_after_normalization_counterexample(self):
        wrong = softmax([0., 0., 20.])[:2]
        right = softmax([0., 0.])
        self.assertLess(sum(wrong), 1e-8)
        self.assertEqual(sum(right), 1.)


if __name__ == '__main__':
    unittest.main()
