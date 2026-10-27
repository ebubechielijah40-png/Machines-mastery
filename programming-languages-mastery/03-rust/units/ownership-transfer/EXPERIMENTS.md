# Actual ownership and vector-growth experiment

Question: does transferring this Vec through a Packet and thread duplicate its
byte buffer? Which capacity changes occur while building33 bytes?

Hypothesis: moving the owner preserves the live allocation; cloning is the
separate operation that duplicates bytes. Capacity transitions are observations
of the installed implementation, not a promised factor.

Control: bytes0..32, one worker, no external input, same source and compiler;
change debug versus optimized test builds, then extend to another element type.
Instrumentation: capacity after each push, live buffer-address equality before/
after transfer, exact arithmetic sum and final length, thread join outcome.
Procedure: execute run.py; inspect its actual version, flags,8-test outputs,
three rejected programs and final binary output in [observed.json](evidence/observed.json).
The returned buffer is still live when compared; no freed address is dereferenced.

The actual run reported sum528, length33 and move_preserved_buffer=true. Read
its capacity list directly rather than copying a number from a different runtime.
This supports the declared move/buffer behavior of this program. It does not
measure allocator throughput, bytes copied by all compiler transformations,
cache behavior, scheduling latency or the safety of unsafe Rust. Alternative
explanations for changing capacity counts include element size and library
policy. Follow up by using u64 values and an explicit clone; predict which
observable invariants survive before running.

Reconstruction assessment: implement the same contract without the reference,
then introduce an old view used after mutation. Explain why that different
program is rejected even when a particular push would have spare capacity.
