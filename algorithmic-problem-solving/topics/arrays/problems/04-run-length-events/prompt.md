# Run-Length Encode Repeated Events

Difficulty: **basic**. Original repository exercise; learner NOT STARTED.

## Scenario

A telemetry stream often contains long runs of the same categorical state. Compress consecutive repeats without changing sequence semantics.

## Task

Return a list of `(value,count)` pairs describing maximal consecutive runs.

## Constraints

- 0 <= len(values) <= 100000
- equal values are grouped only when adjacent

## Examples

- `["OK","OK","WARN","WARN","OK"] -> [("OK",2),("WARN",2),("OK",1)]`

## Before coding

Write down: (1) the simplest correct method you can think of, (2) its time and auxiliary-space costs, (3) the invariant that would let you know a one-pass or in-place method is correct, and (4) one input that could make a naive implementation slow.

## Real-system transfer

RLE is used in bitmap formats, column encodings, state traces and sparse event timelines. The key distinction is local repetition versus global frequency.

## Follow-up

After solving, change one constraint (streaming input, immutable input, external memory, concurrency, or bounded memory) and state whether your algorithm still applies. Do not read `solution.md` until you have an attempt.
