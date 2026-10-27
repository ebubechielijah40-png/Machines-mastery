# Count unordered replenishment bundles

For distinct positive denominations and an exact nonnegative target, count multiplicity vectors of unlimited denominations. Do not count permutations of the same bundle separately. No denominations and target0 has exactly one empty bundle.

## Worked contract examples

coins=[1,2], target3 →2: {1+1+1,1+2}. coins=[], target1 →0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
