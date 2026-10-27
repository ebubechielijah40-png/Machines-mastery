# Choose a minimum-cost monotone inspection route

For a rectangular integer cost grid, move right/down from top-left to bottom-right, paying every visited cell including both endpoints. Return (cost,coordinate_path). Negative cell costs are allowed; empty dimensions return None.

## Worked contract examples

[[1,7],[2,1]] →cost4 through(0,0),(1,0),(1,1). [[−3]] →cost−3.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
