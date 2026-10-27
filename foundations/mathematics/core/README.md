# Equations, proofs, transformations and change

This is a connected foundational unit, with original instruction and executable
mechanisms. Begin with [counting and units](../counting-and-units/README.md).
No calculus, matrix package or proof course is assumed at entry. You should be
able to count finite objects, add and multiply whole numbers, and distinguish
a measured duration from its numerical value in a unit.

| Order | Study | Evidence to produce before moving on |
| --- | --- | --- |
| 1 | [Algebra and functions](01_ALGEBRA_FUNCTIONS.md) | Solve a byte budget, derive a calibration and state its domain; A1–A8 |
| 2 | [Proofs and discrete models](02_PROOFS_DISCRETE.md) | Explain an invariant and a termination argument separately; D1–D8 |
| 3a | [Coordinates, angles and complex arithmetic](GEOMETRY_COMPLEX.md) | Derive a modulus, reciprocal and rotation; G1–G6 |
| 3 | [Vectors and maps](03_VECTORS_MAPS.md) | Construct a matrix from basis images, solve a system, diagnose a misleading small residual; L1–L8 |
| 4 | [Change, rounding and measurement](../change-error-and-evidence/README.md) | Explain finite-difference cancellation and random variation versus bias |
| 5 | [Calculus and optimization](04_CALCULUS_OPTIMIZATION.md) | Derive a chain rule computation and a stable update bound; C1–C8 |

The [exercises](EXERCISES.md), [hints](HINTS.md) and [solutions](SOLUTIONS.md)
are separate so an initial attempt can be independent. Solutions explain the
reasoning and boundary cases; a matching final number alone is insufficient.

## Implement the mechanisms

Python 3.10 or later, standard library only. From the repository root:

```bash
python3 -m unittest discover -s foundations/mathematics/core -v
python3 foundations/mathematics/core/experiment.py --output foundations/mathematics/core/evidence/your-run.json
```

Read [discrete.py](discrete.py) after deriving Euclid's invariant, then rebuild
it without looking. Read [linear.py](linear.py) after constructing the basis-map
example. It uses scalar loops for products, row scaling and partial pivoting
for a small real system, and an explicitly derived quadratic gradient. A library
solver can later replace these loops for practical work, but cannot replace
understanding of the interface and failure modes.

The tests use alternative structures: exact rational two-by-two formulas,
basis-column reconstruction, finite differences, the defining page inequality,
and independently checked Bézout identities. They exercise dimensions, complex
inner products, singularity, scaling and deliberately unstable updates.

[Experiment instructions](EXPERIMENTS.md) distinguish predictions from retained
executed observations. [Sources](SOURCES.md) records precisely inspected scopes;
none of the linked books or their prose is bundled in this unit.

## Exit task and transfer

Without opening the code, reconstruct `page_count`, extended Euclid, matrix
composition and the gradient of half the squared residual. Explain one input
each must reject, why each loop terminates, and one thing its passing tests do
not establish. Then change the dimensions of the sensor-mixing example and
predict its output shape before running it.

For algorithms, continue to the [graph release](../../../algorithmic-problem-solving/topics/graphs/LESSON.md).
For physical systems, continue to [motion and energy](../../physics/MOTION_ENERGY.md)
and [RC dynamics](../../../hardware-electronics-mastery/02_RC_TRANSIENTS.md).
For inference, use [finite probability](../../statistics/probability-inference/README.md).
For learning systems, carry the gradient derivation into
[automatic differentiation](../../../16-machine-learning/code/autodiff.py)
and the [tiny trainable model](../../../16-machine-learning/training/README.md).
The complex inner product prepares the [quantum statevector unit](../../../20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md).

This bounded unit does not teach a full real-analysis course, general constrained
optimization, sparse factorizations, eigensolvers, measure theory or numerical
PDEs. Those remain distinct curriculum gaps, not implicit prerequisites the
learner is expected to find elsewhere to complete these exercises.

For the rate-law handoff, continue through [initial-value evidence](../initial-value-evidence/README.md).
Derive Euler/Heun/RK4, separate local error from stability and physical
constraints, then investigate a stiff state, oscillator energy/phase and a
smooth pulse missed by adaptive sampling. The unit supplies exact oracles,
budgeted code,24 separated exercises and actual numerical observations.
