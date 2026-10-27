# Derivation: Minimum unit-cost text corrections

## State, construction and correctness

D[i,j] is the minimum cost for prefixes. The final action is delete a[i−1], insert b[j−1], or match/replace both. Their candidate costs are D[i−1,j]+1, D[i,j−1]+1, D[i−1,j−1]+[a[i−1]≠b[j−1]]. Taking the minimum exhausts the final-action cases. Boundaries D[i,0]=i,D[0,j]=j are required. Each row depends only on itself to the left and the previous row, so two rows suffice.

## Failed approach and counterexample

Taking a maximum computes an expensive path rather than minimum correction. Replacement cost0 makes "a" and"b" distance0 and does not encode longest common subsequence; do not copy that source-note typo.

## Cost and boundary

O(mn) arithmetic operations, O(n) auxiliary cells where n=len(b). Input/output strings and code-point versus user-perceived-character semantics are separate costs.

The reference function is `edit_distance` in [the shared executable library](../../code/dp.py);
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
