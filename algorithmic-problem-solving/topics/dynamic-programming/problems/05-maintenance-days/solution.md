# Derivation: Choose nonadjacent maintenance days

## State, construction and correctness

B[i] is the best benefit in the first i days. Skip the last day for B[i−1], or take it and combine with B[i−2]. Bases B[0]=0 and missing earlier prefix=0 handle singletons. Every legal selection belongs to one case, and either candidate is legal. Backtracking decreases i by1 or2; clamping at0 avoids a negative-index loop.

## Failed approach and counterexample

Taking the largest remaining benefit and deleting its neighbors can fail: [4,5,4] has optimum8, not5. Summing all positive entries violates adjacency.

## Cost and boundary

O(n) arithmetic operations, O(n) table storage and O(n) returned indices. Only the objective can be computed in O(1) extra cells.

The reference function is `nonadjacent` in [the shared executable library](../../code/dp.py);
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
