# Hints after a design attempt

1. Mean is the middle value; sample variance divides squared deviations by two. Add the correction to the mean, not to its variance.
2. There are n(n-1)/2 unordered pairs. Divide all covariance terms by n² after expanding the sum.
3. A restricted wire format deliberately rules out alternate spellings and implicit unit conversion. Changing it requires a new interpretation contract.
4. Sum pairwise squared differences over ordered pairs, then divide by `2*n*(n-1)`.
5. Drift, correlated noise, hysteresis, quantization and changing ambient conditions can violate assumptions. Synthetic Gaussian code does not measure these effects.
6. A content hash has no secret. Compare with authenticated origin and externally trusted checkpoints in p09.
7. Keep the public units/schema separate from the scientific independence model.
8. Sequence numbers alone do not measure time. Repeated standards, timestamps, randomized order and independent instruments can supply discriminating evidence.
