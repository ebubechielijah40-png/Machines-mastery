# Maximum Burst in a Circular Buffer

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A periodic telemetry buffer wraps at midnight. The strongest contiguous burst may cross the physical end of the array.

## Task

Return the maximum sum of a non-empty contiguous segment in a circular array.

## Constraints

- 1 <= len(values) <= 200000
- segment may wrap at most once

## Examples

- `[5,-3,5] -> 10`
- `[-3,-2,-5] -> -2`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Circular storage and ring buffers turn physical boundaries into an implementation detail. Reasoning by complements often simplifies wraparound algorithms.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
