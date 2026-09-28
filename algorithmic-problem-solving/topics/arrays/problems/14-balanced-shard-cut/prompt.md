# Find Balanced Shard Cut Points

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

For a synthetic weighted array, a cut point is “balanced” when total weight strictly left equals total weight strictly right. Find every such candidate.

## Task

Return all indices i where sum(values[:i]) == sum(values[i+1:]).

## Constraints

- 0 <= len(values) <= 200000
- values may be negative

## Examples

- `[-7,1,5,2,-4,3,0] -> [3,6]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

The same conservation-style reasoning appears in load partitioning, checksums and streaming aggregates: derive an unseen remainder from a total and a prefix.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
