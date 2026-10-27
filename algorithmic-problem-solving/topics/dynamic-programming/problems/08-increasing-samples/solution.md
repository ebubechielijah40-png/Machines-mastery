# Derivation: Retain a strictly increasing sample subsequence

## State, construction and correctness

E[i] is maximum chain length ending exactly at i. It is1 plus max E[j] over j<i with a[j]<a[i], or1 if none exists. Every chain ending at i has a legal predecessor or is a singleton. Attach i to the optimum such predecessor to attain the bound. The global answer is max E[i], not necessarily E[n−1]; parent pointers recover indices.

## Failed approach and counterexample

Using≤ changes the problem to nondecreasing order: [2,2] incorrectly becomes length2. Sorting samples loses the arrival-order constraint.

## Cost and boundary

O(n²) comparisons, O(n) state/parents/output. An O(n log n) tails method is a later extension with a different invariant.

The reference function is `lis` in [the shared executable library](../../code/dp.py);
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
