# From a rate law to a defensible trajectory

A simulator must turn a statement about change **now** into a prediction about
the future. It has finite computation and incomplete information about the
world. This unit derives that transformation, implements it with scalar loops,
and constructs a smooth input that an adaptive integrator misses completely.

Study [functions](../core/01_ALGEBRA_FUNCTIONS.md),
[vectors](../core/03_VECTORS_MAPS.md),
[derivatives/integrals](../core/04_CALCULUS_OPTIMIZATION.md),
[units](../counting-and-units/README.md) and
[Python loops/tests](../../../02-programming/python-entry/README.md) first.
Entry check: explain why integrating metres/second over seconds gives metres;
evaluate a vector-valued function; explain a derivative as local change; write
and independently test a loop. No differential-equations course is assumed.

## 1. Rate law, state and initial value

The state contains the quantities needed, with a stated model and inputs, to
predict their instantaneous rates. An ordinary differential equation (ODE)
uses one independent variable; here it is time. Write an initial-value problem
as \(\dot y=f(t,y),\ y(t_0)=y_0\). The unknown is a function y(t), while y₀
is a known starting value. A numerical trajectory stores approximate states at
selected times. It does not store the unknown continuous function itself.

Before numerical iteration, one can use geometry (tangent/direction fields),
algebraic equilibrium and symbolic integration on solvable models. Numerical
methods retain the rate law but approximate the integral between sample times.
They allow more complicated models; they also introduce a new error mechanism.

Consider a cart with m=2kg, applied force F=6N, linear drag coefficient
b=4N·s/m, initial velocity0. Newton's equation gives

\[
m\dot v=F-bv,\qquad \dot v=3-2v,\qquad v(0)=0.
\]

The coefficient3 has units m/s²;2 has units s⁻¹. Position, if required, is
another state with \(\dot x=v\). Acceleration is a derived rate here.
Specifying the force law without initial velocity leaves many trajectories.
Assumptions include constant parameters and force, linear drag and no contact
changes. A more accurate integrator cannot repair an incorrect drag law.

The equilibrium velocity is \(v_*=F/b=1.5\,\mathrm{m/s}\), and the time
constant is \(\tau=m/b=.5\,\mathrm s\). Subtract v*: u=v-v* obeys
\(\dot u=-u/\tau\). The product rule gives
\(d(e^{t/\tau}u)/dt=0\), so

\[
v(t)=v_*+(v_0-v_*)e^{-t/\tau}.
\]

Thus v(.5)=1.5(1-e⁻¹)≈.9481808382m/s. This formula is an independent oracle
for this model. It predicts approach from below for these initial conditions,
and exposes an unphysical sign or a gross numerical overshoot.

## 2. Derive Euler and Heun from an integral

The exact identity is
\(y(t+h)=y(t)+\int_t^{t+h} f(s,y(s))\,ds\). Replace the varying integrand
by its known value at the interval's left endpoint:

\[
y_{n+1}=y_n+h f(t_n,y_n).
\]

This is forward Euler, a tangent approximation. Repeating it means subsequent
derivatives are evaluated at approximate states. For the cart,h=.25s:

| Step(s) | Start velocity(m/s) | Start acceleration(m/s²) | Euler end velocity(m/s) |
| --- | --- | --- | --- |
| 0→.25 | 0 | 3 | 0+.25×3=.75 |
| .25→.5 | .75 | 1.5 | .75+.25×1.5=1.125 |

Acceleration decreases during each interval, so keeping its larger initial
value overestimates the velocity increment. The exact .94818 is below1.125.

Heun predicts \(p=y_n+h f(t_n,y_n)\), evaluates the endpoint slope there,
and averages its two slope estimates:

\[
y_{n+1}=y_n+\tfrac h2[f(t_n,y_n)+f(t_n+h,p)].
\]

First prediction .75 gives endpoint slope1.5, so corrected velocity is
.25(3+1.5)/2=.5625. The next start slope is1.875, prediction1.03125,
endpoint slope.9375, and corrected velocity
.5625+.25(1.875+.9375)/2=.9140625. The predictor is temporary; it is not
the accepted state or another time step. Heun costs two field evaluations
per step, versus Euler's one.

## 3. Local error, global error and their assumptions

