# Statevector exercises — attempt before hints

Record your prediction and reasoning before executing code. These are ungraded preparation tasks until learner attempts exist. [Hints](HINTS.md) and [solutions](SOLUTIONS.md) are separate.

1. **Basic arithmetic.** Is `((1+i)/2,(1-i)/2)` normalized? Give the direct-read probabilities.
2. **Basic mechanism.** Compute H applied to `(sqrt(3)/2,1/2)` with both intermediate sums.
3. **Basic phase.** Compare `i*(1,1)/sqrt(2)` and `(1,-1)/sqrt(2)` to `|+>`. Which differences can affect a later H?
4. **Basic representation.** List the indices paired by a gate on q1 in a three-qubit array. Explain why there are four pairs.
5. **Basic conditional gate.** Trace CNOT(1,0) on `|10>`, `|11>` and `(|00>+i|10>)/sqrt(2)`.
6. **Application.** Derive P(1) after `H;diag(1,exp(i theta));H` and find angles giving P(1)=1/4 in `[0,2*pi)`.
7. **Application.** For `(1,i,-1,i)/2`, measure q1. Compute both branch probabilities and conditional vectors. Which amplitudes must retain their relative phase?
8. **Application/debugging.** A program obtains correct Bell probabilities but `X(0)|00>` gives `|10>`. Identify its bug and propose a test that Bell symmetry cannot hide.
9. **Reasoning.** Why can a measurement of deterministic q1 in `|0+>` leave q0 interference intact, while measuring q0 destroys that interference if its outcome is discarded?
10. **Reasoning.** Show that a normalized two-qubit product vector has `alpha00*alpha11-alpha01*alpha10=0`. Apply the test to the Bell state and to `(1,i,-1,-i)/2`. Explain the pure-state restriction.
11. **Challenge.** Write two-qubit amplitudes as `a[b,c]`, where b labels the remote qubit. A unitary U acts only on c. Prove `sum_c |sum_d U[c,d]*a[b,d]|² = sum_d |a[b,d]|²`. Interpret the result without claiming to transmit a selected random outcome.
12. **Experiment.** At p=1/2, repeat shot-count trials at 256 and 4096 using at least 30 independent pseudorandom streams. Predict the ratio of standard deviations, compute the observed ratio, and discuss seed reuse, sample variance and limited trial count. Keep raw seeds/counts. Do not expect every trial's error to shrink.
13. **Transfer.** Design a safe interface accepting a text circuit from an untrusted client. Specify preallocation limits, gate validation, timeout/cancellation, error reporting and at least three tests. Explain which of these are absent from this local simulator.
14. **Reconstruction from memory.** Close the implementation and lesson. Implement basis initialization, local unitary action, CNOT and one-qubit measurement. State the representation convention before coding. Reuse only the external behavior tests afterward; explain any failure before repairing it.
