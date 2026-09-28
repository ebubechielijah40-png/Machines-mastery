# Find the Minimal Repair Window

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A mostly sorted SSTable run was corrupted by one bounded reorder. Find the smallest contiguous interval that must be sorted to restore global order.

## Task

Return `(left,right)` for the smallest subarray which, if sorted, makes the entire array nondecreasing. Return `(-1,-1)` if already sorted.

## Constraints

- 0 <= len(values) <= 200000

## Examples

- `[1,2,6,4,5,7] -> (2,4)`
- `[1,2,3] -> (-1,-1)`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Localized repair is common in sorted-file maintenance and data validation: diagnose the smallest inconsistent region instead of rewriting the whole dataset.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
