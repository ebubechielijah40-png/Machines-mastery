# Minimum standard packages

A warehouse has unlimited packages of each distinct positive integer size. Fill exactly target units using the fewest packages; return their sizes, or None when impossible. Different orders are equivalent. Any optimum witness is acceptable.

## Worked contract examples

coins=[1,3,4], target=6 → (3,3). Target0 → (). coins=[4,6], target5 → None.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
