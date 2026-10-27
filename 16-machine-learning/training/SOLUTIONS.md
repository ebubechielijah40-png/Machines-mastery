# Checkable solutions and review rubric

1. u=x²+1=10; du/dx=6; dL/du=20, so dL/dx=120. Seed2 gives240.
2. μ=2, centered vector is all0, variance0; dividing0 by sqrt(10^-5) gives0.
   This guards the operation, not a claim of unit output variance.
3. Result[3,4]. Summing output gives gradients[1,1] into selected row1, zero
   into the other rows. The token index is discrete; it is not differentiated.
4. Inputs3×8; each projected array3×8, split into two3×4 heads. Head outputs
   concatenate to3×8 then mix through8×8. Each head has1+2+3=6 score pairs,
   total12. This excludes future pairs, not the number of projection operations.
5. p=[.4,.6]; loss=-ln(.6)≈.5108256238; gradients[.4,-.4]. Multiplying all
   exponentials by one common factor cancels from probabilities.
6. Affine composition yields A(Bx+c)+d=(AB)x+(Ac+d), another affine map.
   The XOR inequalities require b<0 and b>0. The reference nonlinear model's
   executed truth-table fit is in EXPERIMENTS; it uses all rows, not a held split.
7. Use `(L(p+h)-L(p-h))/(2h)` and compare the analytic gradient. Rebuild loss
   after each perturbation and do not call SGD. Very small h can expose rounding;
   one good h/input is not a universal proof. Tests sample named parameter indices
   in a smaller configuration; they do not check every possible model state.
8. Character encoding raises for absent symbols. The original byte-pair variant
   begins with all256 byte IDs, so UTF-8 roundtrips even when symbols are unseen.
   A token may span multiple bytes/characters. Neither count establishes accuracy.
9. A shared intermediate can retain contributions from an earlier reverse pass.
   Preserving that workspace double-counts old paths. Reset it, compute current
   adjoints, then optionally add saved old leaf adjoints only.
10. The script trains identity copying rather than next-token prediction. For
    sequence[0,1,2], assert inputs[0,1] and targets[1,2]. A future-mutation check
    alone cannot tell what labels the optimizer received.
11. For row E_i, sum every path contribution `dL/dx_t` for positions whose token
    equals i, including paths from those positions into later attention. Separate
    copied leaf Values would update copies unless their gradients were explicitly
    coalesced back into one shared row. Numeric equality is not parameter identity.
12. The retained experiment has train NLL about.01205 and clean held NLL.11487;
    after deliberately optimizing the held string, its NLL is about.01044.
    The latter no longer measures untouched data. Preserve your own measured
    output and versions; these are one synthetic run, not expected universal scores.
13. Assess20% hand/shape derivation,20% independently checked gradients,20%
    correct causality/token interface,20% actual controlled learning/evaluation,
    20% failure/limits/unaided reconstruction. A justified rejection is valid;
    fabricated training observations or mislabeled contaminated evaluation fail.
