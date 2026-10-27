# Derivation: Minimax tests for a monotone breakage threshold

## State, construction and correctness

Let R[e,m] be maximum number of floors resolvable. One drop creates a lower branch with e−1 probes,m−1 moves, the tested floor, and an upper branch with e probes,m−1 moves. Thus R[e,m]=R[e−1,m−1]+1+R[e,m−1], with zero floors for zero probes/moves. Any deeper decision tree is bounded by these branches, and placing the test immediately above the lower resolvable segment attains the bound. Increase m until R[E,m]≥F; descending e preserves old-move states.

## Failed approach and counterexample

Binary search assumes a broken probe can still be reused: with one probe it cannot discard the lower floors safely. Minimizing expected drops without a threshold distribution is a different objective.

## Cost and boundary

O(E M) additions and O(E) cells after capping E by F; M is the returned move count. With one probe M=F, so runtime is linear in numeric F, not log F.

The reference function is `egg_drop` in [the shared executable library](../../code/dp.py);
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
