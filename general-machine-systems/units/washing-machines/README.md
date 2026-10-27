# Washing Machines — mechanism, failure, and reconstruction

## Why this machine exists
Washing machines automate fluid handling, heating, agitation and high-speed rotation safely.

## Energy and information path
Mains power → controller → valves/heater/motor/pump; sensors report door, level, speed, temperature; water/detergent interact with load.

## Mechanism
Cycle control is a state machine constrained by safety interlocks and physical dynamics. Spin imbalance couples load distribution to vibration.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
drain blockage, imbalance, door interlock, bearing wear, heater/sensor faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Model wash-cycle states and inject sensor failures; verify unsafe transitions are blocked.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Reconstruct control state machine from observed cycle behavior.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
