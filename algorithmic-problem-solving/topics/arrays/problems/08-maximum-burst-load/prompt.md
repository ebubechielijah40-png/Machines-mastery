# Maximum Contiguous Burst Load

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

Per-minute load deltas may be positive or negative. Find the contiguous interval with the largest net increase to identify the strongest burst.

## Task

Return the maximum sum of any non-empty contiguous subarray.

## Constraints

- 1 <= len(values) <= 200000
- values are integers

## Examples

- `[-2,1,-3,4,-1,2,1,-5,4] -> 6`
- `[-5,-2,-7] -> -2`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This models burst detection, profit/loss windows and score accumulation. The important idea is dynamic state compression: a whole set of candidate intervals collapses to one sufficient statistic.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
