# Concrete implementation milestones

Each milestone requires an attempt, an explanation, and an observable output before opening the reference solution.

## A0 — represent and inventory

Run the starter on the synthetic fixture. Write a two-record parser contract: headers, upper/lower case, empty records, invalid symbols, duplicate names, and line breaks. Record the raw-byte hash. Change only FASTA line wrapping: sequence lengths should stay equal while byte identity changes. Explain why.

## A1 — model the objective

Manually score `A-G`/`ACG` at (2,-1,-2). Derive three possible final columns. Fill global boundaries and all six interior cells of the `AG`/`ACG` matrix. Expected final score is 2; a table alone is insufficient without the predecessor argument.

## A2 — global mechanism and invariants

Implement score filling and explicit traceback directions in a pure function. Independently rescore emitted columns; remove gaps and recover both inputs in order. Empty/empty must score zero. Default `AA`/`A` must return a reproducible tied optimum, with your tie policy stated. Inspect the reference only after your tests exist.

## A3 — local intervals

Change the state definition before changing code. Introduce zero boundaries, restart, maximum endpoint, and stop-at-zero traceback. Return zero-based half-open spans. The fixture at (2,-3,-2) must return `ACGT`/`ACGT`, score 8, both spans (2,6). Explain why using the bottom-right cell is now incorrect.

## A4 — integrate the bounded CLI

Accept a local file and explicit global/local mode. Read at most max_bytes+1 bytes so a growing file cannot defeat a prior stat check. Validate exactly two nonempty records. Enforce table-cell budget before allocation. Print JSON containing parameters, input/source hashes, strings, spans, and limits. On rejection return nonzero and no result JSON.

## B — independent verification and debugging

Run the [CLI integration tests](tests/test_workbench.py) and the biology oracle tests. Deliberately replace global boundaries with zeros in your own copy, then show an unequal-length counterexample. Deliberately forget traceback reversal and show why rescoring may pass while input-order reconstruction fails. Repair the cause and retain the failed transcript as evidence.

## C — controlled experiment

Predict gap sensitivity before running [the protocol](../../18-computational-biology/alignment/EXPERIMENTS.md). Keep strings, match, mismatch, implementation, and tie policy fixed. Measure all returned strings and scores. Identify the tie at gap=-4; change to -5 as a follow-up to resolve it strictly. Do not turn a toy score into an ancestry claim.

## D — bounded extension and reconstruction

Implement score-only two-row storage and verify it against the independent short-input path oracle. Compare measured memory with the full-table version on the same synthetic workloads. Explain the missing traceback information. Then reconstruct the original full-output algorithm from memory and apply it to a tiny line-diff problem with new score assumptions. Passing this milestone requires the derivation and test evidence, not a copied solution.
