# From energy and torque to a sampled motor controller

A wheel does not obey a requested speed merely because software stores that
number. The controller can command a voltage; current generates torque; torque
changes motion; a sensor reports an imperfect history of that motion. This unit
builds the complete, bounded chain. All parameters and observations are synthetic.
No motor, driver or physical robot was energized or validated.

## Prerequisites and progression

Study [quantities and units](../../foundations/mathematics/counting-and-units/README.md),
[change, numerical error and uncertainty](../../foundations/mathematics/change-error-and-evidence/README.md)
and [electrical quantities](../../foundations/physics/electrical-quantities/README.md)
first. The [mechanics bridge](../../foundations/physics/MOTION_ENERGY.md) introduces
force, torque, inertia and energy. [RC dynamics](../../hardware-electronics-mastery/02_RC_TRANSIENTS.md)
teaches a one-state differential equation and why an explicit numerical step can
create behavior absent from a physical model. Here two coupled energy stores add
an electrical state and a mechanical state. Chemistry/materials are not needed
to execute the ideal model; they are needed to choose real insulation, magnets,
bearings and thermal limits. Those material assumptions are not hidden guarantees.

## 1. Choose a boundary and derive the plant

Choose positive shaft rotation and positive current such that positive current
produces positive motor torque. We model a rigid shaft, constant magnetic field,
linear resistance/inductance and viscous friction. The states are current i in A,
angular speed ω in rad/s and angle θ in rad. Commands are voltage v in V and
external load torque τ_L in N·m, positive when opposing positive rotation.

The electrical loop obeys

\[
v=Ri+L\dot i+k_e\omega.
\]

The resistor dissipates power; the inductor stores magnetic energy; rotation
creates opposing back EMF. This equation is a declared lumped model, not a
semiconductor commutation model. Newton's rotational equation gives

\[
J\dot\omega=k_t i-b\omega-\tau_L,\qquad\dot\theta=\omega.
\]

J has units kg·m², b has units N·m·s/rad, k_t has units N·m/A and k_e has units
V·s/rad. Thus every electrical term is V and every mechanical term is N·m.
Treat radians consistently as the SI dimensionless angle unit. In coherent SI
for this ideal conversion model, k_t and k_e have equal numerical values k.
The [source map](SOURCES.md) gives the inspected modeling sources and caveats.

One useful internal invariant is an energy *balance*, not constant stored energy:

\[
E=\tfrac12Li^2+\tfrac12J\omega^2,\qquad
\dot E=vi-Ri^2-b\omega^2-\tau_L\omega.
\]

To derive it, multiply the electrical equation by i and the mechanical equation
by ω. Their k iω conversion terms cancel; use d(i²)/dt=2i di/dt and the analogous
speed identity. Positive electrical input can increase stored energy, do load
work and become heat. With zero supply/load and nonnegative R,b, stored energy
cannot increase in the continuous model. An unstable integrator need not preserve
that inequality; test an algorithm separately from the equations.

**Worked initial state:** hypothetical J=.02, b=.02, R=2, L=.02, k=.1. At i=1 A,
ω=3 rad/s, v=6 V and τ_L=.01 N·m, di/dt=(6−2−.3)/.02=185 A/s and
dω/dt=(.1−.06−.01)/.02=1.5 rad/s². Stored-energy rate is
`.02*1*185 + .02*3*1.5 = 3.79 W`. Independently, `6−2−.18−.03=3.79 W`.
The .3 V back EMF is not an unexplained extra resistor; it is the electrical
signature of energy conversion into rotation.

At steady state with zero external load, the mechanical equation gives i=bω/k
(for k>0). Substitute this into v=Ri+kω and collect the terms in ω:

\[
\omega_\infty=\frac{k v}{Rb+k^2}.
\]

For 6 V, numerator .6 and denominator .05 give 12 rad/s. A demanded 20 rad/s is
unreachable under this voltage constraint. Increasing software gains cannot
create the missing steady-state power. With load, the numerator becomes
`k v − R τ_L`; a large opposing load can reverse the steady-state speed in this
linear model. Real stiction and current limits may invalidate that prediction.

## 2. A gearbox trades speed for torque

Let G=ω_motor/ω_output>0; G=4 is a four-to-one speed reduction. An ideal gear
has equal input/output power, so τ_output=G τ_motor while ω_output=ω_motor/G.
For output inertia J_L, rewrite its kinetic energy:

\[
\tfrac12J_L(\omega_m/G)^2=\tfrac12(J_L/G^2)\omega_m^2.
\]

The reflected inertia at the motor is J_L/G², not J_L/G. Example: .8 kg·m²
behind G=4 adds .05 kg·m² to motor-side inertia. A gearbox can increase output
torque without increasing power. Efficiency, backlash, elastic shafts, bearing
loads and tooth failure require additional states/constraints. The helper
`reflected_inertia` tests precisely this ideal energy relation; it does not size
a physical gearbox.

## 3. Derive the controller memory

Define measured-speed error e=r−y. A proportional command K_p e corrects current
error but generally needs nonzero error to provide the voltage that maintains a
loaded motion. Introduce a state z with dz/dt=e, so a persistent error changes
future command. A sampled rectangle approximation is z_next=z+e Δt.

