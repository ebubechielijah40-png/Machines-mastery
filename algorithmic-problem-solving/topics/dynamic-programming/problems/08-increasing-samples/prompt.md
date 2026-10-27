# Retain a strictly increasing sample subsequence

Given integer samples in arrival order, return indices of a longest strictly increasing subsequence. Indices must increase. Equal values cannot both extend a strictly increasing chain. Any optimum is acceptable.

## Worked contract examples

[3,1,2,2,4] has optimum length3. [2,2] has length1. Empty input returns().

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
