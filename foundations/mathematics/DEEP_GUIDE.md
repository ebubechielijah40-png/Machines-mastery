# Mathematics: derive the model before running it

Begin with [counting and units](counting-and-units/README.md), then use the
[connected core](core/README.md). The earlier repeated exercise templates have
been replaced by the concrete mechanisms below. They supply prerequisites for
bounded projects; they do not certify the entire mathematics curriculum.

| Order | Internal instruction | Observable exit task |
| --- | --- | --- |
| 1 | [Quantities, ratios and units](counting-and-units/README.md) | Convert unlike time units, distinguish a count from a duration, state what was measured |
| 2 | [Algebra and functions](core/01_ALGEBRA_FUNCTIONS.md) | Derive a byte constraint and sensor calibration; explain composition, domains and nonunique inverses |
| 3 | [Finite representations](finite-representations/README.md) | Derive positional value, unsigned capacity and modular wraparound |
| 4 | [Logic, proof and counting](core/02_PROOFS_DISCRETE.md) | Prove an invariant, termination and an induction; distinguish causal from total order |
| 4a | [Coordinates, angles and complex arithmetic](core/GEOMETRY_COMPLEX.md) | Derive a rotation, modulus and reciprocal before using complex amplitudes |
| 5 | [Vectors and maps](core/03_VECTORS_MAPS.md) | Construct a basis map, compose it, solve equations and demonstrate sensitivity |
| 6 | [Change, finite error and measurement](change-error-and-evidence/README.md) | Diagnose cancellation, centered variance, bias and covariance assumptions |
| 7 | [Calculus, accumulation and updates](core/04_CALCULUS_OPTIMIZATION.md) | Derive a gradient, a quadratic stability bound and an Euler state transition |
| 8 | [Finite probability and inference](../statistics/probability-inference/README.md) | Derive conditioning, binomial counts and coverage; refute a false iid assumption |

For example, the same multiplier explains several different models. A physical
decay equation dx/dt=−kx gives Euler multiplier 1−hk; a scalar quadratic loss
with curvature λ gives gradient-update multiplier 1−αλ. Derive each from its
own governing equation before connecting them. Matching formulas do not give
identical causes, units or validation methods. A controller also has limits,
delay and sensors; an optimizer also has finite data and evaluation questions.

A matrix with nearly dependent columns can give a tiny residual despite a large
change in the inferred state. In the core experiment a fixed 10⁻⁷ perturbation
yields solution displacement proportional to 1/δ. Test shape, units, numerical
range and input sensitivity before interpreting a solver's output as evidence.

The core has [specific exercises](core/EXERCISES.md), separate hints/solutions,
scalar-loop implementations and [executed experiments](core/EXPERIMENTS.md).
The numerical and probability units have their own independent oracles and
assessments. Reconstruct at least one mechanism without its reference code,
then change an assumption and predict the failure before running it.

Still requiring full instructional development: geometry/trigonometry beyond
the new bounded bridge, eigen/singular-value algorithms, general optimization,
sparse numerical methods, rigorous analysis, broad differential equations and
PDEs. Those subjects are not silently assumed to complete the exercises above.
