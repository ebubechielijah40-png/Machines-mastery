# Build a neural learner from a scalar computation graph

A program can implement a fixed rule; a learned model instead adjusts numeric
parameters against an explicit objective. This build asks when that adjustment
actually changes behavior, how to check its derivatives, and why fitting data
is different from predicting new data. The result is a scratch reverse-mode
engine and a nonlinear two-input learner, followed by a connected next-token
model. Python3.10+ standard library is sufficient. No downloaded model, GPU or
external service is needed.

**Developed bounded project:** original instruction, executable reference,
independent tests, executed synthetic experiments and separated assessments are
supplied. Large tensor kernels, robust statistical generalization, distributed
training and serving are outside this project. Its artifacts do not complete
the whole machine-learning domain.

## Derive before implementing

Read [prerequisites](PREREQUISITES.md), then [the graph/XOR teaching unit](../../16-machine-learning/training/README.md#1-the-graph-remembers-operations-not-just-answers).
Write the derivative of `(x*x+1)^2` without running code. At x=3, first x*x=9,
then u=10 and L=100. The outer derivative20 multiplies the inner derivative6,
giving120. Both paths through x*x contribute; overwriting a contribution loses
half the result.

Now attempt to fit the XOR truth table using one affine score. Equal-sign inputs
require b<0 and unequal-sign inputs require b>0 after adding their inequalities.
The contradiction motivates nonlinear hidden features. A hidden layer without
an intervening nonlinearity remains an affine map and cannot remove it.

Architecture: input rows → shared scalar parameters → tanh hidden features →
tanh output → mean squared loss → reverse graph traversal → finite SGD update.
A fresh graph is built after every parameter update. Training state consists of
parameters and the chosen example order; gradient buffers are not observations.

## Milestones and learner tasks

| Stage | Build/derive before reading the reference | Observable evidence |
| --- | --- | --- |
| A0 | Trace values/local derivatives on paper | L=100 and derivative120 at x=3; list both shared paths |
| A1 | Implement addition, product, power and tanh with parent links | Independent hand expressions and central differences agree |
| A2 | Visit the graph in reverse topological order | Branch gradients add; a second backward pass does not reuse intermediate adjoints |
| A3 | Write affine XOR inequalities, then add four nonlinear hidden units | Explain impossibility before reporting a fit |
| A4 | Average all four squared errors and apply SGD | Actual saved loss trace decreases for declared settings; report every row |
| A5 | Deliberately use a wrong gradient or oversized step | A targeted test catches the gradient bug; the bad setting has a recorded outcome |
| A6 | Freeze model/data/settings and reconstruct | Explain the parameter-to-loss path without reference code |
| A7 | Transfer to token embeddings and a causal decoder | Continue the [decoder project](../ai-autodiff-transformer/README.md) with shifted labels and a held-set boundary |

After your design attempt, use [hints](HINTS.md). The runnable references are
[autodiff.py](../../16-machine-learning/code/autodiff.py) and
[tiny_models.py](../../16-machine-learning/training/tiny_models.py); the latter
contains the MLP and optimizer. References are complete solutions, so preserve
your own attempt before opening them. [Checkpoint details](CHECKPOINTS.md)
explain each acceptance rule. [Tests](TESTS.md) and [experiments](EXPERIMENTS.md)
provide exact commands, failure cases and observed results.

## Deliver, assess and reconstruct

Submit your graph engine, MLP, independent derivative checks, hand proof/trace,
actual optimization log, failure-and-repair explanation and declared limits.
Use [the separate exercise set](../../16-machine-learning/training/EXERCISES.md);
its solutions are linked only after the attempt. Rubric: graph/gradient
reasoning25%, independent checks25%, model/objective derivation20%, evidence and
interpretation20%, unaided transfer10%. A passing reference test is evidence
about behavior; it is not evidence of unaided learner reconstruction.

Close the code and rebuild a three-hidden-unit version with a different seed.
Predict which parameter dimensions change, derive the new parameter count, and
explain why this changes optimization opportunities without guaranteeing a fit.
Then replace one row's target and identify which gradients change before running.
[Production boundaries](PRODUCTION.md) and [limits](LIMITS.md) prevent turning
this bounded demonstration into unsupported claims.

## Family mechanisms before larger abstractions

Use [logistic/CNN/RNN and explicit generative builds](../../16-machine-learning/model-families/README.md) to derive likelihood and shared-parameter gradients before the decoder milestones. Deliver one held-distribution failure and an independent gradient/count oracle for each selected mechanism.
