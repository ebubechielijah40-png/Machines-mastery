# Digital construction sequence

[EXPLANATION] Planned progression: binary representation → Boolean algebra → truth tables → gates → combinational composition → multiplexers/demultiplexers → encoders/decoders → adders/comparators → ALU → latches/flip-flops → registers/counters → finite-state machines → memory → datapath/control → CPU.

At each combinational boundary, derive the complete finite function before RTL. At each stateful boundary, specify initial/reset state, clock/update event, priority, next state and outputs. Distinguish a latch's level-sensitive behavior from an edge-triggered model; do not casually use them interchangeably. Timing topics include propagation delay, clocking, setup/hold and physical memory behavior, gated by verified source/device evidence. The prepared [clocked register](../hardware-description-languages/systemverilog/units/01-enabled-register/README.md) demonstrates the logical contract only.

For physical gates, the chain is charge → current → voltage → resistance/power → controlled switching → transistor device model → logic voltage ranges → gate behavior. The electricity bridge provides meanings, but a full transistor construction lesson remains unprepared. No simulated truth table certifies a physical gate's speed or noise tolerance.

Capstone acceptance: write assembly for the learner's declared RISC-V subset, compare instruction-by-instruction traces with an independent architectural model, then add components only when their contracts are verified. Full ISA compatibility must not be claimed for a subset.
