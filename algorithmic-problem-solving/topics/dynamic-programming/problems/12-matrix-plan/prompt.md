# Plan a dense matrix multiplication chain

Given positive dimensions d of length n+1 for nonempty chain A0…A(n−1), return(minimum scalar multiplications,parenthesization). Ai has shape d[i]×d[i+1]. Use ordinary dense multiplication cost abc, without changing matrix order.

## Worked contract examples

d=[10,30,5,60] →4500, ((A0*A1)*A2). One matrix d=[2,3] costs0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
