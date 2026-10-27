# Minimum-cost one-to-one assignment

A square integer cost matrix gives the cost of assigning worker i to job j. Assign every worker to exactly one distinct job. Return(minimum_cost,jobs_by_worker). Negative costs are legal. Empty input costs0; n is bounded to16 by the implementation.

## Worked contract examples

[[4,1],[2,3]] →(3,(1,0)). [[−5]] →(−5,(0,)).

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
