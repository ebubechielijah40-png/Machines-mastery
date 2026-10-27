# Lay out a bounded technical label

Given positive word lengths and a nonnegative line width, break words into consecutive lines with one space between words. Minimize squared unused width on every line except the last, which costs0. Return(cost,half-open word-index ranges), or None if any word cannot fit.

## Worked contract examples

lengths=[3,2,2,5], width6 →cost10 with lines(0,1),(1,3),(3,4). Empty words →(0,()).

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
