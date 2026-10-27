# Autonomous Systems — mechanism, failure, and reconstruction

## Why this machine exists
Autonomous systems close perception-decision-action loops with limited human intervention.

## Energy and information path
Sensors → perception → state estimate → prediction/planning → control → actuators → world, with safety monitor and operator interface.

## Mechanism
Autonomy is bounded by observability, model uncertainty, compute latency, actuator authority, environment shift and fallback design.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
distribution shift, sensor spoof/failure, planning error, stale maps, actuator saturation

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate a planner/controller with an obstacle appearing after planning; test replanning latency/fallback.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Create an assurance case listing what must remain true for safe operation.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
