# Motion, force, torque and energy before a machine controller

A motor controller's numbers become meaningful only after choosing what moves,
which forces act, and what a measurement represents. Begin with
[counting/units](../mathematics/counting-and-units/README.md) and the
[change/error bridge](../mathematics/change-error-and-evidence/README.md).
The source trail for this original bridge is in the
[control source map](../../17-embedded-robotics/control-path/SOURCES.md).

## Motion requires state and a reference

Position x in m depends on an origin and axis. Displacement is x_final−x_initial;
velocity is the derivative dx/dt in m/s, acceleration dv/dt in m/s². Constant
velocity has zero acceleration even if its magnitude is large. Force is not
required to maintain ideal frictionless constant motion; it changes momentum.
Newton's model for a constant mass m is ΣF=m a. We adopt this experimentally
motivated classical law within low-speed macroscopic mechanics; it is not
proved from algebra or claimed valid in quantum/relativistic regimes.

For a 2 kg cart, forward force6 N and backward friction2 N give net4 N and
acceleration2 m/s². Starting at rest for.5 s under constant net force gives
v=1 m/s and x−x0=.25 m, because v=a t and accumulated position is a t²/2.
Forces sum before dividing by mass. Dividing the driving force alone by m
ignores the stated friction and predicts the wrong motion.

## Energy checks a different aspect of the same motion

For constant force along displacement, work W=F Δx in J. For varying force,
accumulate F dx. Use a=v dv/dx in F=m a to obtain dW=m v dv, whose accumulation
is Δ(m v²/2). Define kinetic energy K=m v²/2. In the cart example, net work
4*.25=1 J matches final kinetic energy.5*2*1²=1 J. Driving work is1.5 J and
friction dissipates.5 J. Energy has not disappeared; the model transfers it to
untracked thermal surroundings. Power is work per time, in W=J/s, with P=F v
for aligned instantaneous quantities. A large force on a blocked stationary
cart does zero mechanical work while a real motor can still heat electrically.

## Rotation is not just translation with different labels

A point at perpendicular radius r moves distance r dθ for angular increment
in radians. Tangential force gives torque τ=r F_t in N·m. Forces through the
axis give zero torque about it even if they are large. From K=Σ m_i(r_iω)²/2,
define fixed-axis inertia J=Σm_i r_i², in kg·m². The same total mass farther
from the axis has larger inertia. Sum tangential Newton equations times radii
to get net torque=J dω/dt for a rigid body about a fixed inertial axis.

A .2 m lever with perpendicular10 N force gives2 N·m. At ω=3 rad/s it transfers
6 W. If the force is parallel to the lever it gives zero torque, not2 N·m.
A rotor with J=.5 kg·m² under net2 N·m accelerates at4 rad/s². Units alone
cannot distinguish torque from energy even though both contain N·m: torque
must be paired with an angular displacement to calculate work. Keep the
quantity's physical role, not only its dimensional signature.

## Conservation is a boundary statement

Choose the system boundary before writing “energy is conserved.” A motor's
magnetic/kinetic stored energy changes because electrical power crosses the
boundary, friction/resistance generate heat and load work leaves. If temperature
is a state, a lumped thermal model can add `C_th dT/dt=P_loss−(T−T_ambient)/R_th`,
where C_th is J/K and R_th K/W. This assumes one spatially uniform temperature,
constant coefficients and a linear heat-flow relation. It is not a universal
material law; spatial gradients, radiation, changing resistance and phase
transitions can break it. Insulation failure and allowable temperature require
material specifications, which this hypothetical model does not supply.

## Transfer and assessment

1. A cart moves backward while force points forward. Explain the signs of power
   and kinetic-energy change. 2. Two1 kg point masses lie at radii1 and2 m from
   an axis: calculate J. 3. A20 W loss and R_th=2 K/W produce which steady
   temperature rise in the declared thermal model? 4. Why does a steady
   temperature not imply zero heat flow? 5. Reconstruct the cart/rotor balances
   without this page; give a counterexample to omitting friction or the system
   boundary. Answers: negative power/slowing backward motion; J=5 kg·m²;
  40 K rise; input loss balances outward heat rather than vanishing.

Continue directly into [the electromechanical model and sampled controller](../../17-embedded-robotics/control-path/README.md).
Its independent hand/energy/analytic tests and synthetic experiment provide the
executable extension of this bridge. No physical experiment is claimed here.
