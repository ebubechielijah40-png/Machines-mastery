# Derivation: Lay out a bounded technical label

## State, construction and correctness

T[i] is minimum penalty laying out words i onward. For each feasible first line i…j, add its squared slack (or0 for the final line) to T[j+1]. These first-break cases partition layouts. T[n]=0, and descending i makes each suffix available. Parent breaks reconstruct the exact layout. Spaces contribute j−i units to a line containing j−i+1 words.

## Failed approach and counterexample

Greedily filling the first line for [3,2,2,5],width6 gives lines(3,2),(2),(5), penalty16; moving the second word to the next line gives9+1=10. Charging the last line changes the objective.

## Cost and boundary

O(n²) candidate lines in the worst case and O(n) table/break storage. Prefix lengths or running used width avoid re-summing every candidate.

The reference function is `justify` in [the shared executable library](../../code/dp.py);
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
