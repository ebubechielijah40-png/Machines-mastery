# Maximum Product Contiguous Window

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A synthetic multiplicative score can flip sign when a negative factor arrives. Find the contiguous interval whose factors produce the maximum product.

## Task

Return the maximum product of any non-empty contiguous subarray.

## Constraints

- 1 <= len(values) <= 200000
- integer values may be negative or zero

## Examples

- `[2,3,-2,4] -> 6`
- `[-2,0,-1] -> 0`
- `[-2,3,-4] -> 24`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This is dynamic programming over sufficient extremes and illustrates why sign changes can make “bad” intermediate states valuable later.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
