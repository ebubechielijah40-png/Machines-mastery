# Stable Compaction of Deleted Records

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

An append-only staging buffer marks deleted entries with `None`. Before flushing to disk, remove tombstones while preserving the relative order of live records.

## Task

Mutate `values` so all non-None entries occupy the prefix in original order. Fill the remaining suffix with `None` and return the number of live entries.

## Constraints

- 0 <= len(values) <= 100000
- live values may be falsey such as 0 or empty strings
- only None is a tombstone

## Examples

- `[3,None,4,None,5] -> [3,4,5,None,None], return 3`
- `[None,None] -> unchanged, return 0`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

Log compaction, garbage collection, packed columnar buffers and GPU work queues all repeatedly convert sparse logical occupancy into dense storage.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
