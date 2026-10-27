# Derivation: Recover a common event order

## State, construction and correctness

L[i,j] is maximum common-subsequence length of a[:i],b[:j]. Matching final symbols can extend an optimum diagonal prefix by1; an optimum of that length exists using the matched pair. For unequal finals, every common sequence omits at least one final position, so take max of the upper and left cells. Zero-length prefixes give0. Trace diagonal matches or a neighbor retaining the optimum.

## Failed approach and counterexample

Longest common substring is a different problem: "ace" is a subsequence of"abcde" without being contiguous. Character-set intersection discards order and multiplicity.

## Cost and boundary

O(mn) time/cells for witness recovery, plus output length at most min(m,n). A length-only rolling-row version need not store all cells.

The reference function is `lcs` in [the shared executable library](../../code/dp.py);
[solution.py](solution.py) exposes that implementation as `solve` without a second
copy. [The independent suite](../../code/test_dp.py) compares complete small
search spaces or alternative formulations, in addition to the local fixed-contract
test. None of these finite checks replaces the displayed general argument.

## Reconstruction and transfer

Close the implementation, derive the state/base/order again, rebuild it and write
a fresh witness/negative test. Then change the constraint named above and explain
whether the state still contains everything needed for the next decision.

These are original teaching statements for established methods; the selected
[primary-source map](../../SOURCES.md) distinguishes direct source scopes from
independently derived extensions.
