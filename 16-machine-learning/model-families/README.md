# Why model families behave differently

A decreasing loss is not an explanation of what a learner has learned. Two
systems can fit the same examples while responding differently to a translated
pattern, a delayed input or a new data distribution. This unit builds those
contrasts through mechanisms small enough to derive completely.

There are five actual mechanisms here: regularized binary logistic regression,
a circular convolutional classifier, a scalar recurrent classifier, a finite
bigram generator and one-dimensional Gaussian-mixture expectation maximization.
All numerical loops and reverse derivatives are original Python standard-library
implementations. The existing [autodiff](../03_AUTODIFF_BACKPROP.md) and
[trained decoder](../training/README.md) remain complementary builds. This unit
supplies missing model-family foundations; it does not complete deep learning,
modern vision, gated recurrent models, VAEs, GANs, diffusion or production AI.

## Prerequisites and progression

Begin with [Python execution](../../02-programming/python-entry/README.md),
[functions and algebra](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md),
[vectors and maps](../../foundations/mathematics/core/03_VECTORS_MAPS.md),
[chain derivatives/optimization](../../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md)
and [conditional probability](../../foundations/statistics/probability-inference/README.md).
Before using a new operation, work its numerical trace below. Source papers and
books verify the explanations; leaving the repository is not required for the
basic builds.

| Study in order | Construct | Exit evidence |
| --- | --- | --- |
| [1. Binary learning and evaluation](01_BINARY_LEARNING.md) | Conditional likelihood, logistic score, gradient, regularization, train-only transform, metrics and leakage | Derive the zero-weight gradient and reproduce a shortcut failure |
| [2. Local patterns and convolution](02_LOCAL_PATTERNS.md) | 2D patch products, shape rules, shared 1D kernels, nonlinearity, pooling and reverse derivatives | Build an independent correlation oracle and prove the exact circular shift property |
| [3. Recurrence and memory](03_RECURRENCE_MEMORY.md) | State update, unrolled graph, all parameter/input derivatives and temporal products | Trace a two-step state and derive the first-input gradient; break retention with a new input |
| [4. Probability models and generation](04_GENERATIVE_MODELS.md) | Chain factorization, bigram counts, smoothing, latent mixture/density, EM and sampling | Compute an exact sequence likelihood and a mixture update; expose memory and initialization failures |

## Run the actual code

From the repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/model-families -v
python3 16-machine-learning/model-families/experiment.py
```

The experiment prints a new JSON observation. Preserve it under a new filename
when comparing to [the executed run](evidence/observed-2026-10-23.json). Seeds,
parameters, costs and source-file hashes are included. It needs no downloads,
accounts, GPU or third-party package. [The protocol and results](EXPERIMENTS.md)
distinguish finite synthetic observations from claims about natural data.

The files are deliberately inspectable:

- [discriminative.py](discriminative.py) contains analytic logistic/CNN/RNN
  derivatives and atomic returned updates. Parameters are immutable tuples.
- [generative.py](generative.py) contains count tables, normalized mixtures,
  explicit Box–Muller sampling and constrained EM updates.
- [test_families.py](test_families.py) checks every model parameter against central
  differences, plus exact patch/count oracles, shift properties and numerical
  rejection paths. Numerical agreement is a diagnostic, not a general proof.

## Build before consulting the reference

Use [the 24 exercises](EXERCISES.md), then [hints](HINTS.md) only as needed.
[Solutions](SOLUTIONS.md) supply independent calculations and reference contracts.
Build in four milestones: logistic likelihood, a shared kernel, an unrolled
recurrence, then a probabilistic generator. At each milestone, retain a failing
prediction, an independent oracle and a reconstruction from memory.

An acceptable final investigation declares a data-generating process, freezes
train/evaluation access before fitting, tests the model's structural assumptions,
and explains a failure it actually observed. The evaluation rubric awards one
point each for correct derivation, independent test, controlled experiment,
reproducible evidence and honest limitations, for each of the four milestones.
A runnable copied reference without those explanations earns no derivation or
reconstruction evidence. It does not establish learner mastery.

## Engineering boundary

These are bounded educational computations, not a serving system. Vectors are
limited to256 entries, feature columns to64, batches to4096 and real teaching
scalars to magnitude1e6. Models reject malformed/nonfinite inputs; recurrent
adjoint overflow produces a controlled error rather than a silent update.
Gradients, preprocessing state, RNG seeds, alphabet order and stopping rules are
part of a reproducible model. Input validation, finite tests and a seed do not
provide service isolation, authenticated model provenance or data privacy.
[SOURCES](SOURCES.md) records selected inspected originals and copyright limits.
