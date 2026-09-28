# First Missing Positive Identifier

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A compact synthetic allocator stores positive slot IDs in an unsorted array. Find the smallest positive ID absent from the set without allocating another O(n) set.

## Task

Return the smallest missing positive integer using O(n) time and O(1) auxiliary space; mutating the input is allowed.

## Constraints

- 0 <= len(values) <= 200000
- integers may be negative or very large

## Examples

- `[3,4,-1,1] -> 2`
- `[1,2,0] -> 3`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This is an example of using the input array itself as an implicit hash table when keys map bijectively to a bounded index range.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
