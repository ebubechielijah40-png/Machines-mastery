# Microcontrollers — mechanism, failure, and reconstruction

## Why this machine exists
Microcontrollers integrate CPU, memory and peripherals for direct device control.

## Energy and information path
Clock/power/reset → CPU executes firmware → memory-mapped peripherals exchange data with timers, ADC, GPIO, serial buses.

## Mechanism
Peripheral registers expose hardware state; interrupts redirect control flow on events. Clock trees and power modes affect timing and energy.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
bad clock config, brownout, peripheral misuse, interrupt storms, flash wear

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Use a simulator/dev board to toggle GPIO with timer hardware, then compare busy-wait timing.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Map a simple sensor-to-actuator task onto peripherals and identify what the CPU need not do itself.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
