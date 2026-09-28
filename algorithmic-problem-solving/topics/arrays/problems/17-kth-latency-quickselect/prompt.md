# Select the k-th Latency Without Full Sorting

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A diagnostic tool needs one order statistic from a large latency sample. Full sorting does more work than necessary when only one rank is requested.

## Task

Return the k-th smallest value using zero-based k. The function may mutate the input. Reject invalid k.

## Constraints

- 1 <= len(values) <= 200000
- 0 <= k < len(values)

## Examples

- `[7,2,9,4], k=1 -> 4`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Percentiles and order statistics are common in observability systems. Production implementations often use streaming sketches instead when the full sample cannot be retained.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
