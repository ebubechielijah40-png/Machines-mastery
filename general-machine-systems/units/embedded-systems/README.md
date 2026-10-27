# Embedded Systems — mechanism, failure, and reconstruction

## Why this machine exists
Embedded systems couple computation tightly to physical devices under timing/resource constraints.

## Energy and information path
Sensors/inputs → MCU peripherals → firmware state/control → drivers → actuators/communications, powered by constrained electrical system.

## Mechanism
Interrupts, timers, DMA, buses, real-time deadlines, watchdogs and finite memory shape software architecture.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
missed deadlines, brownouts, stack overflow, race conditions, sensor faults, watchdog resets

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Write a simulated periodic controller with injected jitter and missed deadlines; measure effects.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Reconstruct firmware architecture from I/O list and timing requirements before choosing code structure.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
