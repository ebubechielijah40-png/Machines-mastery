# Power Supplies — mechanism, failure, and reconstruction

## Why this machine exists
Power supplies convert and regulate electrical energy into voltage/current forms a load can use.

## Energy and information path
Input source → rectification/conversion/switching → filtering → feedback control → regulated output.

## Mechanism
Linear regulators dissipate excess voltage as heat; switching converters store/transfer energy through inductors/capacitors and controlled switches, trading complexity for efficiency.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
overcurrent, thermal overload, unstable feedback, capacitor aging, short circuits, ripple

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate a regulator under varying load; measure output droop/ripple and efficiency.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Given device voltage/current needs, sketch conversion stages and protections.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
