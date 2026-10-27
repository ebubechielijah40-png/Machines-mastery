# Generators — mechanism, failure, and reconstruction

## Why this machine exists
Generators convert mechanical work into electrical energy using electromagnetic induction.

## Energy and information path
Prime mover rotates magnetic/electrical structures; changing flux induces voltage; load current creates opposing torque and heat.

## Mechanism
Faraday induction links changing magnetic flux to EMF. Regulation and power electronics condition raw output for the load/grid.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
overheating, insulation failure, bearing wear, overvoltage, excitation/regulator faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Spin a small hobby motor as a generator and measure open-circuit voltage versus speed if safe equipment exists.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Design the measurement plan to characterize a mystery generator without knowing internals.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
