# Reconcile an exact ledger amount

Choose each nonnegative integer record amount at most once to total target exactly. Return increasing original indices, or None. Zero-valued records and duplicates are legal. An empty witness solves target0.

## Worked contract examples

values=[2,2,5], target4 →(0,1). values=[2], target4 →None. [0,0], target0 →().

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
