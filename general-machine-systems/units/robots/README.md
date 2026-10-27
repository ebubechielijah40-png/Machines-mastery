# Robots — mechanism, failure, and reconstruction

## Why this machine exists
Robots combine sensing, estimation, planning, control and actuation to change the physical world.

## Energy and information path
Environment → sensors → state estimate → decision/planner → controller → actuators → body/environment → feedback.

## Mechanism
Performance depends on model accuracy, latency, observability, actuation limits, uncertainty and safety constraints.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
localization loss, actuator saturation, sensor failure, unstable control, collision, software faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate a 1D robot moving to a target with feedback; add sensor noise/delay and tune controller.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Design the block diagram for a mobile robot and specify fallback behavior for sensor loss.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
