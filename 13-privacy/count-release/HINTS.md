# Hints after attempting the derivation

1. Removal can subtract zero or one; addition can add zero or one.
2. Bound the change in the sum for one person's whole contribution, then use Δ/ε.
3. Integrate each exponential branch and solve for z. Endpoint uniforms make log(0) appear.
4. Use `(|t-11|-|t-10|)/b`; tails are enough to attain the extremum.
5. Variance of an average of independent terms is variance of one divided by count. Each .1 release has much larger noise than the ε=1 release.
6. Conditional on a known seed, there is no unknown noise to the attacker. Identical correlated noises can cancel in differences.
7. Privacy-safe post-processing may depend on public parameters and prior released values, not unaccounted sensitive input.
8. Passing a grid or statistical moment check does not cover every measurable event or finite-precision support gap.
9. The object has neither persistent identity nor synchronized shared state.
