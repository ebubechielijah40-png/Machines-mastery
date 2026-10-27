# Alignment exercises — attempt before hints

Use r=2, q=-1, g=-2 unless a task changes them. Store your prediction before running code. [Hints](HINTS.md) and [solutions](SOLUTIONS.md) are separate.

## Basic understanding

1. Score `A-G`/`ACG` by columns. Remove gaps and identify the consumed strings.
2. Fill the entire global table for `A` and `AC`, including the boundaries. What mistake results from a zero first row?
3. Explain why a last column has exactly three possibilities and why a gap/gap column is invalid.
4. With default code scores (1,-1,-1), list two optimum global alignments of `AA` and `A`. Which does the documented tie policy return?
5. Predict global and local outputs for empty/nonempty inputs and for local `AA` versus `CC`. Distinguish a score of zero from a unique alignment.

## Application

6. Derive the entire `AG`/`ACG` matrix from the recurrence, then reproduce the traceback without looking at the lesson's table.
7. Align `TTACGTAA` and `GGACGTCC` locally at (2,-3,-2). Give score, displayed strings, and zero-based half-open spans. Explain what each coordinate means.
8. At r=2, q=-5, g=-1, compare a mismatch against two adjacent opposing gaps for `A`/`C`. Should the code be changed or the scoring/model assumptions be documented? Defend your answer.

## Reasoning and debugging

9. A program returns the right optimum score but prints an alignment whose rescored columns differ. Give three possible bugs and a test that distinguishes them.
10. A colleague changes gap cost from kg to `open + (k-1)*extend` but leaves one score per prefix and the same three candidates. Construct two prefixes with equal scores but different future gap-extension costs. What state is missing?

## Challenge

11. Implement a two-row global score-only function. Explain which output capability it loses. Compare it with the independent exhaustive oracle on all binary strings of length at most 3; include empty strings. Do not copy the reference's row-filling code.

## Experiment

12. Predict the gap-sensitivity outcomes before reading `evidence/results.json`. Run the experiment. Explain why changing the model can change alignment and why the 90-permutation tail fraction is not evidence of biological function. Record one alternative null model and the question it would answer.

## Transfer and unaided reconstruction

13. An unknown text-diff system aligns lines instead of bases. Specify its alphabet, score model, boundaries, tie policy, resource limits, and provenance. Then close this repository, reconstruct global and local alignment from the final-column argument, and implement a five-case test set including ambiguity and a failure. Reopen and compare only after recording your attempt. Transfer understanding requires explaining the new problem's assumptions, not renaming variables.
