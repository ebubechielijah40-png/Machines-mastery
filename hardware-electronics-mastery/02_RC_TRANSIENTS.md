# RC transients: build a dynamical model, then try to falsify it

**Scope:** one ideal resistor, one ideal capacitor and a constant voltage source;
then a finite-resistance measurement load and a finite-step computer model.
This unit is prepared instruction, not evidence of learner mastery. The numerical
experiment has been executed; a physical circuit has **NOT YET BEEN MEASURED**.

Read the [units](../foundations/mathematics/counting-and-units/README.md) and
[electrical quantities](../foundations/physics/electrical-quantities/README.md)
bridges first. The additional mathematics needed here is developed below.
Use [exercises](rc-transients/EXERCISES.md) before opening the
[hints](rc-transients/hints/README.md) and
[solutions](rc-transients/solutions/README.md). See the
[source map](rc-transients/SOURCES.md) for inspected sources and claim boundaries.

## 1. The engineering question

A sensor input is noisy, and a controller should respond gradually rather than
follow every abrupt change. A resistor alone gives an instantaneous proportional
relation in a lumped ideal model; it has no state with which to remember the
previous voltage. A capacitor adds state: charge accumulated on its plates.
The question becomes: after the source changes, how does the node move from its
previous value to its new value, and can the observation method change that motion?

A circuit predates the computer simulation. The simulation is a model of that
circuit, and has its own failure modes. A numerical oscillation is not automatically
evidence of a physical oscillation.

Our circuit is unambiguous without a diagram: connect a constant source's positive
terminal through a resistor `R` to an output node. Connect capacitor `C` between
that output node and the source's reference terminal. Measure output voltage `v`
relative to that reference. Current `i` is positive from source through resistor
into the capacitor's output-node plate. This sign convention matters when discharging.

| Quantity | Symbol | SI unit | Operational meaning |
| --- | --- | --- | --- |
| Charge on output-node plate | q | coulomb, C | integral of current into that plate |
| Current | i | ampere, A = C/s | charge transferred per second |
| Potential difference | v | volt, V = J/C | energy transfer per unit charge |
| Resistance | R | ohm, Ω = V/A | proportional voltage drop per current in this model |
| Capacitance | C | farad, F = C/V | charge change per voltage change for this linear capacitor |
| Time | t | second, s | elapsed time since source step |
| Stored energy | E | joule, J | energy of the ideal capacitor's electric field |

The symbol `C` for capacitance and the unit abbreviation `C` for coulomb have
different roles. Code uses `c_farad` to avoid that ambiguity.

## 2. From conservation to an equation of motion

Assume a linear, constant capacitor: `q = C v`. An increment `Δq` changes voltage
by `Δv = Δq/C`. Average current over a short time is `Δq/Δt`; the instantaneous
current is the limit as that time approaches zero:

\[
i = \frac{dq}{dt}= C\frac{dv}{dt}.
\]

Here `dv/dt` means slope in volts per second. It is a rate, not `v/t`: the latter
uses a line from the origin, while the former concerns change near the present
state. Constant `C` is necessary for this form. A voltage-dependent capacitor
requires a differential charge relation instead.

With no other branch at the output node, charge conservation requires resistor
current to equal capacitor current. Ohm's model gives `i = (V_s-v)/R`; loop-voltage
balance says source rise equals resistor drop plus capacitor voltage. Equating
currents gives the first-order ordinary differential equation (ODE):

\[
C\frac{dv}{dt}=\frac{V_s-v}{R},\qquad
\tau\frac{dv}{dt}+v=V_s,\qquad \tau=RC.
\]

Check dimensions before computing: `(V/A)(C/V)=C/A=s`. In particular, the
exponent `t/τ` below is dimensionless; `exp(-t)` is invalid if `t` carries seconds.

**State:** `v`; **input:** `V_s`; **parameters:** `R,C`; **output:** measured node
voltage (equal to `v` only for an ideal nonloading observer). An initial value
`v(0)=v_0` is required. An ODE alone describes many trajectories. Positive `R,C`
and a bounded source imply finite current; a finite current cannot transfer a
finite charge in zero time, so capacitor voltage is continuous at the step.
An ideal zero-resistance voltage source connected directly to a capacitor with
a different voltage is outside this finite-current model.

