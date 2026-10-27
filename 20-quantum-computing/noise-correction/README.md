# From a pure state to noise, mixed states and limited correction

First complete [state vectors and measurement](../10_STATEVECTOR_MEASUREMENT.md).
That unit teaches complex amplitudes, tensor ordering, unitary gates, sampling
and projective collapse, with a bounded executable simulator. A single normalized
vector does not describe an unknown mixture of preparations or a subsystem whose
environment is ignored. This unit derives a one-qubit density model, then an
ideal three-qubit error-correction mechanism. No physical quantum hardware, cloud
job or empirical calibration was used. All outputs are exact synthetic model
calculations in floating-point arithmetic.

## 1. A histogram does not determine the state

Take the normalized vector |ψ⟩=√.8|0⟩+i√.2|1⟩. A Z-basis measurement has
probabilities(.8,.2). A classical preparation choosing |0⟩ with probability.8
and |1⟩ with probability.2 gives the same Z histogram. They are different
preparations: the pure vector has a relative phase that a suitable measurement
can reveal. No amount of Z-only shots identifies that missing information.

For a column ψ, form its outer product ρ=ψψ†. The dagger transposes and conjugates;
without conjugation the diagonal of a complex vector need not be a probability.
For the chosen vector,

\[
\rho_{pure}=\begin{pmatrix}.8&-.4i\\.4i&.2\end{pmatrix},\qquad
\rho_{mix}=\begin{pmatrix}.8&0\\0&.2\end{pmatrix}.
\]

To derive the first off-diagonal, multiply √.8 by the conjugate of i√.2 to get
−i√.16=−.4i. For a preparation distribution with probabilities w_j, average
outer products: ρ=Σw_j ψ_j ψ_j†, where w_j≥0 and Σw_j=1. Averaging vectors instead
would introduce interference between alternatives that were never coherently
prepared. Mixture descriptions need not be unique: equal mixtures of |0⟩/|1⟩
and of |+⟩/|−⟩ both give I/2 and have identical measurement predictions.

Apply U=(1/√2)[[1,−i],[1,i]], then measure in Z. This is a Y-basis measurement
on the original state. Uψ has first amplitude(√.8+√.2)/√2, squared magnitude.9;
the other outcome has probability.1. The mixture instead gives(.5,.5).
The executed experiment records those values. A basis change is an operation
needed to expose coherence, not a relabeling of the original Z counts.

## 2. What makes a matrix a physical state?

For one qubit, write ρ=[[a,c],[c*,b]]. The requirements are Hermiticity, trace1
and positive semidefiniteness. Trace gives a+b=1. Positivity means x†ρx≥0 for
every complex x, ensuring any basis measurement has nonnegative probability.
For a two-by-two Hermitian matrix, checking a≥0,b≥0 and ab−|c|²≥0 suffices.
For a>0, complete the square in x†ρx to obtain
`a|x0+(c/a)x1|² + (b−|c|²/a)|x1|²`; the a=0 case forces c=0. This justifies
the validator rather than trusting only diagonal probabilities. A matrix with
both diagonals.5 and off-diagonal1 has trace1 but a negative eigenvalue: it is
not a state.

Purity is Tr(ρ²)=a²+b²+2|c|². For a normalized pure vector, ρ²=ψ(ψ†ψ)ψ†=ρ, so
purity1. For the mixed example it is.64+.04=.68. A qubit density matrix has
purity between.5 and1; purity.5 is I/2. This scalar detects mixing but does not
identify a physical noise mechanism, and a pure state can still be the wrong
state for an intended computation.

A unitary gate transforms each vector as ψ→Uψ, so outer products transform as
ρ→UρU†. The simulator evaluates that product explicitly and compares it with
separately evolved vector amplitudes for100 seeded states. Input matrices are
validated without silent normalization or clipping, except probability outputs
are guarded against floating-point tolerance at zero/one. The declared numerical
validation tolerance is1e−10; it is not a quantum-device error bar.

## 3. Derive noise as an average of alternatives

A phase flip applies Z=diag(1,−1) with probability p and I otherwise. If the
outcome is unobserved, average states, not amplitudes:

\[
\Phi_Z(\rho)=(1-p)\rho+pZ\rho Z
=\begin{pmatrix}a&(1-2p)c\\(1-2p)c^*&b\end{pmatrix}.
\]

At p=.5, off-diagonals vanish. At p=1, a known Z is certain, so the output is
pure whenever the input was pure; phase information has changed predictably,
not become maximally uncertain. For our example, purity is .68+.32(1−2p)².
It falls to.68 at.5 and returns to1 at1. Calling p a continuously increasing
"amount of lost coherence" would therefore misdescribe this particular random
Pauli model. Noise parameters require a precise convention.

A general bounded channel here is specified by matrices K_j:
Φ(ρ)=ΣK_jρK_j†, with ΣK_j†K_j=I. Cyclic trace shows trace preservation:
TrΦ(ρ)=Tr(ρΣK_j†K_j)=Trρ. Positivity follows because each x†KρK†x is nonnegative;
the same construction remains positive on an extended entangled system. This is
why checking Kraus completeness is stronger than checking output trace for one
input. Our code rejects an invalid set such as a single2I rather than renormalize
a probability leak away. The IBM source map identifies the inspected channel
formulation; the matrix operations and tests are independently written.

Energy relaxation uses K0=diag(1,√(1−γ)), K1=[[0,√γ],[0,0]]. Their K†K sum is
identity. Multiplication gives

\[
\Phi_{relax}(\rho)=
\begin{pmatrix}a+\gamma b&\sqrt{1-\gamma}c\\
\sqrt{1-\gamma}c^*&(1-\gamma)b\end{pmatrix}.
\]

