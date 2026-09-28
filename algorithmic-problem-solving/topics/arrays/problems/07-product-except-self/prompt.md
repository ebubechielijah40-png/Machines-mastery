# Per-Sensor Product Without Self

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A calibration stage needs, for each sensor, the product of all other gain factors. Division is forbidden because zeros are valid gains in the synthetic model.

## Task

Return an array where output[i] equals the product of all input values except values[i], without division.

## Constraints

- 2 <= len(values) <= 100000
- integer arithmetic
- zeros and negative values allowed

## Examples

- `[1,2,3,4] -> [24,12,8,6]`
- `[0,2,3] -> [6,0,0]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Prefix/suffix decomposition is a general technique for removing one contribution from an aggregate without recomputing the entire aggregate.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
