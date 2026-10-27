# Training/evaluation experiment — actual software observations

## Protocol before execution

Question: can the scratch differentiation/decoder pipeline optimize a declared
small objective, and do lower loss and more evaluation records imply better
external evidence? Hypotheses: nonlinear features fit XOR; the causal decoder
learns the repeated training direction; reversed transitions remain difficult;
optimizing the held set can lower its loss while invalidating held-out status;
a large unclipped learning rate can destabilize this particular run.

Controls: fixed synthetic strings, frozen character vocabulary, architecture,
initial seed11, example-choice seed13 and4 predicted tokens per string. The main
run changes parameters with180 SGD updates, learning rate.08 and global norm
clip1. A separate high-rate model uses the same initial seed and training strings
but rate3 without clipping for30 updates; because both rate/clipping differ,
this is a deliberately bad configuration comparison, not a clean estimate of
clipping's isolated causal effect. A follow-up must vary one at a time.

Instrumentation: exact mean next-token NLL, exp(NLL), XOR MSE, gradient norm,
training traces and single-run elapsed time; Python/platform in stdout. No
natural-language data, external model or GPU is involved. The raw source strings
and their hash are retained. Train/held exact-string intersection is checked,
which does not rule out all distributional dependence.

Procedure from the repository root:

```sh
python3 16-machine-learning/training/experiment_training.py
python3 -m unittest discover -s 16-machine-learning/training -v
python3 -m unittest discover -s 16-machine-learning/code -p test_autodiff.py -v
```

## Executed observations — 2026-10-22

[Raw JSON](evidence/training-2026-10-22.json) preserves the actual run and complete
settings. All figures below are **synthetic local observations**, not paper results.

| Measurement | Before | After declared clean training |
| --- | ---: | ---: |
| XOR MSE, all four training rows |1.03120903 |.00923594 |
| Decoder training NLL |1.19591595 |.01205321 |
| Held phase NLL |1.10188148 |.11487241 |
| Reversed-pattern shift NLL |1.05553418 |4.59271707 |

The548-parameter decoder generated `cabcabcabcabcabc` with top-k1 from c.
Clean held perplexity was about1.12173. Deliberately adding40 optimization steps
on the held string reduced its loss from.11487241 to.01044400; that later score
is explicitly contaminated. The high-rate/unclipped run's final training NLL
was5.53788783 after30 steps, worse than its initialization on this corpus.

Interpretation: the pipeline learns this tiny pattern and implements the
expected local information/gradient contracts. Improved training fit coexists
with much worse reversed-pattern loss. One held string does not estimate real
language competence or robust generalization. The high-rate run changes two
factors; alternatives include step size, clipping, seed and optimization dynamics.
The one-run timings are not a benchmark, and the vocabulary is only three symbols.

Follow-ups: multiple seeds, more independently generated held strings, overlapping-
window contamination checks, label-shift controls, separate rate/clipping sweeps,
position extrapolation and memory/time scaling. No unrun outcome is asserted.
