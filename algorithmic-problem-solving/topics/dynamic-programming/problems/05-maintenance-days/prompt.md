# Choose nonadjacent maintenance days

Each day has an integer benefit. Choose days with no consecutive indices to maximize total benefit; return (benefit,indices). Choosing no days is legal. Negative benefits are not mandatory costs.

## Worked contract examples

[4,1,1,4] →(8,(0,3)). [-3,-2] →(0,()). [4] →(4,(0,)).

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
