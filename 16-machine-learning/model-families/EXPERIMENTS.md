# Controlled model-family experiments

## Question, controls and procedure

Does a mechanism's structural assumption explain both a successful fit and a
failure? Predict each row below before executing `python3 16-machine-learning/model-families/experiment.py`
from the root. Run the seventeen tests first. No input download or framework is
used. `experiment.py` records parameters, seeds, source hashes, loss checkpoints,
wall times and metrics. The retained [JSON](evidence/observed-2026-10-23.json)
is an actual run on2026-10-23, not reported paper results. Timings are single-host
observations; optimization comparisons require repeated, interleaved measurements.

| Question | Controlled procedure | Hypothesis |
| --- | --- | --- |
| Shortcut dependence | Fixed train seed421, held seed422;80 training and128 held examples;500 steps,rate.15; flip only the target-derived shortcut at evaluation | A classifier may trust the shortcut and fail under its reversal |
| Local pattern transfer | Six length12 circular rings at positions0–2;18 held rotations;800 steps,rate.3; compare five-parameter max-pooled shared kernel to13-parameter flat linear model | Exact circular invariance can transfer a learned detector |
| State retention | Six first-sign sequences of lengths2,4,8;900 steps,rate.15; evaluate blanks to128 and four late distractors separately | Blank retention need not imply resistance to new inputs |
| Mixture initialization |160 train draws seed601 and512 held seed602; generating weights.4/.6, means−2/+2,SD.35/.55;40 EM steps,floor.01 | Symmetric initialization can remain a poor symmetric density |
| Generation memory | Eight balanced first/last-character documents;alphabet(a,b,x),α.1; fixed seed per sample | Equal last-character transition rows discard initial-character information |

Clipping bounds are5 for logistic/CNN and1 for recurrence. All training examples
are reused at each full-batch step. Neither the structural held rotations nor two
sequences at each blank length count as a natural-data benchmark.

## Actual observations and interpretation

The shortcut classifier reached training NLL.000821 and IID held accuracy1;
reversing the shortcut gave accuracy0 and NLL6.91918. The stable-feature-only
control reached held accuracy.75. This shows a failure under an explicitly
constructed distribution change. It does not identify a causal feature in real
data. Train-only and train-plus-held scaling means differ; that observation alone
does not measure metric inflation from preprocessing leakage.

The circular CNN reached accuracy1 on the18 held rings, with positive logit
range0 across rotations. The flat linear baseline reached1 in training but1/3
held. This finite comparison supports the local assumptions used here. Exact
invariance also follows by reindexing the circular feature sum or maximum; neither
result promises invariance with zero padding, subsampling or natural images.

The recurrence retained both signs through128 blank positions, but late
distractor accuracy was.5. The initialized first-input derivative diminished to
approximately−1.160e−39 by length128. Forward retention in the trained state
and backward sensitivity at initialization are separate measured quantities.

Separated mixture initialization gave training NLL1.327974 and held1.290657;
identical initialization gave2.116407 and2.120529. The largest observed
likelihood decrease was0 in both runs. Lowering the floor on repeated identical
data from.01 to1e−12 improved NLL from−1.383647 to−12.896572 while learning
nothing about population variation. Component indices have no identifiable name.

The bigram's training NLL including end markers was.761740 nats per prediction.
Conditional on the next character after x being a or b, each probability was.5.
Saved samples include early termination and a mismatched final character. Samples
illustrate the table; the table, rather than anecdotal sample selection, proves
the memory limitation.

## Alternative explanations and follow-up

Architecture, optimizer and initialization all differ between some comparisons;
this is not a controlled ranking of all model families. A flat nonlinear model
could learn adjacency with more data. A different RNN initialization could fail
even the simple blank task. More mixture restarts might find better density, but
selecting restarts on the held set would contaminate evaluation.

For follow-up, freeze a new training/validation/test split; vary one of kernel
padding, distractor magnitude, sequence length or mixture initialization; repeat
seeds; report distributions of losses, calibration and cost. Retain failures and
all attempted configurations. None of these local synthetic runs reproduces the
historical source papers or establishes production safety, privacy or reliability.
