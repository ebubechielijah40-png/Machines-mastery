# Recover a common event order

Given two Unicode strings, return a longest common subsequence. Characters need not be adjacent but must keep order. Any longest witness is acceptable. Indices are Python code points, not grapheme clusters.

## Worked contract examples

"ABCBDAB" and"BDCABA" have optimum length4. "ab" and"ba" have optimum length1. Either input empty gives"".

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
