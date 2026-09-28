# Partition Three Packet States

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A packet inspection pipeline labels packets 0=drop, 1=inspect, 2=forward. Group the states in one pass before handing ranges to specialized workers.

## Task

Sort an array containing only 0, 1 and 2 in place using O(1) auxiliary space.

## Constraints

- 0 <= len(values) <= 1000000
- every element is 0, 1 or 2

## Examples

- `[2,0,2,1,1,0] -> [0,0,1,1,2,2]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Multiway partitioning appears in quicksort variants, memory allocators, packet classification and work-queue bucketing.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
