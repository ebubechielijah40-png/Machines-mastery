# Derivation: Reconcile an exact ledger amount

## State, construction and correctness

R[i,t] records reachability with the first i records. The last record is either absent or present once, so R[i,t]=R[i−1,t] OR R[i−1,t−v]. R[0,0] is true and other totals false. Every included transition moves to a previous item layer, even for v=0. Backtracking skips when the previous layer already reaches t, otherwise records i−1 and subtracts its value.

## Failed approach and counterexample

A single unlimited-coin recurrence makes [2] reach4 illegally. Conflating None with an empty tuple also loses the distinction between impossible and the valid empty solution.

## Cost and boundary

O(nT) Boolean transitions and O(nT) storage for this transparent witness implementation. Boolean-only reachability can use descending totals and O(T) cells, but witness history needs care.

The reference function is `subset_sum` in [the shared executable library](../../code/dp.py);
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
