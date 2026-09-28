# Find a Duplicate Without Modifying the ID Array

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A read-only array of n+1 references stores IDs in the range 1..n, guaranteeing at least one duplicate. Find one duplicate using constant extra memory.

## Task

Return a duplicated value without modifying the input and using O(1) auxiliary space.

## Constraints

- len(values)=n+1 for n>=1
- each value is in [1,n]
- at least one value repeats

## Examples

- `[1,3,4,2,2] -> 2`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

The deeper lesson is representation: an integer array can encode a directed functional graph. Reinterpreting data structure semantics can unlock algorithms unavailable in the “just an array” view.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
