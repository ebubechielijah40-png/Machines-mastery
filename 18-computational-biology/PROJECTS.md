# Computational biology project ladder

Each project has A0–A3 assistance. Do not begin with the reference path unless blocked.

## CB-1 Sequence workbench
Build a CLI that reads FASTA, reports composition, reverse complement, motif counts, and k-mer spectra. Add property tests and malformed-input tests.

**A0 acceptance:** deterministic output, streaming-friendly design explanation, tests for empty/ambiguous sequences, and a provenance log.

**A1 prompts:** What does `N` mean? Should it contribute to GC denominator? What complexity does k-mer counting have? How will you prevent loading multi-GB files at once?

**A2 scaffold:** parser → record iterator → analysis functions → CLI → tests.

**A3 reference:** use `code/sequence_lab.py` only after attempting your design; then rebuild a streaming version independently.

## CB-2 Alignment engine
Implement Needleman–Wunsch, traceback, affine-gap extension as optional depth, tests against hand-worked examples, and runtime/memory experiments. Explain why scoring assumptions determine the “best” alignment.

## CB-3 Variant evidence pipeline
Using synthetic reads/variants, model reference coordinates, evidence counts, quality filters, and provenance. Do not claim clinical interpretation. Introduce mapping ambiguity and sequencing-error simulations.

## CB-4 Population genetics simulator
Simulate drift/selection/migration. Compare empirical distributions to expectations and show how population size changes variance.

## CB-5 Gene-regulatory dynamics
Implement deterministic ODE simulations for expression/degradation/feedback, numerical-step sensitivity tests, and parameter-identifiability discussion.

## CB-6 Reproducible public-data study
Choose a public non-sensitive dataset, freeze identifiers/versions, construct an analysis pipeline, record transformations, use a holdout strategy that matches the scientific question, and write a limitations section.
