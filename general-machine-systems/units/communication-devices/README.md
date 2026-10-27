# Communication Devices — mechanism, failure, and reconstruction

## Why this machine exists
Communication devices encode information into physical signals and recover it across noisy channels.

## Energy and information path
Source bits → framing/coding/modulation → transmitter/channel → receiver/demodulation/decoding → bits.

## Mechanism
Bandwidth, signal-to-noise, modulation, coding, synchronization and channel properties bound performance. Protocol layers add addressing, reliability and multiplexing.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
interference, clock drift, fading, congestion, framing errors, hardware faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate binary transmission with adjustable bit-flip probability and add a simple error-detecting code.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Given observed error patterns, distinguish channel noise from framing/protocol hypotheses.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
