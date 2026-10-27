# Pneumatics — mechanism, failure, and reconstruction

## Why this machine exists
Pneumatics use compressed gas for motion/control where compliance and cleanliness can be useful.

## Energy and information path
Compressor stores energy in compressed gas; valves meter flow; actuators convert pressure to motion; exhaust returns gas to atmosphere.

## Mechanism
Gas compressibility makes behavior spring-like and pressure dependent, unlike ideal incompressible hydraulic assumptions.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
leaks, pressure drop, moisture, valve sticking, unsafe stored energy

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Model cylinder force versus gauge pressure and area; compare with hydraulic assumptions.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Infer likely valve/actuator roles from a pneumatic schematic and predict state when supply is removed.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
