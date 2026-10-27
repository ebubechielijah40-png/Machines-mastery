# Find a cheapest route with a hop budget

In a directed graph with n≥1, integer weighted edges, valid source/target and nonnegative hop budget, return minimum(cost,vertex_walk) using at most that many edges, or None. Repeated vertices and negative weights are allowed. A zero-edge source-to-itself walk is legal.

## Worked contract examples

0→1 cost−2,1→0 cost−2: source=target=0,hops2 →cost−4 and(0,1,0). hops0 givescost0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
