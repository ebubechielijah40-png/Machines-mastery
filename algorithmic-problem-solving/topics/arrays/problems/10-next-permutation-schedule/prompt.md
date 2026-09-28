# Next Lexicographic Schedule

Difficulty: **intermediate**. Original repository exercise; learner NOT STARTED.

## Scenario

A deterministic test harness enumerates unique orderings of worker IDs in lexicographic order. Generate the next ordering without sorting every permutation globally.

## Task

Transform `values` in place into the next lexicographically greater permutation. If none exists, transform it into the smallest permutation. Return `True` if a greater permutation existed, else `False`.

## Constraints

- 0 <= len(values) <= 100000
- values are mutually comparable
- duplicates allowed

## Examples

- `[1,2,3] -> [1,3,2], True`
- `[3,2,1] -> [1,2,3], False`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

This is useful for exhaustive test generation and exposes lexicographic ordering as a state-transition system rather than a sorting problem.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
