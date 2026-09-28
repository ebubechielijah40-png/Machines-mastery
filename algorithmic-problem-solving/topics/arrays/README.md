# Arrays — released problem set

**Status: PREPARED; learner NOT STARTED.** This topic now contains 20 original problems: 6 basic, 8 intermediate and 6 hard. Each problem separates prompt, graduated hints, detailed solution, executable implementation and tests. Generated preparation is not learner mastery.

## Learning intent

Arrays are not merely “lists of values.” They expose contiguous indexed state, mutation, locality, prefix/suffix structure, in-place transforms and the cost of moving data. The set progresses from direct scans and compaction into dynamic invariants, in-place encoding, order statistics and implicit graph interpretations.

## Required workflow

For each problem: read only `prompt.md` → write an attempt → state time/space complexity and an invariant → use `hints.md` only if blocked → run your tests → inspect `solution.md` → modify one constraint and solve again. Periodically reconstruct the solution without reference.

## Real-world transfer

Problems are framed around buffers, telemetry, storage compaction, ordered runs, scheduling, capacity updates and observability samples. These are bounded teaching models; do not equate an algorithm exercise with a production-ready subsystem. Use the production track to measure and operate larger systems.

## Problem index

- [01 — Rotate a Log Buffer Right](problems/01-rotate-log-buffer/prompt.md) — basic
- [02 — Stable Compaction of Deleted Records](problems/02-compact-deleted-records/prompt.md) — basic
- [03 — Find the First Ordering Violation](problems/03-first-order-violation/prompt.md) — basic
- [04 — Run-Length Encode Repeated Events](problems/04-run-length-events/prompt.md) — basic
- [05 — Merge Two Sorted Time Series](problems/05-merge-time-series/prompt.md) — basic
- [06 — Move Empty Slots to the End](problems/06-move-empty-slots/prompt.md) — basic
- [07 — Per-Sensor Product Without Self](problems/07-product-except-self/prompt.md) — intermediate
- [08 — Maximum Contiguous Burst Load](problems/08-maximum-burst-load/prompt.md) — intermediate
- [09 — Maximum Burst in a Circular Buffer](problems/09-circular-burst-load/prompt.md) — intermediate
- [10 — Next Lexicographic Schedule](problems/10-next-permutation-schedule/prompt.md) — intermediate
- [11 — Partition Three Packet States](problems/11-three-state-packet-partition/prompt.md) — intermediate
- [12 — Find the Minimal Repair Window](problems/12-minimal-repair-window/prompt.md) — intermediate
- [13 — Apply Bulk Range Load Updates](problems/13-range-load-updates/prompt.md) — intermediate
- [14 — Find Balanced Shard Cut Points](problems/14-balanced-shard-cut/prompt.md) — intermediate
- [15 — First Missing Positive Identifier](problems/15-first-missing-positive-id/prompt.md) — hard
- [16 — Compute Trapped Capacity Between Barriers](problems/16-trapped-buffer-capacity/prompt.md) — hard
- [17 — Select the k-th Latency Without Full Sorting](problems/17-kth-latency-quickselect/prompt.md) — hard
- [18 — Merge Into a Reserved Storage Buffer](problems/18-merge-into-reserved-buffer/prompt.md) — hard
- [19 — Find a Duplicate Without Modifying the ID Array](problems/19-duplicate-cycle-id/prompt.md) — hard
- [20 — Maximum Product Contiguous Window](problems/20-maximum-product-window/prompt.md) — hard

## Validation

Run every problem test from repository root:

```sh
python3 algorithmic-problem-solving/topics/arrays/run_all_tests.py
```

The test runner records pass/fail only; passing tests do not advance learner mastery. Several tests use exhaustive bounded inputs or an independent brute-force oracle.
