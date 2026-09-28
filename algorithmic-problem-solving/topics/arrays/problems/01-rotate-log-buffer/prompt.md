# Rotate a Log Buffer Right

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

A bounded diagnostic buffer is exported in chronological order, but the hardware DMA cursor means the last k entries physically appear at the front of the next snapshot. Reconstruct the logical order by rotating the array right by k positions.

## Task

Given a mutable list `values` and integer `k`, rotate the list to the right by `k` positions in place. Empty input must remain empty. Negative `k` is allowed and follows Python modulo semantics.

## Constraints

- 0 <= len(values) <= 100000
- values may contain duplicates
- k may be any integer

## Examples

- `[1,2,3,4,5], k=2 -> [4,5,1,2,3]`
- `[1,2,3], k=-1 -> [2,3,1]`
- `[], k=10 -> []`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Ring buffers, circular queues, storage pages and media buffers all use logical order that differs from physical layout. Rotation is a small model of translating between those views.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
