# Hints

1. Every term of the dynamic equation must have unit U.
2. Preserve the sign of the gain before dividing.
3. A residual needs an error model before it becomes a rejection criterion.
4. Subtract readings first, then divide by gain. The offset cancels in a difference.
5. Complete the characteristic square; differentiate the proposed response at0.
6. Multiply by q'. At rest, viscous loss is initially zero.
7. Expand `(z-λ)(z-conj(λ))` and compare its sum/product terms.
8. Keep fractions until the last conversion. The radius is sqrt(−C_d).
9. Set both partial derivatives to zero. Inspect the determinant.
10. Each row of the design matrix is proportional to every other row.
11. Divide by a, then restore the nonzero drive term.
12. Remove the sine weight by choosing v0=−αq0.
13. A longer record on the same grid still adds multiples of2π to the phase.
14. The recurrence assumes zero-drive coordinates relative to the correct origin.
15. Count endpoints. Neighboring states approach each other as h decreases.
16. A refusal is observable behavior, not an inconvenient missing result.
17. Accumulate five sums once; the present implementation also stores samples.
18. c is inverse capacitance. Charge rate is current.
19. Compare outputs to the oracle on changed initial conditions, not to copied code.
20. A fitting equation cannot supply an unknown device's voltage rating or pinout.
