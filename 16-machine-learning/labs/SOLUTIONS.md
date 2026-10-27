# Solutions and independent checks

1. `2*3 + (-1)*4 = 2`, a scalar.
2. `[1/4,3/4]`, sum one.
3. Q and K: 5-by-2; V: 5-by-4; weights: 5-by-5; O: 5-by-4.
4. `[0]`, `[0,1]`, `[0,1,2]`. This implementation rejects an empty sequence
   rather than inventing a distribution over no keys.
5. Every output is `[7,-2]` because the permitted weights sum to one.
6. Weights remain `[1/4,3/4]`; `o=7`; `r=[4,8]`; `t=[-3/4,3/4]`.
   Thus `dq=(3/4)ln(3)`, `dK=[-3/4,3/4]`, `dV=[1/4,3/4]`.
7. At query i, weights are `1/(i+1)` over permitted positions. For raw tokens
   `[1,0]`, `[0,1]`, `[1,1]` and W_V `[[2],[4]]`, values are `[2],[4],[6]`;
   the final output is `[4]`. W_Q can be any compatible finite matrix.
8. Example: use tokens `[1],[2],[-1]`, W_Q=W_K=`[[1]]`, W_V=`[[1,2,3]]`.
   Compare each cached output with the last full-prefix output. Tolerance
   should be explicit; do not only check final dimensions.
9. Let q and key 0 be all ones, key 1 all zeros. Scaled scores are `[sqrt(d),0]`.
   The first probability tends to one. The independence/zero-mean random
   coordinate assumptions are absent.
10. `sum_j t_j = sum_j a_j r_j - mean*sum_j a_j = mean-mean = 0`.
    Perturbing all scores by delta therefore has zero directional derivative.
11. If upstream query gradient is h, then `dL/dW_ij=x_i*h_j`, an outer product.
    A full sequence sums contributions over positions. If a matrix is shared
    by different paths, all path contributions must accumulate. Finite
    differences of a chosen scalar loss check these entries, but training
    also needs gradients through other operations, an objective, parameters,
    optimization and independent evaluation data.
12. Supply your own measurements. The committed reference observation is in
    [evidence](evidence/2026-10-22-attention.json); it is not your result.
    A handful of seeds does not cover all inputs or prove a security property.
13. No. The mean already contains future readings. Compute a prefix-only or
    prior-window feature and fit normalization statistics on training data
    only. Change readings after 10:00; the full 10:00 input/features/output
    must stay fixed. Test upstream transformations as well as attention.
14. No canonical copied solution establishes reconstruction. Compare the
    fresh implementation against hand arithmetic and the Decimal/finite
    difference tests, then explain any discrepancies.
