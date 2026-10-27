# Actual bounded allocator experiment

Question: when construction fails after allocation1, does its error path release
that acquired storage? Hypothesis: registered error cleanup releases the tag;
success transfers both buffers to caller cleanup.

Controlled variables: tag=tag, body=DATA, Zig0.13.0, u8 allocations, same constructor
and allocation order. Change only fixed-buffer budget over1,2,4,8,16 bytes.
Instrumentation: returned error/success and FixedBufferAllocator.end_index before
successful cleanup and after every path. Procedure: run run.py using the pinned
compiler and read [observed.json](evidence/observed.json).

Actual observations:1,2 and4 bytes returned OutOfMemory with end0;8 and16 bytes
succeeded with end7 then end0. The failure-injection test also ran both allocation
failure prefixes. The deliberately broken constructor produced the expected
nonzero MemoryLeakDetected result. That failure is retained as a successful
negative-control detection, not passed off as a working constructor.

Interpretation: the written paths balance their acquisitions under the inspected
allocator/test harness. An alternative constructor branch could leak without
these cases exercising it, so update the matrix whenever adding resources.
The fixed-buffer end is not process memory, allocator fragmentation or arbitrary
alignment overhead. Follow up with u64-aligned blocks and a non-LIFO interleaving;
predict why end recovery can differ. No real embedded memory exhaustion, timing
or multi-thread allocator claim is reproduced by this finite simulation.
