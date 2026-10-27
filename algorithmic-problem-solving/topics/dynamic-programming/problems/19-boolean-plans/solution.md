# Derivation: Count true Boolean parenthesizations

## State, construction and correctness

For each interval retain(F,T), counts of false and true trees. A singleton contributes exactly one tree in its literal class. For every outer split, combine each left/right truth pair with the connecting operator, adding the product of their counts to the resulting truth class. Every syntax tree has one outer split, so no tree is missed or counted twice. Evaluate increasing interval length.

## Failed approach and counterexample

Evaluating only left-to-right picks one syntax tree. Counting valid left trees plus right trees is wrong; each left tree pairs with every right tree, so multiply.

## Cost and boundary

O(n³) arithmetic operations, O(n²) pairs of integer counts; Catalan growth makes integer-bit cost significant. This function is not Python eval.

The reference function is `boolean_parenthesizations` in [the shared executable library](../../code/dp.py);
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
