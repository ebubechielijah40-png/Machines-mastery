# Vehicles — mechanism, failure, and reconstruction

## Why this machine exists
Vehicles transform stored energy into controlled motion while managing traction, steering, braking and safety.

## Energy and information path
Fuel/battery → engine/motor → transmission/inverter → wheels → road; sensors/controllers regulate torque, stability and emissions/energy.

## Mechanism
Longitudinal acceleration follows net force/mass; drag grows strongly with speed; tire-road friction bounds acceleration/braking/turning.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
brake fade, tire loss, cooling faults, powertrain failure, sensor faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Compute stopping distance under several speeds/friction assumptions and separate reaction from braking distance.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
From a vehicle subsystem symptom, draw energy/control paths and choose measurements before parts.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
