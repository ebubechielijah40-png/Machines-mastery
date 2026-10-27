# Derivation: Count ordered pattern embeddings

## State, construction and correctness

After scanning a source prefix, W[j] counts embeddings of pattern[:j]. W[0]=1. If current source char matches pattern[j−1], embeddings using it are in bijection with previous-prefix embeddings of length j−1. Add that number. Process j descending so the previous-prefix count has not yet incorporated the current source character. Existing embeddings account for skipping it.

## Failed approach and counterexample

Ascending j makes source"a" embed pattern"aa" once by reusing the same position. Using a set of matched strings loses multiplicity: "aaaa" would have only one textual"aa".

## Cost and boundary

O(mn) character comparisons/additions and O(n) integer cells, where n is pattern length. Exact counts can require many bits.

The reference function is `subsequence_count` in [the shared executable library](../../code/dp.py);
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
