# Select one copy of each payload

Given parallel positive integer weights and integer values, choose a subset of item indices with total weight at most capacity and maximum value. Return (value,indices). Items are distinct even when their weights match. The empty subset is permitted; ties may return any optimum.

## Worked contract examples

weights=[2,3,4], values=[4,5,7], capacity5 → value9 with indices(0,1). One item(weight2,value3), capacity4 → value3.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
