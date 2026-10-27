# Actuators — mechanism, failure, and reconstruction

## Why this machine exists
Actuators convert control energy into physical action.

## Energy and information path
Controller command → driver/power stage → electromagnetic/fluid/thermal mechanism → force/position → mechanical load → feedback.

## Mechanism
Actuator performance is bounded by force/torque, speed, stroke, bandwidth, power, heat, and control dynamics.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
stall, saturation, overheating, backlash, leakage, driver faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Command step changes in a simulated motor/servo and measure rise time, overshoot, steady-state error.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Choose an actuator for a robot joint from load/speed constraints and state missing real-world data.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