Along a sufficiently smooth exact solution, Taylor's formula yields
\(y(t+h)=y(t)+hy'(t)+h^2y''(t)/2+O(h^3)\). Euler omits a one-step state
defect of orderh² **when started at the exact state**. On a fixed interval,
there are aboutT/h steps. Under error-propagation bounds the total becomes
orderh; smaller one-step error does not by itself bound accumulated error.

Here is a concrete bound. Suppose
\(\|f(t,u)-f(t,v)\|\le L\|u-v\|\) in the relevant state region and
\(\|y''(t)\|\le M\). The first condition, Lipschitz continuity in state,
bounds how much changing a state can change its rate. Euler's error obeys

\[
e_{n+1}\le(1+hL)e_n+Mh^2/2.
\]

Starting exactly and summing the geometric series gives, forL>0,

\[
e_N\le\frac{Mh}{2L}[(1+hL)^N-1]
\le\frac{Mh}{2L}(e^{LT}-1),\qquad T=Nh.
\]

ForL=0 the sum isMTh/2. Initial error contributes(1+hL)ᴺe₀. These statements
need a solution and bounds over the interval where the estimates are used.
They exclude accumulated rounding and uncertain physical parameters. Refining
the mesh cannot remove an incorrect initial condition or calibration bias.

Heun matches the quadratic Taylor terms: expanding its predicted endpoint
slope gives f+h(f_t+f_y f)+O(h²), so its increment is
hf+h²(f_t+f_y f)/2+O(h³), matching y''=f_t+f_y f. Thus its local state
defect is orderh³ and its global error is orderh² with appropriate propagation
bounds. Partial derivatives describe changing one input while holding the
others fixed; f_y f is matrix-vector multiplication for vector state.

## 4. Four-stage RK4 and a worked trace

Classical RK4 constructs four rate estimates:

\[
\begin{aligned}
k_1&=f(t,y),&k_2&=f(t+h/2,y+hk_1/2),\\
k_3&=f(t+h/2,y+hk_2/2),&k_4&=f(t+h,y+hk_3),\\
y_+&=y+h(k_1+2k_2+2k_3+k_4)/6.
\end{aligned}
\]

For y'=-y,y=1,h=.5: k₁=-1; the first midpoint state.75 givesk₂=-.75;
the next midpoint state.8125 givesk₃=-.8125; predicted endpoint.59375
givesk₄=-.59375. The final state is.6067708333333, compared with
e⁻⁰·⁵≈.6065306597126. Every stage is constructed from the same original y.

For y'=λy, putz=hλ and substitute the stages algebraically to obtain
\(y_+=R(z)y\), where
\(R(z)=1+z+z^2/2+z^3/6+z^4/24\). This matches the exponential through
degree4. For a derivative depending only on time, RK4 reduces to Simpson
quadrature. Those calculations explain the independent linear/polynomial
test oracles; they are not a proof of every nonlinear RK4 order condition.
General RK4 has local order5 and global order4 under suitable smoothness and
stability conditions; the full mixed-derivative proof remains outside this unit.

## 5. Stability differs from physical constraints

For decay y'=-ky,k>0, Euler's multiplier is1-hk. Shrinkage in magnitude needs
|1-hk|<1, or0<hk<2. Nonnegative states also requirehk≤1. Athk=1.5 the
trajectory alternates sign while shrinking; athk=2 its magnitude stays constant;
athk=3 it doubles. A negative concentration or energy needs more scrutiny than
a small magnitude alone. For complexλ, the relevant test is|R(hλ)|≤1;
the real decay interval is not a universal vector-system stability test.

Backward Euler uses the unknown endpoint in its rate:
\(y_+=y-hky_+\), hence \(y_+=y/(1+hk)\). It stays positive and decays
for every positiveh, but a very large step poorly resolves the transient.
Our `decay_step(...,implicit=True)` solves only this scalar linear model.
A general nonlinear implicit step needs another equation solver, its derivative
information and its own stopping/failure policy.

In y'₁=-y₁,y'₂=-1000y₂ with initial(1,1e-6), the tiny fast state is physically
almost gone while its explicit stability restriction remainsh<.002s. Resolving
the slow behavior may not require such a small step; maintaining explicit
stability does. This is a concrete stiffness mechanism. Removing the fast state
requires a justified reduced model, especially if coupling or constraints make
that transient important. A small initial amplitude alone is insufficient.

## 6. Conservation as an independent diagnostic

An unforced, undamped oscillator obeys x'=v,v'=-ω²x. Assume **m=1kg**,
position in metres, velocity in m/s and angular frequency in s⁻¹. Then
\(E=m(v^2+\omega^2x^2)/2\) is measured in joules. The continuous derivative
is m(vv'+ω²xx')=0. That identity supplies a check separate from a plot's shape.

Forward Euler updates both coordinates from the old state. Expanding squares
cancels the cross terms and gives
\(E_+=(1+h^2\omega^2)E\). Therefore afterN steps,
\(E_N=E_0(1+h^2\omega^2)^N\): the discretization creates energy.

Velocity-first symplectic Euler instead applies
\(v_+=v-h\omega^2x\), then \(x_+=x+hv_+\). Its matrix is
\(A=\begin{pmatrix}1-h^2\omega^2&h\\-h\omega^2&1\end{pmatrix}\), with
determinant1. Substitution shows it preserves the modified quadratic

\[
\widetilde E=\tfrac12(v^2+\omega^2x^2-h\omega^2xv)
=\tfrac12[(v-h\omega^2x/2)^2+\omega^2(1-h^2\omega^2/4)x^2].
\]

Forω>0 and0<hω<2 this quadratic is positive definite, hence its constant
level sets bound both coordinates. It differs from physical energy. The matrix
trace is2-h²ω², so its oscillatory eigenvalues have angleθ satisfying
cosθ=1-h²ω²/2. Generallyθ≠hω: bounded energy can coexist with accumulating
phase error. Athω=2 the quadratic loses positive definiteness. Damping,
forcing, varyingω or varyingh invalidates this fixed-step invariant as stated.

## 7. Adaptation and its precise limitation

Compare one RK4 step of sizeh with two steps of sizeh/2. If the same leading
local-error coefficientC describes the interval, the coarse error isCh⁵ and
the two-half-step error is2C(h/2)⁵=Ch⁵/16. Their difference is about15Ch⁵/16,
so|fine-coarse|/15 estimates the fine result's error. We accept the fine result
without extrapolation. This assumes an informative smooth local asymptotic
regime; agreement can also result from missing the input altogether.

Normalize componenti by \(a_i+r\max(|y_{old,i}|,|y_{fine,i}|)\). Absolute
toleranceaᵢ has that component's units; relative tolerancer is dimensionless.
Use the maximum component ratio. Changing metres to millimetres multiplies
both that coordinate/rate and its absolute tolerance by1000. An unscaled
mixture of positions, temperatures and currents would make units choose the mesh.

For nonzero normalized errore, our controller proposes
h_new=h·clip(.9e⁻¹⁄⁵,.2,5); ife=0 it grows by5. Rejected attempts retain the old
state/time; all attempts cost12 field calls. Minimum-step, call and attempt
budgets, finite-value checks and representable-time checks expose failed solves.
They do not interrupt a callback or iterator that fails to return.

Construct a decisive counterexample. On a=.1,b=.15, letu=(t-a)/(b-a), and put

\[
f(t,y)=\begin{cases}12012\,u^6(1-u)^6/(b-a),&a<t<b,\\0,&\text{otherwise.}\end{cases}
\]

This pulse and its first5 derivatives match zero at its endpoints. A single
adaptive attempt from0 to1 samples only0,.25,.5,.75,1. All slopes are0,
so both paths return0 with estimated error0. But polynomial expansion gives
\(\int_0^1u^6(1-u)^6du=\sum_{j=0}^6(-1)^j\binom6j/(7+j)=1/12012\).
Withy(0)=0 the exact final state is **1**. Smoothness alone does not make a
finite sampling set observe every feature. Supplying the known support interval
to the same solver is a useful controlled contrast; it is not automatic detection.

## 8. A rate equation need not define a unique finite future

For y'=2√y,y(0)=0, any waiting timec≥0 gives a solution that stays0 untilc,
then follows(t-c)². Both derivatives match0 atc. The square root fails a local
Lipschitz bound there. Euler remaining0 selects a valid solution without proving
uniqueness. Continuity in time/state together with a local state-Lipschitz
condition underlies a standard local existence/uniqueness theorem; this example
shows why its hypotheses matter, rather than proving the whole theorem.

For y'=y²,y(0)=1, separating variables givesy=1/(1-t), valid before blowup
att=1. A finite numerical output att=1.1 cannot establish continuation of the
same classical solution. Budget exhaustion, divergence and model breakdown
must remain different findings in an experiment log.

## Build and assess the mechanism

Python3.10+ standard library suffices. From repository root:

```bash
python3 -m unittest discover -s foundations/mathematics/initial-value-evidence -v
python3 foundations/mathematics/initial-value-evidence/experiment.py
```

Build five milestones in a learner-owned directory: derive the cart oracle;
implement Euler plus an exact rational one-step test; add Heun/RK4 and mesh
refinement; expose stiff/oscillator failures; finally implement adaptive rejection,
scaled tolerances and resource guards, then challenge it with the pulse.
Try [exercises](EXERCISES.md) before [hints](HINTS.md) and [solutions](SOLUTIONS.md).
[Actual experiment evidence](EXPERIMENTS.md) preserves predictions, controls,
raw outputs, interpretation and limits. [Sources](SOURCES.md) records inspected
versions and boundaries; no external tutorial is needed for these builds.

Deliver a units/model declaration, intermediate handwritten trace, your code,
independent oracle, raw experiments and a reconstruction without notes. Rubric:
derivation/units25%, ordinary/boundary implementation25%, independent experiment
and interpretation25%, transfer/reconstruction/limits25%. A program agreeing
with itself supplies no independent-oracle evidence.

The code accepts forward finite spans,1–8 state components and bounded work.
It reads at most9 iterable components before rejecting dimension excess;
booleans, numeric strings, nonfinite states and dimension changes are errors.
It retains every accepted state, using memory proportional to accepted steps;
a streaming production solver needs another output policy. Callback exceptions
propagate. Trusted local callbacks and budgets do not constitute a hostile-code
sandbox, hard realtime controller or physical safety argument.

Transfer to [RC circuits](../../../hardware-electronics-mastery/02_RC_TRANSIENTS.md)
and [motor control](../../../17-embedded-robotics/control-path/README.md) by stating
their states/rate laws before swapping an integrator. Keep sampling delay,
measurement uncertainty and model error separate. General implicit solvers,
certified error bounds, PDEs, DAEs, boundary-value problems and robust event
localization remain explicitly unfinished broader curriculum.
