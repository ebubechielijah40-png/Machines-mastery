# Executed optimization experiment and learner investigations

Question: do nonlinear hidden features plus correct reverse-mode derivatives
optimize XOR under a fully declared setting? Prediction: four hidden tanh units
can fit the four training rows, while an affine threshold cannot separate them.
Controls: inputs(-1,-1),(-1,1),(1,-1),(1,1); targets-1,+1,+1,-1; hidden width4;
seed7; mean squared error; SGD.1;300 updates. Instrumentation is exact model loss,
row predictions, Python/platform and the saved procedure.

Run from the repository root:

```sh
python3 16-machine-learning/training/experiment_training.py
```

[Actual raw run](../../16-machine-learning/training/evidence/training-2026-10-22.json):
MSE1.03120903 → .00923594; predictions approximately[-.8847,.9023,.8934,-.9476].
All four signs fit. All four rows were trained, so this supports a particular
optimization result, not held-out generalization. The same script separately
executes decoder clean/shifted/contaminated evaluation; its
[protocol and interpretation](../../16-machine-learning/training/EXPERIMENTS.md)
explain why apparently better held loss can invalidate its own test status.

Unrun extensions: hold seed/data/width/steps fixed and vary only learning rate;
repeat each setting with multiple seeds; compare hidden widths1,2,4,8; replace a
local gradient with a known wrong rule and observe which tests catch it. Before
each run write a hypothesis, controlled variables, exact command, measurements,
interpretation, alternative explanations and a follow-up. A single noisy elapsed
time does not measure deployment latency or training throughput reliably.
