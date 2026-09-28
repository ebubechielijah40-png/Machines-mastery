# Apply Bulk Range Load Updates

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A capacity planner receives many updates saying “add delta to every minute in [start,end]”. Applying each update cell-by-cell is too slow.

## Task

Given array length n and inclusive updates `(start,end,delta)`, return the final values after all updates. Initially every position is zero.

## Constraints

- 0 <= n <= 200000
- 0 <= len(updates) <= 200000
- 0 <= start <= end < n

## Examples

- `n=5, [(1,3,2),(2,4,-1)] -> [0,2,1,1,-1]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Difference arrays model batched counters, reservation windows and offline range updates. They are the discrete derivative/integral pair of prefix sums.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
