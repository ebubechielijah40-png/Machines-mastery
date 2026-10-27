# Derivation: Count legal binary control records

## State, construction and correctness

Let Z,O count legal length-k strings ending in0 or1; at k=0 use Z=1,O=0 as the empty-prefix state. Appending0 is legal to both classes, giving Z′=Z+O. Appending1 is legal only after0, giving O′=Z. The classes stay disjoint and cover all legal extensions. Return Z+O after n steps.

## Failed approach and counterexample

Subtracting(n−1) forbidden positions from2^n double-counts strings containing several adjacent pairs. Replacing simultaneous updates with sequential assignment changes the recurrence.

## Cost and boundary

O(n) integer additions and two integer accumulators. Values have O(n) bits, so constant cell count is not constant bit space.

The reference function is `binary_no_adjacent` in [the shared executable library](../../code/dp.py);
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