## 3. Solve it rather than memorize a charging formula

A just-in-time calculus bridge: an integral of a rate accumulates its tiny
contributions, defined as the limiting sum of rate×time over shrinking intervals.
It reverses differentiation for the continuous rates used here. Define
`ln(x)=integral from1 to x of1/u du` for positive dimensionless x, so its slope
is1/x. The exponential is its inverse. Differentiating `ln(exp(z))=z` by the
chain rule gives `exp'(z)/exp(z)=1`, hence `exp'(z)=exp(z)`. A negative exponent
therefore gives decay; `d exp(-t/τ)/dt=-exp(-t/τ)/τ`. For nonzero signed e,
`d ln|e|/de=1/e` on either side of zero. The derivation below treats zero
separately because dividing by e would otherwise discard a valid solution.

Let the remaining distance from equilibrium be `e(t)=v(t)-V_s`. For a constant
source, `de/dt = dv/dt`, so `de/dt = -e/τ`. If `e` is nonzero, divide by `e`
and integrate between initial and present states:

\[
\int_{e(0)}^{e(t)}\frac{1}{e}\,de
 =-\int_0^t\frac{1}{\tau}\,dt,
\quad
\ln\left|\frac{e(t)}{e(0)}\right|=-t/\tau.
\]

The exponential is the inverse of the natural logarithm: `ln(exp(x))=x`.
Exponentiating, preserving the initial sign, yields

\[
e(t)=e(0)e^{-t/\tau},\qquad
\boxed{v(t)=V_s+(v_0-V_s)e^{-t/\tau}}.
\]

If `v_0=V_s`, division by `e` was invalid, but the constant solution `v(t)=V_s`
satisfies the original equation directly. Include this case instead of losing
it during algebra. Verify the general solution independently: differentiating
it gives `(V_s-v)/τ`, and setting `t=0` gives `v_0`.

The familiar `V_s(1-exp(-t/τ))` is only the special case `v_0=0`. A precharged
capacitor may approach a lower source voltage from above. A source of zero
volts describes discharge through the resistor; `i` is then negative under our
charging sign convention.

For `t≥0`, `a=exp(-t/τ)` lies between zero and one, so `v=a v_0+(1-a)V_s` is a
weighted average. It remains within the interval between initial and final
voltages, moves monotonically, and does not overshoot. These are useful test
oracles derived independently of particular numerical answers. After one time
constant, the remaining distance is `exp(-1)≈0.367879` of the initial distance;
it has not reached its endpoint. An exact endpoint is approached only as time
grows without bound in this model.

## 4. Worked timing and energy example

Choose hypothetical parameters `V_s=3.3 V`, `R=10 kΩ=10,000 Ω`,
`C=10 μF=10×10^-6 F`, `v_0=0`. These are simulation inputs, not a component
selection or a measured circuit.

1. `τ=10,000×10×10^-6=0.1 s`. Unit conversion happens before multiplication.
2. Initially, `i(0)=3.3/10,000=0.00033 A=0.33 mA` and
   `dv/dt=i/C=33 V/s`. Current starts largest because the resistor sees the
   largest voltage difference.
3. At `t=0.1 s`, `v=3.3(1-exp(-1))≈2.085998 V`. Remaining resistor drop is
   `1.214002 V`, current is about `0.121400 mA`, and slope has decreased.
4. To find the first time at fraction `f` of supply, solve
   `f=1-exp(-t/τ)`: `t=-τ ln(1-f)` for `0<f<1`. At half supply,
   `t=0.1 ln 2≈0.0693147 s`. At 90%, `t≈0.230259 s`.
5. A 100% threshold has no finite solution; a threshold above supply is
   unreachable. Returning a negative or complex time would conceal a wrong model.

Energy provides a second consistency check. Work needed to add charge `dq` at
voltage `v=q/C` is `dE=v dq`. Integrating from zero to final charge `Q` gives
`E=Q²/(2C)=Cv²/2`. For initially uncharged charging to `V_s`, the source
transfers total charge `CV_s`, hence delivers `CV_s²`. The capacitor stores
half; the resistor dissipates the remaining half. In this example the limiting
energies are `108.9 μJ` from the source and `54.45 μJ` stored. The resistor's
loss equals `54.45 μJ`, irrespective of positive `R` when integrating the
ideal transient to infinite time. Increasing `R` reduces power and spreads
loss over longer time; it does not eliminate that loss. These statements
assume an ideal constant source, no leakage and `v_0=0`.

