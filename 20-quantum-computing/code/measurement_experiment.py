"""Execute the bounded experiments specified in ../experiments/MEASUREMENT.md.

Run from repository root; stdout is JSON, no files are written by this script.
Seeds and sizes are fixed; this is a classical mathematical simulation.
"""
import cmath
import datetime
import json
import math
import platform
import random
import sys

from simulator import H, Z, State


def bell():
    return State(2).apply1(0, H).cnot(0, 1)


def equal_bit_probability(state):
    return math.fsum(p for i, p in enumerate(state.probs()) if ((i >> 1) & 1) == (i & 1))


def observe():
    phase_sweep = []
    for theta in (0, math.pi / 2, math.pi):
        phase = ((1, 0), (0, cmath.exp(1j * theta)))
        state = State(1).apply1(0, H).apply1(0, phase).apply1(0, H)
        predicted = math.sin(theta / 2) ** 2
        phase_sweep.append({'theta_radians': theta, 'predicted_p1': predicted,
                            'computed_p1': state.probs()[1],
                            'absolute_error': abs(state.probs()[1] - predicted)})

    sampling = []
    for shots in (256, 4096):
        results = State(1).apply1(0, H).sample(shots, seed=1801)
        ones = sum(results)
        standard_error = math.sqrt(.5 * .5 / shots)
        sampling.append({'shots': shots, 'ones': ones, 'frequency_1': ones / shots,
                         'predicted_p1': .5, 'binomial_standard_error_at_p_half': standard_error})

    # Each conditional branch retains a pure state. Averaging branches describes
    # discarded measurement outcomes without pretending it is one statevector.
    coherent = State(1).apply1(0, H).apply1(0, H).probs()
    measured_branches = []
    for outcome in (0, 1):
        state = State(1).apply1(0, H).collapse(0, outcome).apply1(0, H)
        measured_branches.append({'conditioned_outcome': outcome, 'branch_weight': .5,
                                  'after_second_H_probabilities': state.probs()})

    coherent_zz = equal_bit_probability(bell())
    coherent_xx = equal_bit_probability(bell().apply1(0, H).apply1(1, H))
    mixture_zz = mixture_xx = 0
    for initial in (0, 3):
        vector = [0j] * 4
        vector[initial] = 1
        state = State.from_amplitudes(vector)
        mixture_zz += .5 * equal_bit_probability(state)
        mixture_xx += .5 * equal_bit_probability(state.apply1(0, H).apply1(1, H))

    before = bell().probability(1, 1)
    after = bell().apply1(0, H).apply1(0, Z).probability(1, 1)
    counts = {'00': 0, '01': 0, '10': 0, '11': 0}
    rng = random.Random(990)
    for _ in range(512):
        state = bell()
        q0 = state.measure(0, rng=rng)
        q1 = state.measure(1, rng=rng)
        counts[f'{q1}{q0}'] += 1

    return {
        'executed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'environment': {'python': sys.version, 'platform': platform.platform()},
        'kind': 'classical ideal-statevector mechanism experiment; no physical quantum device',
        'phase_sweep': phase_sweep,
        'finite_shots': sampling,
        'measurement_interruption': {'unmeasured_after_second_H': coherent,
                                     'measured_conditioned_branches': measured_branches},
        'bell_vs_classical_mixture': {'coherent_P_equal_ZZ': coherent_zz,
                                      'coherent_P_equal_XX': coherent_xx,
                                      'mixture_P_equal_ZZ': mixture_zz,
                                      'mixture_P_equal_XX': mixture_xx},
        'local_operation_marginal': {'q1_P1_before': before, 'q1_P1_after_U_on_q0': after},
        'bell_partial_measurement_counts_512': counts,
        'representation_lower_bound_complex128_bytes': {str(n): 16 * (1 << n) for n in (10, 20, 30, 40)},
    }


if __name__ == '__main__':
    print(json.dumps(observe(), indent=2, allow_nan=False))
