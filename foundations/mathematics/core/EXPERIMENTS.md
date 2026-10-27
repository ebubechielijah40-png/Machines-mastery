# Investigating sensitivity, steps and accumulation

Read the chapters and write predictions before opening the retained results.
The question is whether an algorithm can produce a tiny equation residual while
its solution is highly sensitive to input changes, and whether a locally correct
gradient guarantees a useful finite update.

## E1 — Nearly dependent equations

Hypothesis: with A=[[1,1],[1,1+δ]] and a perturbation ε to the second component
of b=A(1,1), the solution displacement grows as |ε/δ|. A residual against the
perturbed equations can remain tiny. Hold ε=10⁻⁷, solver and nominal solution
fixed; vary δ from10⁻¹ to10⁻⁹. Record actual float coefficients, both right-hand
sides, solution, residual infinity norm and displacement from(1,1).

The independent reference is the algebraic real solution(1−ε/δ,1+ε/δ).
Do not label its small disagreement with floating output a failed proof: the
decimal constants and perturbation are themselves rounded. The experiment
separates a data perturbation, coefficient rounding, solver error and measurement
accuracy, none of which are interchangeable.

## E2 — A correct gradient with an unstable step

Use L=½(x₁²+4x₂²), x₀=(1,1), zero target,30 updates. Vary only α among
.1,.4,.5,.6. Instrument every state and loss. The chapter's multipliers1−α
and1−4α predict decay, a boundary oscillation and divergence. No optimizer
adaptation, random batch, stochastic measurement or learning-rate search is used.

An alternative explanation for growth in a general model would be an incorrect
gradient or numeric overflow. Here every-coordinate finite-difference tests
and the independent diagonal recurrence make the step-size mechanism testable.
This does not establish a stability bound for arbitrary neural models.

## E3 — Quadrature error under step halving

Approximate∫₀¹t²dt with n=4,8,16,32,64 equal trapezoids. Hold the interval,
function and summation method fixed. Measure signed error relative to1/3;
the exact quadratic error1/(6n²) is an independent rational oracle. Predict
error reduction by4 for each doubling of n. Follow-up: use a function with a
corner, then an unresolved narrow pulse. A rule's error order needs smoothness
and adequate sampling; the result for t² cannot establish those conditions.

## Procedure and executed record

From repository root:

```bash
python3 -m unittest discover -s foundations/mathematics/core -v
python3 foundations/mathematics/core/experiment.py --output foundations/mathematics/core/evidence/your-run.json
```

The retained [observed run](evidence/observed-2026-10-23.json) was actually executed;
it records Python/platform, UTC time, all selected inputs and raw traces. It is
mathematical simulation, not a physical observation or a performance benchmark.

| Executed observation | Interpretation within this model |
| --- | --- |
| δ=10⁻⁹ gave displacement≈100 with perturbed residual≈2.22×10⁻¹⁵ | A small residual alone did not bound forward sensitivity |
| α=.4 loss2.5→≈1.22×10⁻¹³ after30 updates | Both coordinate multipliers have magnitude below1 |
| α=.5 ended at loss2.0; α=.6 at≈1.17×10⁹ | Boundary and growing second-coordinate modes were observed |
| Trapezoid error≈.0104167 at n=4 and≈.00260417 at n=8 | This smooth quadratic followed the derived factor-of-four error reduction |

Follow-up experiments should vary one mechanism at a time: uniformly rescale
the equations, perturb both columns instead of b, use coordinates with different
units, or introduce rounding at every update. Retain unsuccessful runs. State
which hypothesis the instrument actually tests before drawing a conclusion.
