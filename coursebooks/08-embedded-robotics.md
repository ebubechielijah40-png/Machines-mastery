# Embedded control: why a stored command does not guarantee motion

A robot loop observes, computes and acts, repeatedly. It works only when the
units, reference frames, actuator limits and timing agree across that boundary.
This coursebook develops one connected motor-speed loop deeply; it does not
claim complete robot kinematics, planning or hardware deployment.

## 1. Motion and energy before software tuning

Study [units](../foundations/mathematics/counting-and-units/README.md),
[change/error](../foundations/mathematics/change-error-and-evidence/README.md),
[electrical quantities](../foundations/physics/electrical-quantities/README.md),
[RC transients](../hardware-electronics-mastery/02_RC_TRANSIENTS.md) and
[motion/energy](../foundations/physics/MOTION_ENERGY.md) before the implementation.
Each adds a mechanism needed by the next. The relevant local sources are mapped
in the [control unit](../17-embedded-robotics/control-path/SOURCES.md).

For constant mass, net force m a changes speed; for a rigid fixed-axis rotor,
net torque J dω/dt changes angular speed. Inertia J=Σm_i r_i² has unitkg·m².
Mass farther from the axis costs more torque for the same acceleration. A.2m
perpendicular lever under10N gives2N·m; at3rad/s it transfers6W. The same force
through the axis produces no torque. Torque and energy share dimensional factors
but play different roles; work requires angular displacement.

An ideal reduction G=ω_motor/ω_output trades speed for torque. From equal power,
τ_output=Gτ_motor; from equal kinetic energy, output inertia reflected to the motor
is J_load/G². A.8kg·m² load behind G4 therefore contributes.05kg·m² motor-side.
Neither relation includes backlash, elasticity, loss or tooth stress. Those are
missing physical mechanisms, not reasons to conceal units inside a generic gain.

## 2. Two coupled energy stores define the plant

Let i be current,ω speed,θ angle. Positive current gives positive torque; positive
load torque opposes positive motion. For constant-field, linear R/L, viscous-friction
model, write L di/dt=v−Ri−kω; J dω/dt=ki−bω−load; dθ/dt=ω. The back EMF resists
current as the shaft turns. The three states have distinct units; v is a command,
not a speed. Temperature and driver switching are excluded states.

Multiply the first equation by i and the second byω. The kiω terms cancel:
d(Li²/2+Jω²/2)/dt=vi−Ri²−bω²−load·ω. This independent balance catches sign errors.
With R2Ω,L.02H,J.02kg·m²,b.02N·m·s/rad,k.1 in coherent SI, at i1A,ω3rad/s,
v6V,load.01N·m, slopes are185A/s and1.5rad/s²; stored-energy increase3.79W equals
6W input less2W copper,.18W friction and.03W load transfer.

Set both slopes to0. With no load and k>0, i=bω/k; substitution into v=Ri+kω gives
ω=k v/(Rb+k²). The stated6V bound permits12rad/s steady speed. A20rad/s request
is infeasible. Large gains cannot fix that missing capacity; they can only drive
saturation harder. Thermal and current constraints can impose stricter limits.

## 3. Sensing creates a second state history

A speed sensor can have scale/bias, quantization, noise and latency. In the local
model y_n=quantize(ω_n+bias+seeded_noise), returned d samples later. The first
sample is held as prehistory. State that initialization because a delay queue
otherwise pretends to know earlier motion. A.002s sample interval and d100 mean
.2s latency, not100seconds. A timestamp is part of a measurement's meaning.

If a controller makes measured steady error r−y≈0 while y=ω+c, true speed tends
to r−c. With c+.5rad/s and target2, roughly1.5rad/s is expected. Repeatedly observing
the same biased sensor cannot identify that offset independently. A calibrated
reference is needed. Gaussian pseudorandom samples are a declared synthetic model,
not an empirically verified noise distribution.

## 4. A controller remembers error and can remember too much

Proportional action u_p=Kp(r−y) responds immediately. Integral state z_next=z+e dt
accumulates persistent error so nonzero command can remain when measured error
becomes small. Derivative action estimates minus the rate of measurement change,
not target change, avoiding a target-step derivative kick. A first-order filter
reduces high-frequency differencing noise but also changes temporal response.

The implemented command is clip(Kp e+Ki z−Kd filtered_dy,−U,U). Clipping u does
not constrain z. Under an unreachable positive target, z can keep growing while
the driver remains saturated. After the target falls, this memory can keep the
command positive until negative error unwinds it. Conditional integration rejects
candidate integral increments that drive farther into saturation while allowing
increments that unwind it. It is a precisely specified strategy, not a universal
stability proof or a substitute for modeling an inner current limiter.

For Kp2,Ki1,U3V,e10rad/s,dt.01s, P alone requests20V. After100samples an unrestricted
integrator contributes another10V, although output stays3V. The conditioned
integrator keeps z0 in that example. Same instantaneous actuator command, different
future state: a final-output-only test misses the mechanism.

## 5. Build, verify and investigate

The [complete motor/control lesson](../17-embedded-robotics/control-path/README.md)
contains runnable original code, RK4 equations, hand/analytic tests, separate
exercises/hints/solutions and executed raw JSON. The
[guided project](../projects-guided/p13-robot-controller/README.md) constructs the
plant, numerical step, sensor and controller in stages. Use it before reading the
reference implementation. Ten tests check derivatives, energy, exact decoupled
exponentials, gear energy, delay, derivative initialization, saturation recovery
and failed-input state preservation.

The executed synthetic experiment asks whether conditioned integration improves
recovery when20rad/s changes to2rad/s at4s under6V. With identical motor/gains,
reference samples end near2.00753rad/s with conditioning and7.51264 without it;
the chosen post-switch absolute-error integrals are3.65797 and38.7934rad. These
observations match the predicted windup mechanism for these settings. The biased
case ends near1.50734rad/s. Delay slightly improved the chosen metric in one case;
preserve that observation and vary delay/gains/horizon before generalizing.

Step refinement changes both the integrator and the sampled controller. Use an
open-loop analytic special case for numerical accuracy, and treat closed-loop
sample changes as a different controller experiment. Real firmware also needs
worst-case deadlines, packet-loss/stale-reading policies, watchdogs, current
limits, safe reset and independently characterized hardware. None were measured.

## 6. Reconstruct and extend

Without notes, derive the energy balance, no-load maximum speed and gear-square
relation. Write the exact sample update order and predict a bias-induced offset.
Rebuild the simulation and check independent tests. Add an opposing load step;
predict increased current and reduced speed before execution. Then add a current
limit and show where the original voltage-only anti-windup assumption fails.

This bounded path gives a physical mechanism, implementation and causal experiment.
It does not teach full multi-link kinematics/dynamics, estimation, motion planning,
embedded interrupt/driver implementation, robot contact or physical safety testing.
Those remain explicit remediation work. A useful next unit derives a planar
link's forward kinematics and Jacobian from geometry before choosing a robotics
framework; this coursebook makes no claim that such a unit was completed here.
