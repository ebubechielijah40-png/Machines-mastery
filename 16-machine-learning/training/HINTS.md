# Hints

1. Name the shared square and add its two paths before multiplying outer effects.
2. Center first. The numerator is zero; the denominator is sqrt(ε).
3. One-hot multiplication selects. Lookup must return shared parameters.
4. Each head has width4; row t has t+1 permitted positions.
5. Differentiate log-sum-exp; subtract1 on the selected coordinate.
6. Add inequalities from the equal-sign rows, then the unequal-sign rows.
7. Rebuild the graph for every perturbed evaluation and restore every parameter.
8. Freeze merges/token IDs learned from training; do not retrain during evaluation.
9. Internal adjoints are a workspace; leaf accumulation is a separate API decision.
10. Check input/target offsets directly; low loss can be achieved by a wrong task.
11. Different positions are multiple computation paths into one parameter node.
12. Separate optimization progress from fresh statistical evidence.
13. Preserve dimensions/information boundaries before measuring quality.