## 5. Instrument loading changes the system

A voltmeter with resistance `R_m` is a branch from output to reference, and a
probe may add capacitance `C_p`. Node-current balance becomes

\[
(C+C_p)\frac{dv}{dt}=\frac{V_s-v}{R}-\frac{v}{R_m}.
\]

Set slope to zero to get final voltage. Then collect the coefficient of `v`:

\[
V_\infty=V_s\frac{R_m}{R+R_m},\quad
R_{\rm eff}=\left(\frac1R+\frac1{R_m}\right)^{-1},\quad
\tau_{\rm loaded}=R_{\rm eff}(C+C_p).
\]

Use the same first-order solution with `V_∞` and `τ_loaded`. A finite meter
resistance lowers the final voltage and decreases effective resistance;
added probe capacitance increases the time constant. Their combined effect
cannot be guessed merely from the word "loading."

Example: `R=100 kΩ`, `C=1 μF`, `V_s=3.3 V`, hypothetical `R_m=1 MΩ`,
`C_p=100 pF`. Then `V_∞=3.0 V`, `R_eff≈90,909.09 Ω`,
`C_total=1.0001 μF`, and `τ_loaded≈0.0909182 s`, compared with the
unloaded `0.1 s`. Fitting the observed curve while falsely fixing its endpoint
to `3.3 V` biases the inferred time constant. The experiment script exposes
this using a synthetic sample and labels it accordingly. Real instrument
parameters must come from that instrument's specification and configuration;
none of these hypothetical values describe every meter or probe.

## 6. Uncertainty is not a decorative ± sign

Suppose only hypothetical tolerance bounds are known: `R` within ±1%, `C`
within ±10%, centered on the timing example. Monotonicity of `RC` gives exact
corner bounds under these assumptions:

\[
0.1(0.99)(0.90)\le\tau\le0.1(1.01)(1.10),
\quad \tau\in[0.0891,0.1111]\ {\rm s}.
\]

Bounds are not standard deviations. If, additionally, errors are independent
and uniformly distributed across those intervals, a uniform relative error
on `[-a,a]` has variance `a²/3`, obtained by integrating
`x²/(2a)` from `-a` to `a`. For small deviations,
`δτ≈C δR+R δC`. Squaring and averaging yields

\[
u^2(\tau)\approx C^2u^2(R)+R^2u^2(C)+2RC\,\mathrm{cov}(R,C).
\]

Under the stated independence assumption the covariance term is zero, and
`u(τ)/τ≈sqrt((0.01²+0.10²)/3)≈0.058023`, or `u(τ)≈0.0058023 s`.
This is a first-order model-based standard uncertainty, not an observed
repeatability result or an exact 95% confidence interval. Correlated errors,
nonuniform tolerance distributions, temperature drift and source/meter errors
require a different budget. NIST's inspected uncertainty guidance is mapped
in [SOURCES](rc-transients/SOURCES.md).

For threshold fraction `f`, `t=-τ ln(1-f)` has sensitivity
`dt/df=τ/(1-f)`. A voltage threshold near the asymptote is highly sensitive to
small uncertainty in the fraction and final voltage. Measuring the last few
percent is harder than simply printing more decimal places.

## 7. A computer model can violate a physical invariant

Approximate the slope by a forward difference over step `h`:

\[
\frac{v_{n+1}-v_n}{h}=\frac{V_s-v_n}{\tau},\qquad
v_{n+1}=v_n+\alpha(V_s-v_n),\quad \alpha=h/\tau.
\]

This is forward Euler. Each step uses the old state to predict the change.
For the timing example and `h=0.05 s`, the steps are `0 → 1.65 → 2.475 V`.
The last value is at `t=τ`, where the exact answer is `2.085998 V`. A plausible
smooth curve can still be quantitatively wrong.

Subtract equilibrium to get the numerical error recurrence
`e_(n+1)=(1-α)e_n`. This is an exact statement about this algorithm, distinct
from the continuous solution. Repeated substitution gives
`e_n=(1-α)^n e_0`:

| Step ratio | Consequence |
| --- | --- |
| `0<α≤1` | weighted-average steps; monotonic approach within physical range |
| `1<α<2` | alternating deviations that decay; numerical overshoot despite a nonoscillatory circuit |
| `α=2` | deviations alternate without decaying |
| `α>2` | deviation magnitude grows; artificial instability |

The boundary follows from `abs(1-α)<1`, not a memorized "small enough" rule.
Stability does not imply accuracy. At a fixed end time, halve `h` repeatedly
and check the change. Our experiment compares to an exact solution and tests
roughly first-order convergence, meaning error is approximately proportional
to `h` in the tested regime.

Backward Euler instead evaluates the slope at the new state:
`v_(n+1)=(v_n+αV_s)/(1+α)`. Its error multiplier is `1/(1+α)`;
positive steps preserve the range and damp deviations. Large steps still
lose the actual transient shape. An exact step for constant source multiplies
the old deviation by `exp(-h/τ)`. That expression is unavailable for many
nonlinear circuits, motivating numerical integration.

## 8. Runnable build and investigation

Python 3.10+ standard library only. From repository root:

```sh
python3 hardware-electronics-mastery/code/test_rc_lab.py
python3 hardware-electronics-mastery/code/run_rc_experiments.py > /tmp/rc-experiment.json
```

[Reference code](code/rc_lab.py) keeps the original `rc_charge` and
`time_to_threshold` APIs. `rc_response` adds arbitrary initial voltage;
`loaded_parameters` models the observer; `simulate` exposes three integration
methods. Finite values and positive `R,C` are checked before arithmetic.
`expm1` and `log1p` preserve precision for very small changes. A missing `R,C`
check in the original threshold helper allowed negative model time constants;
the updated tests reject those inputs. The model does not support zero or
negative `R,C`, impulses, time-varying source, nonlinear components or a
physical safety decision.

Build it in milestones rather than copying the reference:

1. Write the parameter/unit table and predicted signs before code. Deliver an
   ODE plus initial condition and explain why one state suffices.
2. Implement the exact solution and threshold inverse. Test initial condition,
   endpoint limit, signed discharge and an unreachable threshold. Deliver
   failing and passing tests, not only one printed answer.
3. Implement Euler directly from current and charge increments, then derive
   its multiplier. Predict instability before running the four step ratios.
4. Add the measurement branch by node-current balance. Deliver separate
   final-voltage and time-constant predictions and a synthetic trace.
5. Perform fixed-horizon step halving, energy accounting and a tolerance
   budget. Deliver raw outputs, units, interpretation and limitations.

Code review should explain every variable's unit and why tests use different
oracles: analytic answer, interval invariant, numerical derivative residual,
energy balance and convergence rate. The energy test integrates current/power
with midpoint quadrature; it is not another call that repeats the final
voltage formula and calls it independent confirmation.

For the controlled experiment design, executed output and remaining physical
limitations see [EXPERIMENT](rc-transients/EXPERIMENT.md). If a trajectory
oscillates, first examine `h/τ`, then source behavior and instrument setup.
Changing `R` and `C` while keeping their product fixed preserves the ideal
voltage trajectory but changes current and stored energy; equal waveforms
do not prove identical physical systems.

## 9. Transfer, boundaries and review

An exponential approach also appears in cooling and first-order feedback.
Transfer the mathematics only after identifying the corresponding conserved
quantity, state, resistance-like flow relation and assumptions. A neuron,
battery or motor cannot be declared a single RC circuit because its plot
looks smooth.

Physical extensions need source impedance, capacitor leakage/ESR, temperature
behavior, measurement bandwidth and sampling effects. Multiple independent
energy stores generally require more state variables; we have not taught or
validated an RLC resonator, transistor switching circuit or CPU timing model
here. The rest of the hardware domain remains incomplete.

**Reconstruction challenge:** close the lesson and reference. Given a source,
series resistor and capacitor with an initial voltage above the source,
derive the direction of current, exact response, energy change and Euler
stability boundary; implement them from a blank file. Then add a parallel
meter resistance and predict which observations would distinguish numerical
instability from a second physical energy store. Verify against the tests
only after writing your own predictions. Passing the reference tests is
preparation evidence, not proof of independent learner reconstruction.