γ=1 sends every state to |0⟩, so a noisy physical process can increase purity.
Do not claim every nonunitary channel always reduces it. This is an idealized
zero-temperature channel parameter, not a measured T1 time, device temperature
or a combined thermal/dephasing calibration.

## 4. Encode a state without measuring its value

Encode α|0⟩+β|1⟩ as α|000⟩+β|111⟩. This is not three independent copies of an
unknown state: (α|0⟩+β|1⟩)⊗3 contains six other terms in general. The local vector
index is |q2 q1 q0⟩, with q0 the least significant bit, matching the earlier
simulator. Encoding preserves the two-dimensional logical information in an
eight-dimensional physical space.

Measure two parities s0=q0 XOR q1 and s1=q1 XOR q2. Both000 and111 have syndrome00.
A parity measurement therefore distinguishes error subspaces while leaving the
relative α/β inside a subspace unobserved. Directly measuring each data qubit
would reveal the logical bit and destroy the encoded superposition. The two
parity operators are Z0Z1 and Z1Z2, which commute.

| Error mask in q2q1q0 order | Syndrome(s0,s1) | Corrective operation |
| --- | --- | --- |
| 000 | (0,0) | I |
| 001 | (1,0) | X on q0 |
| 010 | (1,1) | X on q1 |
| 100 | (0,1) | X on q2 |

Our `recover` projects amplitudes by syndrome, computes each branch's norm²,
normalizes each branch separately, then applies the table's correction. It
returns a list of classical branches, not a coherent sum of their amplitudes.
For any encoded α,β and any single X error, syndrome is deterministic and the
correction recovers the entire complex superposition. Tests include unequal
amplitudes and a relative i phase; checking only logical000 would establish less.
The reference projects exactly in software; it does not construct noisy ancilla
measurement circuits or claim fault-tolerant physical control.

## 5. Why two errors and phase errors defeat the code

Two bit flips have the same syndrome as the complementary single error. The
correction then flips the third bit, turning000↔111, which is a logical X.
Three flips already do that with syndrome00. If independent physical X errors
occur with probability p per qubit in one cycle, failure needs at least two:

\[
p_L={3\choose2}p^2(1-p)+p^3=3p^2-2p^3.
\]

p_L−p=−p(2p−1)(p−1), which is negative for0<p<.5, zero at0,.5,1 and positive for
.5<p<1. Thus ideal repetition suppresses this error only in a specified regime.
At p=.1, p_L=.028; at.75 it is.84375, worse than an unencoded.75. The code's
computational function enumerates eight masks; the tests compare with this
independently simplified polynomial and with the resulting logical density
channel. It does not insert the answer polynomial as both model and oracle.

A Z on any one physical qubit sends α000+β111 to α000−β111. Its syndrome remains00.
For encoded|+⟩ this produces an orthogonal logical|−⟩, despite perfect bit-error
correction. This is a concrete counterexample to calling the repetition code
complete quantum error correction. Ancilla/gate/measurement faults, correlations,
leakage and repeated rounds are also absent; their overhead and failures cannot
be inferred from this one perfect correction cycle.

## 6. Execute a falsifiable, bounded investigation

Python3.10+ standard library, from repository root:

```sh
python3 -m unittest discover -s 20-quantum-computing/noise-correction -p 'test_*.py' -v
python3 20-quantum-computing/noise-correction/experiment.py
```

**Question:** can equal Z histograms hide different quantum behavior, and does
ideal X correction protect against arbitrary errors? **Hypotheses:** Y-basis
measurement separates the chosen preparations; repetition improves independent
X failure only below.5; one phase error can evade syndrome detection. **Controls:**
input state, basis ordering, perfect recovery and one cycle. **Changed variables:**
p and error type. **Instrumentation:** explicit complex matrices, trace/purity,
basis probabilities, syndrome branch norms and all eight error masks. There are
no shots or experimental sampling errors in these exact small calculations.

Actual [raw output](evidence/noise-experiment.json) records interpreter/platform,
matrices as(real,imag) pairs and probability sweeps. The coherent preparation
produced Y probabilities≈(.9,.1), the mixture≈(.5,.5). Phase-flip purities at
p0,.1,.5,1 were≈1,.8848,.68,1. Enumerated p_L at.1,.25,.75 was.028,.15625,.84375.
The phase-error counterexample had syndrome00 and squared overlap0 with the
original encoded|+⟩. These observations support our declared algebraic model,
not noise rates or useful-error thresholds of a physical device.

Nine [tests](evidence/tests.txt) include independent entry formulas, pure-state
gate agreement, every error mask, branch probabilities and invalid states/channels.
An initial equality assertion compared floating-point.7999999999999999 to.8
exactly; the corrected test uses a numerical tolerance consistent with the model.
No implementation change was hidden by broadening the physical claim.

Alternative explanations in a hardware experiment would include readout error,
SPAM, correlated noise and control faults; they do not exist in this exact model.
Follow-ups: inject a faulty correction with explicit probability; compare correlated
triple flips against independent errors with the same marginal p; add phase
protection in a different basis; derive a two-qubit density model and trace out
one half of a Bell state. None of those extended experiments is reported as run.

Attempt [EXERCISES.md](EXERCISES.md), then [HINTS.md](HINTS.md) and
[SOLUTIONS.md](SOLUTIONS.md). The [guided simulator project](../../projects-guided/p15-quantum-simulator/README.md)
connects the existing statevector and new channel builds. [SOURCES.md](SOURCES.md)
states exactly what primary documentation was inspected and what remains unavailable.
