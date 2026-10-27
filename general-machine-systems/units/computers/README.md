# Computers — mechanism, failure, and reconstruction

## Why this machine exists
Computers implement programmable information transformations on physical hardware.

## Energy and information path
Electrical power → regulated rails/clocks → transistors/logic → CPU/memory/I/O → OS/runtime → applications → external state.

## Mechanism
Instructions manipulate encoded state. Layers hide detail but preserve interfaces: ISA, memory hierarchy, interrupts, buses, syscalls and protocols connect the stack.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
power/thermal faults, memory errors, storage failure, software bugs, races, security compromise

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Trace one `write()` call conceptually from source code to syscall to filesystem/device buffering. Measure with strace where available.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Given an unknown executable, infer inputs/outputs, inspect binary/syscalls, and reconstruct a behavioral model.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
