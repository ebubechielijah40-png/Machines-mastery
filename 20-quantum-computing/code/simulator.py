"""Bounded ideal pure-state simulator; see ../10_STATEVECTOR_MEASUREMENT.md.

Index i denotes |q[n-1]...q[0]>, with q0 the least significant bit.
The public amp list is retained for old lessons; invalid mutation is detected
before gates, sampling and measurement. This is not a physical-device model.
"""
from __future__ import annotations

import math
import random

SQRT2 = math.sqrt(2)
X = ((0j, 1 + 0j), (1 + 0j, 0j))
Z = ((1 + 0j, 0j), (0j, -1 + 0j))
H = ((1 / SQRT2, 1 / SQRT2), (1 / SQRT2, -1 / SQRT2))
MAX_QUBITS = 20  # explicit teaching-process allocation guard, not a hardware limit
TOLERANCE = 1e-10


def _integer(value, label):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f'{label} must be an integer (not bool)')


def _finite_complex(value):
    if not isinstance(value, (int, float, complex)):
        raise ValueError('amplitudes and gate entries must be numeric')
    try:
        z = complex(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('amplitudes and gate entries must be finite numbers') from exc
    if not math.isfinite(z.real) or not math.isfinite(z.imag):
        raise ValueError('amplitudes and gate entries must be finite numbers')
    return z


class State:
    def __init__(self, n: int):
        _integer(n, 'n')
        if not 1 <= n <= MAX_QUBITS:
            raise ValueError(f'1 <= n <= {MAX_QUBITS}; simulation is exponential')
        self.n = n
        self.amp = [0j] * (1 << n)
        self.amp[0] = 1 + 0j

    @classmethod
    def from_amplitudes(cls, amplitudes):
        """Accept a finite normalized vector, without silently renormalizing it."""
        data = [_finite_complex(a) for a in amplitudes]
        size = len(data)
        if size < 2 or size & (size - 1):
            raise ValueError('vector length must be 2**n with n >= 1')
        state = cls(size.bit_length() - 1)
        state.amp = data
        state._validate_state()
        return state

    def _qubit(self, q):
        _integer(q, 'qubit')
        if not 0 <= q < self.n:
            raise IndexError(q)

    def _validate_state(self):
        if len(self.amp) != 1 << self.n:
            raise ValueError('amplitude vector length does not match n')
        for amplitude in self.amp:
            _finite_complex(amplitude)
        try:
            norm = self.norm()
        except OverflowError as exc:
            raise ValueError('state squared norm overflowed') from exc
        if not math.isclose(norm, 1.0, rel_tol=0.0, abs_tol=TOLERANCE):
            raise ValueError('state must have squared norm one')

    @staticmethod
    def _gate(u):
        try:
            matrix = tuple(tuple(_finite_complex(a) for a in row) for row in u)
        except TypeError as exc:
            raise ValueError('gate must be a 2 by 2 matrix') from exc
        if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
            raise ValueError('gate must be a 2 by 2 matrix')
        # Columns must be orthonormal: U-dagger U = identity.
        for a in range(2):
            for b in range(2):
                inner = sum(matrix[k][a].conjugate() * matrix[k][b] for k in range(2))
                _finite_complex(inner)
                if abs(inner - (1 if a == b else 0)) > TOLERANCE:
                    raise ValueError('gate must be unitary')
        return matrix

    def apply1(self, q: int, u):
        self._qubit(q)
        self._validate_state()
        u = self._gate(u)
        step = 1 << q
        for base in range(0, 1 << self.n, step * 2):
            for off in range(step):
                i = base + off
                j = i + step
                a, b = self.amp[i], self.amp[j]  # save both before either write
                self.amp[i] = u[0][0] * a + u[0][1] * b
                self.amp[j] = u[1][0] * a + u[1][1] * b
        return self

    def cnot(self, control: int, target: int):
        self._qubit(control)
        self._qubit(target)
        if control == target:
            raise ValueError('control != target')
        self._validate_state()
        for i in range(1 << self.n):
            if (i >> control) & 1 and not ((i >> target) & 1):
                j = i | (1 << target)
                self.amp[i], self.amp[j] = self.amp[j], self.amp[i]
        return self

    def probs(self):
        """Raw computational-basis squared magnitudes, useful for diagnostics."""
        return [abs(a) ** 2 for a in self.amp]

    def norm(self):
        """Squared Euclidean norm; retained name for backward compatibility."""
        return math.fsum(self.probs())

    def probability(self, q: int, outcome: int):
        self._qubit(q)
        _integer(outcome, 'outcome')
        if outcome not in (0, 1):
            raise ValueError('outcome must be 0 or 1')
        self._validate_state()
        return math.fsum(abs(a) ** 2 for i, a in enumerate(self.amp)
                         if (i >> q) & 1 == outcome)

    def collapse(self, q: int, outcome: int):
        """Conditional projection; no randomness. Reject an impossible outcome."""
        probability = self.probability(q, outcome)
        if probability == 0:
            raise ValueError('cannot condition on an outcome of probability zero')
        scale = math.sqrt(probability)
        self.amp = [a / scale if (i >> q) & 1 == outcome else 0j
                    for i, a in enumerate(self.amp)]
        return self

    def measure(self, q: int, seed=None, *, rng=None):
        """One ideal Z-basis measurement, returning a bit and collapsing in place.

        Pass a shared random.Random through rng for an experiment stream. Pass
        seed for a reproducible single invocation; seed and rng are exclusive.
        """
        if seed is not None and rng is not None:
            raise ValueError('choose seed or rng, not both')
        if rng is None:
            rng = random.Random(seed)
        elif not isinstance(rng, random.Random):
            raise TypeError('rng must be random.Random')
        p0 = self.probability(q, 0)
        p1 = self.probability(q, 1)
        outcome = 0 if rng.random() < p0 / (p0 + p1) else 1
        self.collapse(q, outcome)
        return outcome

    def sample(self, shots=1, seed=0):
        """Sample fresh preparations of this state; leave amp unchanged.

        This is deliberately different from repeated projective measurements
        of one specimen. The same seed repeats the same pseudorandom stream.
        """
        _integer(shots, 'shots')
        if shots < 0:
            raise ValueError('shots must be nonnegative')
        self._validate_state()
        rng = random.Random(seed)
        p = self.probs()
        total = math.fsum(p)
        out = []
        last_nonzero = max(i for i, x in enumerate(p) if x > 0)
        for _ in range(shots):
            r = rng.random() * total
            cumulative = 0.0
            for i, probability in enumerate(p):
                cumulative += probability
                if r < cumulative:
                    out.append(i)
                    break
            else:  # rounding of the cumulative sum, never select a zero-mass bin
                out.append(last_nonzero)
        return out
