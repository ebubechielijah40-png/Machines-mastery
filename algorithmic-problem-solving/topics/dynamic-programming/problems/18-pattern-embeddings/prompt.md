# Count ordered pattern embeddings

Count choices of distinct increasing source indices whose characters spell pattern. Equal resulting text at different indices counts as a different embedding. Empty pattern has one embedding in any source.

## Worked contract examples

"aaaa" contains pattern"aa" in6 index pairs. "abc" contains"ac" once. Empty source with pattern"a" gives0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
