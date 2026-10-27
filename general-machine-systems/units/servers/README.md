# Servers — mechanism, failure, and reconstruction

## Why this machine exists
Servers provide networked computation/storage under concurrency and failure.

## Energy and information path
Power/network requests → NIC/kernel → process/runtime → application → cache/database/storage → response, with observability/control planes.

## Mechanism
Throughput and latency emerge from queues and bottlenecks. Redundancy changes failure behavior but adds consistency/coordination problems.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
overload, dependency timeout, disk failure, memory leak, network partition, bad deploy

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Load-test a simple HTTP service and identify saturation by CPU, queue, DB or connections.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Reconstruct service architecture from traces, ports, logs and failure behavior.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
