# Sensors — mechanism, failure, and reconstruction

## Why this machine exists
Sensors convert a physical quantity into an electrical/digital representation.

## Energy and information path
Physical stimulus → transduction → analog signal → conditioning → ADC/digital interface → calibrated value.

## Mechanism
A sensor has range, sensitivity, resolution, bandwidth, noise, bias, drift, hysteresis, and calibration. A digital reading is not the physical quantity itself.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
drift, saturation, noise, miscalibration, aliasing, environmental sensitivity

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Record repeated readings at fixed conditions, estimate noise, then vary the target quantity and fit a calibration curve.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Design a sensing chain for temperature/vibration, identifying uncertainty and sampling requirements.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
