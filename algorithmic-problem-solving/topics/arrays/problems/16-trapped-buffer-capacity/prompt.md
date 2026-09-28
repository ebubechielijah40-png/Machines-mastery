# Compute Trapped Capacity Between Barriers

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A simplified cross-section of a containment tray gives barrier heights at unit-spaced positions. Compute how many unit volumes of liquid can remain after filling and settling.

## Task

Given nonnegative integer heights, return total trapped water.

## Constraints

- 0 <= len(heights) <= 200000
- 0 <= height <= 1000000

## Examples

- `[0,1,0,2,1,0,1,3,2,1,2,1] -> 6`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This problem trains reasoning about local capacity under two-sided constraints and the proof pattern behind two-pointer elimination.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
