# Derivation: Select one copy of each payload

## State, construction and correctness

K[i,c] is best value using the first i items and capacity c. Excluding item i−1 gives K[i−1,c]. Including it gives v[i−1]+K[i−1,c−w[i−1]] when it fits. These cases partition all feasible subsets. The better candidate is feasible and upper-bounds every feasible solution by induction on i. Backtracking compares adjacent rows, skipping an item on ties.

## Failed approach and counterexample

An ascending in-place capacity update can select the same item twice: weight2,value3,capacity4 returns6. A state indexed only by item number forgets remaining capacity.

## Cost and boundary

O(nC) comparisons/additions and O(nC) table storage; O(n) output. Capacity is a numeric magnitude, so the bound is pseudopolynomial in binary-encoded input.

The reference function is `knapsack` in [the shared executable library](../../code/dp.py);
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
