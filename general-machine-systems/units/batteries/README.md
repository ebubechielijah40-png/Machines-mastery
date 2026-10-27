# Batteries — mechanism, failure, and reconstruction

## Why this machine exists
Batteries store chemical free energy and deliver electrical energy through electrochemical reactions.

## Energy and information path
Chemical potential → ion/electron transport → terminal voltage/current → load; internal resistance and reaction kinetics create heat and voltage drop.

## Mechanism
State of charge, open-circuit voltage, internal resistance, temperature, current rate, and chemistry shape behavior. Capacity in Ah is not identical to energy in Wh.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
overcharge, overdischarge, thermal runaway for some chemistries, aging, internal shorts, cell imbalance

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Use simulation or a safe protected cell/source to plot terminal voltage under several loads; infer internal resistance from voltage sag.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Specify sensing/protection needed for a multi-cell pack, without giving unsafe pack-building instructions.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
