# Minimum unit-cost text corrections

Return the minimum number of single-code-point insertions, deletions or replacements needed to transform string a into b. Each costs1; an unchanged character costs0. Return an integer distance, not an edit script.

## Worked contract examples

"kitten"→"sitting" costs3. "a"→"b" costs1. Empty→"ab" costs2.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
