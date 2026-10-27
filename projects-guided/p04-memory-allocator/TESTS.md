# Tests and debugging evidence

Run from the repository root:

```bash
python projects-guided/p04-memory-allocator/code/run.py
```

The harness compiles C11 with `-Wall -Wextra -Werror`, runs at O0 and O2, then
runs O1 with `-fsanitize=undefined -fno-sanitize-recover=all`. Each assertion
program tests invalid request boundaries, exact offsets and rounded sizes,
interior/double release, coalescing, alternating-hole fragmentation, and 5,000
deterministic allocation/release steps. During that trace, live buffers carry
separate byte tags and every live payload is rechecked after every operation.
An independent pairwise interval check detects overlapping live allocations;
the metadata partition checker is another check, not the sole oracle.

[observed-tests.json](observed-tests.json) preserves the first actual run.
[evidence/validation.json](evidence/validation.json) records the current run,
including command, environment, outputs and status. No sanitizer result proves
all C behavior valid; this harness does not intentionally dereference an invalid
pointer, and bounded generated traces are not exhaustive.

Debug by injecting one defect at a time in your learner copy:

1. Shift metadata forward during insertion. Predict which saved remainder is
   overwritten, then use a three-allocation case to expose it.
2. Omit coalescing. Both requests may release successfully, but a later large
   allocation and the no-adjacent-free invariant will fail.
3. Compare only total block size. Construct an overlapping partition with an
   equal-sized gap to demonstrate why that check is insufficient.
4. Remove the request cap before `requested + 7`. A SIZE_MAX request can wrap;
   rejection must happen before unsafe arithmetic.
5. Free a stale address after the same offset is reallocated. The raw-pointer
   API cannot identify the old lease. Treat this as a documented limitation,
   not a test expected to reject every such case.
