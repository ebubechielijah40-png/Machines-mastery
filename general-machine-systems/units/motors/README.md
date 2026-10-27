# Motors — mechanism, failure, and reconstruction

## Why this machine exists
Electric motors convert electrical energy into controlled mechanical torque and motion.

## Energy and information path
Electrical source → switching/commutation → current in windings → magnetic field interaction → torque → rotor/load, with heat and losses.

## Mechanism
Torque arises from electromagnetic interaction. Back-EMF grows with speed and opposes applied voltage. Controllers regulate current/voltage timing according to motor type.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
overcurrent, overheating, bearing wear, demagnetization, insulation breakdown, controller failure

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
With a safe small DC motor, vary supply voltage/load and record speed/current qualitatively or numerically. Explain back-EMF/current behavior.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
From required torque-speed curve, sketch motor + driver + sensor + power path.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
