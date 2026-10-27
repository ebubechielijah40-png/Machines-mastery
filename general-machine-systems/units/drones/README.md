# Drones — mechanism, failure, and reconstruction

## Why this machine exists
Multirotor drones create controlled thrust to regulate attitude and position.

## Energy and information path
Battery → ESCs → motors/propellers → thrust; IMU/barometer/GNSS/camera → state estimate → flight controller → motor commands.

## Mechanism
Differential rotor thrust creates roll/pitch/yaw torques. Fast inner attitude loops stabilize the inherently coupled body; outer loops command velocity/position.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
prop failure, battery sag, estimator drift, saturation, wind, comms loss

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate a vertical-axis controller with mass and thrust limits; inject sensor noise and battery-related thrust reduction.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Draw flight-control loops and define safe behavior for GPS or radio loss.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
