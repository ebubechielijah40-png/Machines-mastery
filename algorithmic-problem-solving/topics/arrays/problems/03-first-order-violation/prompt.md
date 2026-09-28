# Find the First Ordering Violation

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

A storage engine expects a batch to be nondecreasing by timestamp before bulk-loading it into an ordered index. Detect the first adjacent pair that violates that contract.

## Task

Return the smallest index `i` such that `values[i] > values[i+1]`. Return -1 when the array is nondecreasing.

## Constraints

- 0 <= len(values) <= 1000000
- duplicates are valid
- items support comparison

## Examples

- `[1,2,2,4] -> -1`
- `[1,5,3,7] -> 1`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Sorted-run validation appears before merge operations, index construction, event-time processing and binary-search based query paths.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
