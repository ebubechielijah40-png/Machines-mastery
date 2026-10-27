# From local change to optimization and dynamics

Prerequisites: [functions](01_ALGEBRA_FUNCTIONS.md), [vectors/maps](03_VECTORS_MAPS.md)
and [change/error](../change-error-and-evidence/README.md). The last unit derives
the derivative from a shrinking secant and explains why finite differences can
fail. This chapter connects that idea to composed programs, fitting and physical
state evolution. Derivatives are local model properties, not truth detectors.

## 1. Rules follow from first-order changes

Differentiability at x means f(x+h)=f(x)+f'(x)h+r(h), where r(h)/h tends to zero
as nonzero h tends to zero. This is a locally accurate linear approximation;
it is stronger than continuity. For f(x)=x², expansion gives f'(x)=2x and
r(h)=h², whose ratio to h tends to zero. For |x| at zero, no single slope
approximates both directions.

Adding expansions gives `(f+g)'=f'+g'`. Multiplying gives
`(f+f'h+small)(g+g'h+small)=fg+(f'g+fg')h+terms smaller than h`, so the product
rule is f'g+fg'. It is not f'g': that would omit two first-order paths.

For h(x)=f(g(x)), the inside changes by g'(x)Δx to first order. The outside
changes by f'(g(x)) times that inside change. Therefore
`h'(x)=f'(g(x))*g'(x)` under the differentiability assumptions. The inspected
OpenStax chain-rule statement supplies those assumptions. Do not simply cancel
“d” symbols as fractions; the local approximation explains why the formula
also holds when g'(x)=0 and direct division by an inside change would be invalid.

Worked program: u=3x+1, v=u², loss=(v−4)². At x=1, u=4,v=16,loss=144.
Local slopes are du/dx=3, dv/du=8, dloss/dv=24. Their product is576.
An error in u affects loss through both uses of u in u*u; a graph must sum
contributions from shared paths. Reverse-mode automatic differentiation carries
an upstream derivative backward along each operation and adds those contributions.
It does not estimate a derivative from perturbed evaluations, so finite-difference
checks provide a useful independent diagnostic, subject to their rounding limits.

## 2. Several inputs produce a gradient or Jacobian

For f:R^n→R, the partial derivative∂f/∂x_j varies coordinate j while holding
others fixed. Collect the partials in a gradient∇f. For a differentiable f,
`f(x+Δx)≈f(x)+∇f(x)ᵀΔx`. This approximation defines a directional slope.
The gradient's units depend on each input: a loss per metre is not interchangeable
with the same numeric loss per second.

For a vector output, collect local coefficients in a Jacobian J with one row
per output and one column per input. Composition multiplies Jacobians in the
same interface order as linear maps. For a linear layer y=Ax, J=A. An upstream
loss derivative gᵀ over outputs gives input derivative Aᵀg; this is why a
transpose appears in backpropagation. It is not an inverse layer or reconstruction
of the original input.

For L=½||Ax−b||², let r=Ax−b. A perturbation Δx changes residual by AΔx.
Expand the square: L(x+Δx)=L(x)+rᵀAΔx+½||AΔx||². The first-order coefficient
is Aᵀr, so∇L=Aᵀ(Ax−b). This derives the gradient used in `linear.py` and
the stationarity equations in the previous chapter. It is valid for this real
quadratic; complex differentiation requires a separate convention.

## 3. A descent direction does not choose a safe step

Move by Δx=−α∇L. The first-order loss change is−α||∇L||², nonpositive for
α>0. But the ignored quadratic term can dominate at a large step. A gradient
is a direction and local rate, not permission to jump arbitrarily far.

Take L(x)=½λ(x−x*)² with λ>0. Gradient descent gives
`x_next=x−αλ(x−x*)`. Error e=x−x* therefore evolves as
`e_next=(1−αλ)e`. Consequently convergence requires|1−αλ|<1, or0<α<2/λ.
At αλ=1 the quadratic reaches its minimum in one step; between1 and2 the
error alternates while shrinking; at2 it alternates without decaying; above2
it grows. The experiment intentionally tests these regimes.

For A=diag(1,2), L=½||Ax−b||² has independent curvatures1 and4. One shared
step must satisfy both constraints, so α<1/2. A step0.6 can improve the
first coordinate while making the second diverge. Different feature scales
therefore affect optimization behavior even for a convex objective. For a general
quadratic the largest curvature eigenvalue controls this fixed-step bound;
the diagonal example derives that fact for its particular coordinates, rather
than requiring an unwritten eigendecomposition algorithm.

Stationarity∇L=0 is not always a minimum. f(x)=−x² has derivative zero at0,
a maximum. f(x)=x³ also has derivative zero at0 without a local minimum.
A nonconvex neural training loss requires evaluation beyond decreasing its
training objective: held-out errors, data leakage, shift, variance across seeds
and computational cost are separate observations.

## 4. Integrals accumulate locally defined contributions

Suppose a constant current I flows for duration T. Charge transferred is IT.
For changing current divide time into narrow intervals and sum current×duration;
the integral∫I(t)dt is the limit of these sums when that limit exists. Units
multiply: A*s=C. Integrating position would yield m*s, not velocity.

For f(t)=t² on[0,1], n equal right-end rectangles have area
`(1/n)Σ(k/n)² = n(n+1)(2n+1)/(6n³)`, tending to1/3. A trapezoid uses the
average endpoint height on each interval; this treats the function as locally
linear. It has a different approximation error. The reference experiment
compares its area to the independently known1/3, retaining errors for step halving.

The fundamental theorem connects rate and accumulation: if F'=f and f is
continuous on the interval,∫_a^b f(t)dt=F(b)−F(a). This is the bridge used by
energy `dE=F dx` or capacitor charge `dq=C dv`. It does not authorize swapping
integrals/derivatives for arbitrary discontinuous or nonintegrable data without
checking conditions. A sampled finite sum also cannot reveal everything that
occurred between samples.

## 5. Differential equations require state and an initial condition

Equation dx/dt=−kx describes rate as a function of present state. For k>0
and x(0)=x₀, x(t)=x₀exp(−kt) satisfies both rate and initial condition.
Without x₀, many trajectories satisfy the equation. The exponent kt must be
dimensionless, so k has units1/s if t is seconds.

Euler updates x_next=x+h*f(x,t), using the current slope for one step.
For this decay its multiplier is1−hk, reproducing the same stability boundary
as the scalar descent example. This is a mathematical connection, not a claim
that optimization and physical decay have identical causes. The
[RC lesson](../../../hardware-electronics-mastery/02_RC_TRANSIENTS.md) derives
its state equation from charge conservation; physical/control units derive
motion from force and torque instead.

Adding a second-order mechanical equation introduces position and velocity as
two state coordinates: d(position)/dt=velocity, d(velocity)/dt=force/mass.
Discretizing them, choosing integration order and adding delayed feedback can
change stability. An apparently smooth graph alone cannot validate a physical
machine or a control policy.

## 6. Executable assessment and handoff

Run core tests, inspect every-coordinate gradient checks, and perform the
[experiments](EXPERIMENTS.md) before opening [solutions](SOLUTIONS.md).
Attempt C1–C8 in [EXERCISES](EXERCISES.md). A complete reconstruction explains
the graph of local derivatives, derives the step bound and distinguishes model,
floating arithmetic and empirical generalization failures.

Then enter the trained-neural-model build, RC/control path or statistical
inference unit. Each depends on a different part of this chapter; none requires
pretending that this introduction is an entire real-analysis or optimization course.
