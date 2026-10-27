# Count true Boolean parenthesizations

Given a nonempty list of actual Boolean literals and exactly one fewer operators from &,|,^, count complete binary parenthesizations evaluating to True. Literal/operator order is fixed; all operators are binary. This is counting syntax trees, not evaluating standard language precedence.

## Worked contract examples

[True,False,True] with["^","|"] has1 true plan. A single False has0. Two True joined by^ have0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
