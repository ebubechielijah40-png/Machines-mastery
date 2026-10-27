"""Independent dense-action checks, measurement invariants and invalid inputs."""
import cmath
import math
import random
import unittest

from simulator import H, X, Z, MAX_QUBITS, State


def dense_local_action(amplitudes, q, u):
    # Intentionally O(4**n) reference, different from the optimized pair loop.
    result = []
    for row in range(len(amplitudes)):
        total = 0j
        for col, amplitude in enumerate(amplitudes):
            if (row & ~(1 << q)) == (col & ~(1 << q)):
                total += u[(row >> q) & 1][(col >> q) & 1] * amplitude
        result.append(total)
    return result


class SimulatorTests(unittest.TestCase):
    def assertVector(self, actual, expected, tolerance=1e-10):
        self.assertEqual(len(actual), len(expected))
        for a, b in zip(actual, expected):
            self.assertLessEqual(abs(a - b), tolerance)

    def test_legacy_basic_gates(self):
        state = State(1).apply1(0, H)
        self.assertVector(state.probs(), [0.5, 0.5])
        state.apply1(0, H)
        self.assertVector(state.amp, [1, 0])
        self.assertVector(State(1).apply1(0, H).apply1(0, Z).apply1(0, H).amp, [0, 1])

    def test_qubit_order_is_little_endian(self):
        self.assertVector(State(2).apply1(0, X).amp, [0, 1, 0, 0])
        self.assertVector(State(2).apply1(1, X).amp, [0, 0, 1, 0])

    def test_complex_gates_against_dense_oracle(self):
        rng = random.Random(724)
        for n in range(1, 5):
            vector = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(1 << n)]
            scale = math.sqrt(math.fsum(abs(a) ** 2 for a in vector))
            vector = [a / scale for a in vector]
            for q in range(n):
                for _ in range(4):
                    theta, phase = rng.uniform(-math.pi, math.pi), rng.uniform(-math.pi, math.pi)
                    c, s, e = math.cos(theta), math.sin(theta), cmath.exp(1j * phase)
                    gate = ((c, -e.conjugate() * s), (e * s, c))
                    actual = State.from_amplitudes(vector).apply1(q, gate)
                    self.assertVector(actual.amp, dense_local_action(vector, q, gate))
                    self.assertAlmostEqual(actual.norm(), 1.0)

    def test_cnot_all_three_qubit_basis_states(self):
        for control in range(3):
            for target in range(3):
                if control == target:
                    continue
                for initial in range(8):
                    vector = [0j] * 8
                    vector[initial] = 1
                    state = State.from_amplitudes(vector).cnot(control, target)
                    expected_index = initial ^ ((1 << target) if (initial >> control) & 1 else 0)
                    expected = [0j] * 8
                    expected[expected_index] = 1
                    self.assertVector(state.amp, expected)
                    self.assertVector(state.cnot(control, target).amp, vector)

    def test_bell_state_and_inverse(self):
        state = State(2).apply1(0, H).cnot(0, 1)
        self.assertVector(state.amp, [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)])
        state.cnot(0, 1).apply1(0, H)
        self.assertVector(state.amp, [1, 0, 0, 0])

    def test_global_phase_through_circuit(self):
        vector = [math.sqrt(.3), 1j * math.sqrt(.7)]
        phase = cmath.exp(.81j)
        a = State.from_amplitudes(vector).apply1(0, H).apply1(0, Z)
        b = State.from_amplitudes([phase * x for x in vector]).apply1(0, H).apply1(0, Z)
        self.assertVector(b.amp, [phase * x for x in a.amp])
        self.assertVector(a.probs(), b.probs())

    def test_partial_measurement_preserves_unmeasured_coherence(self):
        # q1 is deterministic; measuring it must not turn q0's |+> into a mixture.
        state = State(2).apply1(0, H)
        self.assertEqual(state.measure(1, seed=3), 0)
        state.apply1(0, H)
        self.assertVector(state.amp, [1, 0, 0, 0])

    def test_conditional_measurement_formula(self):
        vector = [math.sqrt(.1), 1j * math.sqrt(.2), -math.sqrt(.3), math.sqrt(.4)]
        for q in range(2):
            for outcome in (0, 1):
                mask = [a if (i >> q) & 1 == outcome else 0j for i, a in enumerate(vector)]
                mass = math.fsum(abs(a) ** 2 for a in mask)
                state = State.from_amplitudes(vector)
                self.assertAlmostEqual(state.probability(q, outcome), mass)
                state.collapse(q, outcome)
                self.assertVector(state.amp, [a / math.sqrt(mass) for a in mask])
                self.assertAlmostEqual(state.norm(), 1)

    def test_bell_measurement_correlates_and_repeats(self):
        seen = set()
        rng = random.Random(91)
        for _ in range(128):
            state = State(2).apply1(0, H).cnot(0, 1)
            first = state.measure(0, rng=rng)
            seen.add(first)
            self.assertEqual(state.measure(0, rng=rng), first)
            self.assertEqual(state.measure(1, rng=rng), first)
            self.assertAlmostEqual(state.norm(), 1)
        self.assertEqual(seen, {0, 1})

    def test_sampling_does_not_collapse(self):
        state = State(1).apply1(0, H)
        before = list(state.amp)
        outcomes = state.sample(100, seed=91)
        self.assertEqual(len(outcomes), 100)
        self.assertEqual(set(outcomes), {0, 1})
        self.assertEqual(outcomes, state.sample(100, seed=91))
        self.assertVector(state.amp, before)
        self.assertEqual(state.sample(0), [])

    def test_never_sample_zero_probability_bin(self):
        self.assertEqual(State(2).apply1(1, X).sample(100), [2] * 100)

    def test_impossible_postselection_is_rejected_without_mutation(self):
        state = State(1)
        with self.assertRaises(ValueError):
            state.collapse(0, 1)
        self.assertVector(state.amp, [1, 0])

    def test_tiny_nonzero_postselection_remains_valid(self):
        state = State.from_amplitudes([math.sqrt(1 - 1e-16), 1e-8])
        state.collapse(0, 1)
        self.assertVector(state.amp, [0, 1])

    def test_invalid_state_construction(self):
        for n in (0, -1, MAX_QUBITS + 1):
            with self.assertRaises(ValueError):
                State(n)
        for n in (1.2, True, '2'):
            with self.assertRaises(TypeError):
                State(n)
        for vector in ([], [1], [1, 0, 0], [0, 0], [1, 1], [float('nan'), 0], [float('inf'), 0], [1e308, 0], ['1', '0']):
            with self.assertRaises(ValueError):
                State.from_amplitudes(vector)

    def test_invalid_qubits_on_all_operations(self):
        state = State(2)
        for q in (-1, 2):
            for action in (lambda: state.apply1(q, H), lambda: state.cnot(q, 0),
                           lambda: state.cnot(0, q), lambda: state.measure(q)):
                with self.assertRaises(IndexError):
                    action()
        with self.assertRaises(TypeError):
            state.apply1(True, H)
        with self.assertRaises(ValueError):
            state.cnot(0, 0)

    def test_invalid_gate_is_rejected_without_mutation(self):
        state = State(1)
        for gate in ([], [[1]], [[1, 0], [0, 2]], [[1, 1], [0, 1]], [[float('nan'), 0], [0, 1]], [[1e308, 0], [0, 1e308]]):
            with self.assertRaises(ValueError):
                state.apply1(0, gate)
            self.assertVector(state.amp, [1, 0])

    def test_mutated_invalid_state_is_detected(self):
        for vector in ([0, 0], [1, 0, 0], [complex('nan'), 0]):
            state = State(1)
            state.amp = vector
            for action in (lambda: state.sample(), lambda: state.measure(0),
                           lambda: state.apply1(0, H)):
                with self.assertRaises(ValueError):
                    action()

    def test_invalid_measurement_arguments(self):
        state = State(1)
        for shots in (-1,):
            with self.assertRaises(ValueError):
                state.sample(shots)
        for shots in (1.5, True):
            with self.assertRaises(TypeError):
                state.sample(shots)
        with self.assertRaises(ValueError):
            state.collapse(0, 2)
        with self.assertRaises(ValueError):
            state.measure(0, seed=1, rng=random.Random(1))
        with self.assertRaises(TypeError):
            state.measure(0, rng=object())


def run():
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SimulatorTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(f'quantum simulator: PASS ({result.testsRun} tests)')


if __name__ == '__main__':
    run()
