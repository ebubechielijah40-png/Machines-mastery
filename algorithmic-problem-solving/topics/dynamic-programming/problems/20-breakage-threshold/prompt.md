# Minimax tests for a monotone breakage threshold

There are floors1…F and a fixed unknown threshold from0…F. A drop above the threshold breaks the probe; a surviving probe can be reused. With E≥1 identical probes, find the minimum worst-case number of sequential drops needed to identify the threshold. Return only the optimal move count.

## Worked contract examples

E1,F10→10. E2,F10→4. E2,F100→14. F0→0.

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
