# Printers — mechanism, failure, and reconstruction

## Why this machine exists
Printers coordinate data interpretation, precise motion and material deposition/marking.

## Energy and information path
Document data → raster/command processing → motion/media control → marking mechanism → physical page/object.

## Mechanism
A printer is a cyber-physical pipeline: timing errors, calibration, material properties and mechanics can all appear as output defects.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
paper jams, clogged nozzle, belt/slip, calibration drift, thermal faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
For a simulated raster printer, vary step calibration and predict geometric distortion.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Trace a print artifact backward from page pattern to candidate motion/data/marking causes.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
