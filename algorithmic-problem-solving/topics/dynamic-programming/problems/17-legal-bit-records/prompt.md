# Count legal binary control records

Count binary strings of length n≥0 with no adjacent1 bits. Leading zeros are meaningful and permitted. There is one empty length0 record. Return an exact integer.

## Worked contract examples

n0→1,n1→2,n2→3,n3→5. For n2 the records are00,01,10.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
