# Observed numerical experiment — 2026-10-22

Ran `experiment.py` with Python3.12.14 on Linux; complete metadata and18 step
rows are in [the raw JSON](observed-2026-10-22.json). This is synthetic software
evidence, not physical measurements or learner assessment.

For x³ at x=1, central errors were about0.01,0.0001,0.000001 as h changed from
0.1 to0.01 to0.001, consistent with the derived h² term before rounding dominated.
At h=10^-7 the reported central error was zero, then about5.55×10^-9 at10^-8.
Several still-smaller steps happened to return3 exactly using the actual endpoint
span. At10^-16 and below the helper rejected indistinguishable endpoints. The
curve is not a smooth universal U-shape; a fortunate exact value is not an
accuracy certificate. Other expressions and scales can change the pattern.

Adding0.1s common bias shifted the synthetic mean from1.0 to1.1s while leaving
SEM0.008164965809277268s unchanged. Copying each of the four readings100 times
produced a formula output SEM0.0007079923254047893s, whose independent-sample
interpretation is invalid. More records are not necessarily more information.

For `[10^9+1,...,+4]`, naive raw-square subtraction produced sample variance0.0,
while centered two-pass calculation returned1.6666666666666667. The independently
computed rational oracle is5/3. At the declared speed inputs, estimate5m/s and
standard uncertainty0.07071067811865475m/s matched the hand derivation.

Independent review then found an unrelated intermediate-range defect in speed
propagation. It was corrected using `-(distance/time)*(u_time/time)` and tested
at tiny/huge scales; see [review and resolution](../../../research/quality/2026-10-22/new-unit-review.md).
The summary helper deliberately remains bounded by float accumulation/square
range: for example `fsum([1e308,1e308])` can overflow although a mean is
representable. A range exception must be handled by a caller; no arbitrary-scale
finite-input or interval-certified numerical claim is made.

Interpretation is limited to these inputs, equations and runtime. Follow-ups
should vary function, point scale, stochastic evaluation noise and sampling
correlation while preserving predictions and all failure rows.
