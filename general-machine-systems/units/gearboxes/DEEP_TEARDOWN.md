# Gearboxes — deep teardown and reconstruction guide

## Purpose
combining gear stages to transform speed/torque/direction.

## Mechanism chain
`input shaft → gear mesh stages → bearings → output shaft`.

Do not memorize this chain as a final design. Use it to create hypotheses for a specific artifact. Real implementations vary.

## What to identify on a real system

1. boundary and operating environment;
2. energy source/storage and conversion stages;
3. structural/load-bearing components;
4. state variables and stored energy/information;
5. sensors and observables;
6. actuators/control elements;
7. mechanical/electrical/software interfaces;
8. timing/feedback loops;
9. heat/loss paths;
10. maintenance and safety constraints.

## Failure tree
Start with: heat, lubrication, backlash, bearing/gear failure. Add environmental, manufacturing, human-interface, power, software, and maintenance causes as appropriate. For each failure, predict an observable symptom and a distinguishing test.

## Reconstruction exercise
Without disassembly, observe normal operation and at least three controlled input changes. Draw two plausible internal architectures. Design a safe experiment that makes them predict different behavior. After evidence narrows the model, build a non-hazardous simplified simulation or bench model.

## Quantitative assignment
Choose one conserved/limited quantity—energy, power, force/torque, flow, bandwidth, storage, latency, or heat. Estimate it from explicit assumptions, check units, then identify which measurement would most improve the estimate.

## Transfer challenge
Compare this system with another category in `general-machine-systems/units/`. Identify one mechanism that transfers and one analogy that breaks.

## Limits
A behavioral replica does not prove identical internals. Do not infer component ratings, safety margins, material properties, or legal operating limits without verified documentation/measurement.
