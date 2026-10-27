# Independent reader review: foundational mathematics gate

The new dynamics unit was authored by a separate team worker. Root read its
implementation, lesson and solutions, then executed independent probes in
[review_math.py](review_math.py). [The raw record](math-reader-probes.json)
fingerprints the reviewed files. This is separate-author team review; it is not
external specialist accreditation or evidence that a learner mastered mathematics.

The cart equilibrium/integrating-factor formula and both Euler/Heun traces agree
with the stated mass, drag and force. The rate and time units are explicit.
The local/global distinction is derived through a Lipschitz recurrence rather
than inferred from a plot. RK4's linear amplification calculation is explicitly
limited; it is not misrepresented as a complete nonlinear order proof. The
modified oscillator quadratic is distinguished from physical energy at mass1kg,
and its positive-definiteness interval excludes the unstable boundary.

Root independently checked16 exact Fraction identities AᵀMA=M, including
parameters outside the positive-definite interval. A new nonlinear test with
y'=1+y²,y(0)=0 used the separately derived oracle tan(t): endpoint error at.7
was9.40050e-11. It required360 field calls. This supplements the author's
linear and manufactured polynomial tests without reusing their recurrence.

A different pulse support(.12,.14), normalized using6!6!/13! rather than the
author's expanded polynomial, still produced the predicted zero/one discrepancy:
the blind path returned0, supplied support returned1.0000000004178087. A fresh
callback counter confirmed an eleven-call budget stopped after eleven calls.
No material defect was found in these selected mechanism/derivation checks.

The existing core was assessed together with the new bridge: algebra/functions,
invariants/Euclid/discrete proofs, complex coordinates, linear maps/elimination,
calculus/quadratic optimization and rounding/error are already connected to
independent rational/finite-difference oracles and separated practice. The new
rate-law build closes the named missing elementary dynamics handoff. Source
maps record inspected selected scopes; unavailable full editions and physical
calibration are not claimed.

The fixed foundational STRONG scope now meets its gate:90.00 weighted readiness,
all six criteria at least87.5, substantive breadth, passed core tests/experiments,
and separate-author review. Full real analysis, eigensolvers, PDEs, general
nonlinear implicit solvers and advanced optimization remain original-mandate
gaps. The original full mathematics domain remains PARTIAL in the separate
EXCELLENT mandate. No denominator or scope changed during the upgrade.
