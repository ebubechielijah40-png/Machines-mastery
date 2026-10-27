# Attention assessment — save attempts before opening solutions

Prerequisites and worked derivations: [DERIVATION.md](DERIVATION.md).
[Hints](HINTS.md) and [solutions](SOLUTIONS.md) are separate on purpose.

1. **Basic:** calculate `[2,-1] dot [3,4]`; state the result's shape.
2. **Basic:** for scores `[0,ln(3)]`, calculate weights and their sum.
3. **Basic:** X is 5-by-3, W_Q/W_K are 3-by-2, W_V is 3-by-4. Give the shapes of Q, K, V, the displayed causal weight matrix, and O.
4. **Basic:** which key positions are allowed for queries 0, 1, 2? What happens at an empty sequence?
5. **Basic:** predict outputs when all permitted values equal `[7,-2]`.
6. **Application:** reconstruct the scalar backward worked example with values changed to `[4,8]`; compute q/K/V gradients for `L=o`.
7. **Application:** zero W_K for any three tokens. Predict the last output before executing; include a rectangular W_V.
8. **Application:** implement a second cache test using head width 1 and value width 3; compare every incremental output with a full prefix.
9. **Reasoning:** someone claims square-root scaling prevents concentrated weights for arbitrary large d. Construct a counterexample and explain the failed assumption.
10. **Reasoning:** show algebraically why score gradients sum to zero, and explain why this is consistent with a common score offset.
11. **Challenge:** derive gradients with respect to one projection matrix `W_Q` when `q=xW_Q`. Use finite differences on every entry; explain why this is still not a complete training system.
12. **Experimental:** use the exact supplied seed/procedure, then repeat using seeds 1, 2 and 3. State a prediction, change only one variable, record raw outputs and explain why exact small-input equality does not establish all-input correctness.
13. **Transfer:** a sensor predictor embeds a whole day's mean into every hourly input. Does causal attention guarantee that the 10:00 prediction cannot use 18:00 readings? Draw the dependency and propose a corrected feature pipeline and test.
14. **From memory:** close reference code, implement projection, stable softmax, one-query attention, triangular causal attention and a K/V cache. Produce one hand-computed oracle, a future-perturbation test and a cache reset test before comparison.

Evaluation: independently correct arithmetic and shapes (1–5); derivation plus
execution evidence (6–8); explicit assumptions and counterexample (9–10);
finite-difference evidence (11); honest measurements and limits (12); whole
pipeline information reasoning (13); fresh implementation and explanation (14).
Passing these tasks is learner evidence only when the learner actually submits
attempts. Reference tests do not establish learner mastery.