Our discrete PID command is

\[
u^*=K_p e+K_i z-K_d\widehat{\dot y},\qquad
u=\max(-U,\min(U,u^*)).
\]

For speed control, K_p has units V·s/rad, K_i V/rad and K_d V·s²/rad.
Differentiation is on measurement, not target: a step in desired speed does not
create an artificial impulse in the derivative term. The measured derivative
uses `(y_n−y_(n−1))/Δt`, then a first-order filter with coefficient
`Δt/(τ_d+Δt)`. Smaller Δt does not eliminate measurement noise; differencing
amplifies high-frequency noise. The first derivative is explicitly zero because
no preceding measurement exists. That initialization is a contract, not a
measurement of actual acceleration.

A clipped output does not itself stop z from growing. Suppose the requested
speed is unreachable and e stays positive. Without anti-windup, z grows even
though u is already at U. When the target falls, the stored positive integral
may keep the actuator driving forward until negative error unwinds it.

The reference uses **conditional integration**: form a candidate integral. If
its requested command is above +U and the integral increment pushes still
farther positive, discard that increment; similarly at −U. Permit increments
that help leave saturation. This is a simple bounded strategy, not a universal
proof of closed-loop stability. It assumes the modeled saturation is the actual
actuator input and that K_i is nonnegative. Hidden inner-loop limits, motor
current protection or another feedforward input need a revised strategy.

**Worked failure:** K_p=2, K_i=1, U=3 V, e=10 rad/s, Δt=.01 s. P alone requests
20 V. After 100 samples, an unbounded integrator adds 10 rad, requesting 30 V;
the actuator still receives only 3 V. Conditional integration holds z=0 in
this case. Both outputs saturate, but their future stored states differ.

## 4. Sensors define what the loop can correct

The synthetic sensor adds a fixed bias, Gaussian pseudorandom noise and optional
quantization, then returns a sample delayed by an integer number of sample
intervals. It holds the first sample as prehistory; it does not invent old motion.
Quantization uses nearest multiples with Python's round-to-even tie rule.

If y=ω+c and the integral drives measured error to zero, it drives ω toward r−c,
not r. The loop cannot infer an unknown calibration offset from this one sensor.
A second calibrated reference or an explicit observation model is necessary.
With delay d samples, controller input refers to earlier state; simply increasing
gain may worsen the phase relationship. A particular delay can nevertheless
improve a selected transient metric accidentally. A claim that delay always
worsens every metric is too strong.

Real sensor records also need timestamps, units, saturation and missing-value
rules. Our simulator has no dropped packets, encoder wraparound, scheduler jitter,
watchdog, driver dead-time or electrical current protection. Do not turn this
reference directly into hardware firmware.

## 5. Runnable implementation, experiment and debugging

`control_lab.py` implements the two-state electromechanical equations plus angle,
a fourth-order Runge–Kutta step, controller memory and sensor pipeline. RK4 samples
four slopes within a time step; it is not adaptive and can still fail on stiff
or poorly sampled dynamics. The electrical time scale is approximately L/R=.01 s
here, so the reference Δt=.002 s is tested with step refinement. Reference and
refined sample control loops are distinct discrete controllers; their changes
are not purely an RK4 truncation study.

From the repository root:

```sh
python3 -m unittest discover -s 17-embedded-robotics/control-path -v
python3 17-embedded-robotics/control-path/experiment.py
```

**Question:** what happens when actuator capacity, integrator memory, sensing
and target feasibility conflict? **Prediction:** conditional integration should
reduce the recovery error after an unreachable command changes to a reachable
one. A biased sensor should leave a true-state offset. **Controls:** same motor,
voltage bound, gains, initial state and target schedule. **Changes:** anti-windup,
100-sample delay, .5 rad/s bias, or .05 rad/s noise plus .1 rad/s quantization.
**Measurements:** true speed, measured speed, integral state, saturation fraction
and integral of absolute true-speed error after t=4 s. **Actual outputs:**
[evidence/control-experiment.json](evidence/control-experiment.json), with full
parameters/platform and every-50-step trace; [tests](evidence/tests.txt).

Observed in that run, conditional integration ended near 2.00753 rad/s versus
7.51264 without it, with post-switch absolute-error integrals about 3.65797 and
38.7934 rad. The biased-sensor case ended near 1.50734 rad/s. The delayed-sensor
case slightly improved the chosen post-switch integral to about 3.44923 rad;
this does **not** establish that delay is beneficial in general. It motivates
changing gains, delay and horizon separately before generalizing.

Tests use hand derivatives, an independent power-balance identity, decoupled
analytic RL/mechanical exponentials, sign symmetry, gear energy, a saturation
counterexample and delayed-sample vectors. A passing tuned loop alone would be
weak validation. Follow-ups: inject load steps, change the gain sign, halve the
sample interval, add supply sag and model thermal resistance changes. Record
all failed predictions. No actual hardware performance is claimed.

Attempt [EXERCISES](EXERCISES.md) before [HINTS](HINTS.md) or
[SOLUTIONS](SOLUTIONS.md), then build [the guided controller](../../projects-guided/p13-robot-controller/README.md).
