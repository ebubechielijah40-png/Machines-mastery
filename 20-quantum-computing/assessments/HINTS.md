# Progressive hints

Attempt the [questions](EXERCISES.md) before reading further.

1–3: Multiply a number by its conjugate; keep amplitudes until the last step. A common factor commutes with every linear gate.

4–5: Write each index in binary. For a pair, only the addressed bit changes. CNOT's first argument is the control, not the leftmost displayed bit by definition.

6: Expand `(1-exp(i theta))*(1-exp(-i theta))` before using a trigonometric identity.

7: q1 partitions indices into `{0,1}` and `{2,3}`. Divide surviving amplitudes by the square root of that branch's total mass.

8–9: One is an address bug; the other distinguishes partial measurement from full-register sampling. Ask which labels the apparatus actually reveals.

10: Expand the four products `(ac,ad,bc,bd)`. A test for a pure vector is not automatically a test for a classical mixture.

11: Expand the squared magnitude into a sum over d and e; unitarity gives `sum_c U[c,d]*conj(U[c,e]) = delta[d,e]`.

12: The variance of an average of N independent Bernoulli(p) variables is `p*(1-p)/N`. Use one seed per stream and retain data rather than selecting a favorable trial.

13–14: Validate n before allocating `2**n`; an amplitude list may itself be an oversized input. A valid norm does not prove the gate or address was correct.
