# Merge Into a Reserved Storage Buffer

Difficulty: **hard**. Original repository exercise; learner NOT STARTED.

## Scenario

A storage page contains m sorted live entries followed by reserved empty slots. Another sorted run must be merged without allocating a third page.

## Task

`a` has length m+n; its first m values are sorted live entries and the remaining n slots are placeholders. `b` contains n sorted values. Merge b into a in place.

## Constraints

- m,n >= 0
- len(a)==m+len(b)
- live prefixes are nondecreasing

## Examples

- `a=[1,3,5,None,None,None], m=3, b=[2,4,6] -> [1,2,3,4,5,6]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Backward merge exploits reserved capacity and is directly related to in-place page maintenance in storage engines and fixed-capacity buffers.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
