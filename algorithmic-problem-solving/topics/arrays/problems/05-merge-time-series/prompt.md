# Merge Two Sorted Time Series

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

Two shards emit records already sorted by timestamp. A downstream stage needs one globally sorted sequence while preserving duplicates.

## Task

Given two sorted lists, return one sorted list containing all values from both.

## Constraints

- combined length <= 200000
- inputs are individually nondecreasing
- duplicates must be preserved

## Examples

- `[1,4,7] and [2,2,9] -> [1,2,2,4,7,9]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This is the merge primitive behind merge sort, LSM-tree compaction, ordered stream fusion and external sorting.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
