# Count monotone routes around blocked cells

Given a rectangular Boolean blocked grid, count paths from top-left to bottom-right moving only right or down. True cells are impassable. Count the singleton unblocked cell as one path. Empty dimensions give0.

## Worked contract examples

An open2×2 grid has2 routes. Blocking its start gives0. [[False]] gives1.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
