# Choose compatible weighted reservations

Each job is(start,end,value), with integer start<end and half-open occupancy[start,end). Select nonoverlapping jobs for maximum value; return(value,original_indices in time order). Equal endpoints are compatible; the empty set is permitted.

## Worked contract examples

[(0,2,4),(2,4,5),(0,4,8)] →value9, indices(0,1). All negative values →empty optimum.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
