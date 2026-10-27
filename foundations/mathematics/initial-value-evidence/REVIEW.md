# Author review and remaining independent gate

Author preparation on2026-10-25 checked the state/time/unit contract, all displayed
cart and RK4 arithmetic, linear amplification and symplectic quadratic algebra,
exact pulse normalization, test independence and actual experiment values.
The three current executable SHA256 hashes match
[the raw observation](evidence/observed-2026-10-25.json). All13 tests actually pass.
This is author review, not independent specialist review or learner evidence.
The integrating parent will independently inspect the bounded unit before using
it to support a domain STRONG gate.

Important limitations retained in teaching and implementation:

- The full nonlinear RK4 order proof is not replaced by a scalar polynomial test.
- Backward Euler is implemented only for a solvable scalar decay equation.
- Fixed-step symplectic modified energy is distinguished from physical energy
  and phase accuracy; positivity excludeshω=2.
- Adaptive step doubling is an asymptotic heuristic; the smooth pulse is an
  executed counterexample to an unconditional global-error claim.
- Bounds on attempts/calls/dimensions do not interrupt nonreturning trusted
  callbacks/iterators or provide physical/realtime safety.
- PDEs, DAEs, general nonlinear implicit iteration, robust event localization,
  certified integration and calibrated physical models remain broader gaps.

Tests use different mathematical structures:120 exact Fraction linear-step
cases, a manufactured time polynomial, a closed exponential, discrete energy
growth,100 exact Fraction symplectic steps,4000-step invariant observation,
unit rescaling, resource/zero-span/representability checks, and an independently
integrated pulse. They are finite checks, not exhaustive proofs for all floats.
