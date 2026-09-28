# Move Empty Slots to the End

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

A numeric work buffer uses zero to mean an unused slot. Compact active values toward the front without reordering them.

## Task

Move all zero values to the end in place while preserving the order of nonzero values. Return the list.

## Constraints

- 0 <= len(values) <= 100000
- integers may be negative
- relative order of nonzero values must remain unchanged

## Examples

- `[0,4,0,2,7] -> [4,2,7,0,0]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Stable compaction is common in vectorized execution engines, sparse buffers and work queues. It also exposes the difference between logical deletion and physical movement.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
