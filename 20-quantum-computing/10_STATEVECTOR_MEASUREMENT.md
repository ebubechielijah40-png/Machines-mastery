# From complex amplitudes to a measured bit

This is a bounded, executable lesson on ideal pure states. It teaches the model that the simulator actually implements, rather than treating a successful Bell circuit as an explanation of a physical quantum computer. Read the [prerequisite check](STATEVECTOR_PREREQUISITE_BRIDGE.md), attempt the [exercises](assessments/EXERCISES.md), then use the [guided build](../projects-guided/p15-quantum-simulator/README.md). The next hardware, noise, algorithms and error-correction chapters remain partial.

## 1. Why keep amplitudes instead of probabilities?

Suppose a machine prepares a bit that reads 0 or 1 equally often. A list `(0.5, 0.5)` predicts a direct reading. Does it predict what happens after another operation? No: two quantum preparations can have that same distribution and yield opposite definite outcomes after the same gate. To model that experiment, the internal state must retain more than direct-read probabilities. Here we accept the finite-dimensional pure-state postulates as the model [Q1]; they are not derived from classical probability or proved to describe nature by this program.

A complex number is `z = a + bi`, with `i*i = -1`; its conjugate is `z* = a - bi`. Multiplication gives `z* z = a*a + b*b`, a nonnegative real number. Write this as `|z|²`. An amplitude is dimensionless. It is neither a voltage nor the chance of observing a negative event.

A one-qubit pure state is a column vector

\[
|\psi\rangle = \begin{pmatrix}\alpha\\\beta\end{pmatrix}
=\alpha|0\rangle+\beta|1\rangle,\qquad |\alpha|^2+|\beta|^2=1.
\]

A ket `|0>` names the vector `(1,0)` and `|1>` names `(0,1)`. It does not add a mysterious operation to the vector. A computational-basis measurement returns 0 with probability `|alpha|²`, or 1 with probability `|beta|²` [Q1, “Measuring quantum states”]. This is an assumed measurement law; normalization makes the two probabilities sum to one.

**Worked arithmetic.** Choose `alpha = (2+i)/3` and `beta = 2/3`. The squared magnitudes are `(4+1)/9 = 5/9` and `4/9`; total one. Choosing `alpha=beta=1` is invalid because the total is two. Dividing both by `sqrt(2)` changes it to a valid state. The constructor rejects invalid input rather than hiding this mistake through automatic normalization.

## 2. How a gate changes a state

A single-qubit gate is a complex 2 by 2 matrix. If its entries are `u00,u01,u10,u11`, multiplication means

\[
\alpha'=u_{00}\alpha+u_{01}\beta,\qquad
\beta'=u_{10}\alpha+u_{11}\beta.
\]

For an isolated ideal system we restrict gates to unitary matrices [Q1, “Unitary operations”]. A dagger means transpose and conjugate. The condition is `U†U=I`. The reason that this is a useful invariant follows by multiplication:

\[
\|U\psi\|^2=(U\psi)^\dagger(U\psi)
=\psi^\dagger U^\dagger U\psi=\psi^\dagger\psi=1.
\]

The inverse is `U†`; applying it undoes the ideal gate. No energy conservation claim follows from this norm invariant: these amplitudes are not energies. Gate duration, pulse energy and thermal environment are outside this mathematical model.

The useful gates in the reference are

\[
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]

`X` swaps two amplitudes. `Z` changes the second amplitude's sign without changing either squared magnitude. `H` adds and subtracts amplitudes. For example,

\[
H|0\rangle=\frac1{\sqrt2}(1,1)^T,\quad
H\frac1{\sqrt2}(1,1)^T=(1,0)^T,
\]

because `(1+1)/2=1` and `(1-1)/2=0`. But inserting `Z` makes the middle vector `(1,-1)/sqrt(2)`; the last `H` then gives `(0,1)`. Cancellation occurs in amplitudes before squaring. Adding probabilities instead would predict 50/50 twice and miss the interference.

**Broken implementation.** Updating `alpha` and then computing `beta` from the changed `alpha` implements a different matrix. The pair loop must save both old values first. A norm check on only `|0>` is insufficient for validating a proposed gate: `diag(1,2)` preserves that one state but fails on `|1>`. The code checks the inner products of both columns, including their cross inner product.

## 3. Global phase, relative phase and an experiment to separate them

Multiplying every amplitude by the same `exp(i*theta)` preserves direct probabilities, because its magnitude is one. Any later linear gate preserves that common factor: `U(exp(i theta) psi)=exp(i theta) U psi`. Thus common phase cannot affect any circuit's final computational-basis probabilities within this model. This is a derivation from the adopted postulates, not evidence from a physical device.

Relative phase behaves differently. Apply `H`, then `diag(1,exp(i theta))`, then `H` to `|0>`. The intermediate state is `(1,exp(i theta))/sqrt(2)`. Final amplitudes are

\[
\alpha'=(1+e^{i\theta})/2,\qquad
\beta'=(1-e^{i\theta})/2.
\]

Multiply the latter by its conjugate:

\[
P(1)=\frac{(1-e^{i\theta})(1-e^{-i\theta})}{4}
=\frac{2-2\cos\theta}{4}=\sin^2(\theta/2).
\]

At `theta=0, pi/2, pi`, predicted probabilities are `0, 1/2, 1`. These are the fixed predictions recorded before interpreting the [phase-sweep experiment](experiments/MEASUREMENT.md). An experiment that only measures the state before the final `H` cannot distinguish these relative phases: every case has probability `1/2` for each bit there.

## 4. Two qubits: tensor products and an address convention

Independent preparations combine by a tensor product [Q2, “Tensor products of quantum state vectors”]. With qubit 1 vector `(a,b)` and qubit 0 vector `(c,d)`, expand distributively:

\[
(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle)
=ac|00\rangle+ad|01\rangle+bc|10\rangle+bd|11\rangle.
\]

The array is therefore `(ac,ad,bc,bd)`. For example `(sqrt(3)/2,1/2)` on qubit 1 and `(1,i)/sqrt(2)` on qubit 0 gives `(sqrt(3)/(2 sqrt(2)), i sqrt(3)/(2 sqrt(2)), 1/(2 sqrt(2)), i/(2 sqrt(2)))`. Probabilities are `(3/8,3/8,1/8,1/8)`, summing to one.

The simulator uses index `x = sum(bit[q] * 2**q)`. Displayed basis strings have qubit `n-1` on the left and qubit 0 on the right. This convention agrees with the inspected IBM statevector/index documentation [Q3]; other software can choose differently.

| Array index | Basis string | Qubit 1 | Qubit 0 |
| --- | --- | --- | --- |
| 0 | 00 | 0 | 0 |
| 1 | 01 | 0 | 1 |
| 2 | 10 | 1 | 0 |
| 3 | 11 | 1 | 1 |

`X` on qubit 0 changes `|00>` to `|01>`, while `X` on qubit 1 changes it to `|10>`. Swapping these is a representation bug that a Bell-only test can miss. A Bell state's symmetric probabilities look identical after swapping the two labels.

For a local gate on qubit `q`, pair every index `i` whose `q` bit is zero with `j=i+2**q`. All other bits agree. Apply the 2 by 2 matrix to that pair. Each amplitude appears exactly once, so the gate costs `O(2**n)` time, `O(1)` extra working state, in addition to the array. The implementation's validation also scans the array, retaining this time bound.

## 5. Conditional gates and a complete Bell trace

CNOT flips its target bit if its control bit is one [Q3, “Gates”]. It is a permutation of amplitudes, not a measurement of the control. For `control=0,target=1`, the permutation is `00->00`, `01->11`, `10->10`, `11->01`. A different control/target order gives a different permutation.

Start with `|00>` and follow the actual array:

| Stage | Amplitudes at indices 0,1,2,3 | Explanation |
| --- | --- | --- |
| Prepare | `(1,0,0,0)` | Both qubits start in 0 |
| `H` on q0 | `(1/sqrt(2),1/sqrt(2),0,0)` | Pair indices 0/1 and 2/3 |
| `CNOT(0,1)` | `(1/sqrt(2),0,0,1/sqrt(2))` | Index 1 moves to index 3 |
| Direct probabilities | `(1/2,0,0,1/2)` | Square magnitudes |

The last state is entangled: it cannot factor as `(a,b) tensor (c,d)`. If it did, both `ac` and `bd` would be nonzero while `ad=bc=0`. Nonzero `ac,bd` require all four factors nonzero, contradicting the zero cross terms. This elementary proof concerns this pure state. Correlated observed bit pairs alone do not prove entanglement.

An ordinary probabilistic mixture preparing `|00>` half the time and `|11>` half the time gives the same direct-read distribution. To distinguish that mixture from the Bell state, apply `H` to both qubits and then read. Expanding the Bell state gives the same Bell state, with equality probability one. Each mixture component instead gives four equally likely outcomes after these gates, so the average equality probability is `1/2`. The code computes the mixture as weighted probabilities of separate preparations, never as an invented “averaged amplitude vector.” This is a model discrimination experiment, not a loophole-free Bell inequality test.

## 6. Partial measurement must preserve what was not measured

Measuring one qubit does not read the complete array. For outcome `b` on qubit `q`, sum probabilities of compatible basis states [Q2, “Partial measurements”]:

\[
p_b=\sum_{x:\,\operatorname{bit}_q(x)=b}|\alpha_x|^2.
\]

Then sample `b` according to these two masses. Conditional on observing it, zero incompatible amplitudes and divide compatible amplitudes by `sqrt(p_b)`. Division by the square root is necessary because squared magnitudes, rather than amplitudes, must sum to one:

\[
\alpha'_x=\begin{cases}\alpha_x/\sqrt{p_b}&\operatorname{bit}_q(x)=b,\\0&\text{otherwise}.\end{cases}
\]

**Worked branch.** Use amplitudes `(sqrt(.1), i sqrt(.2), -sqrt(.3), sqrt(.4))`. Measure q0. The zero branch comprises indices 0 and 2, so `p0=.1+.3=.4`. If zero appears, the new vector is `(1/2,0,-sqrt(3)/2,0)`, with squared norm `1/4+3/4=1`. For the one branch `p1=.6`, the vector is `(0,i/sqrt(3),0,sqrt(2/3))`. The unmeasured q1 remains coherent within each branch.

For the Bell state, reading q0 yields zero or one with equal probability and leaves `|00>` or `|11>` respectively. A second q0 reading repeats the first; q1 agrees. You cannot choose the random first result to send a chosen bit. More generally, a unitary on one subsystem leaves the other subsystem's marginal measurement distribution unchanged; the experiment checks one instance, while exercise 11 derives the algebra.

An important edge case is `p_b=0`: there is no conditional state for an impossible observation. `collapse` rejects it before mutation. A tiny positive branch is mathematically valid; the code does not arbitrarily discard it using a probability tolerance. Extremely tiny amplitudes can nevertheless underflow in floating point, a genuine numerical limitation.

**Sampling is a different API.** `sample(100,seed=0)` represents 100 freshly prepared copies, leaves amplitudes unchanged, and returns whole-register indices. `measure(q,rng=...)` represents one projective observation of one specimen and changes it. `collapse(q,b)` is deterministic conditional calculation; it is not the ability to force an outcome on hardware. Repeatedly resetting a pseudorandom seed does not produce independent experimental streams. Use one `random.Random` object through `rng` for a sequence of measurements.

## 7. Implementation, invariants and debugging

The runnable reference is [simulator.py](code/simulator.py); [tests](code/test_simulator.py) use standard-library `unittest`. Its public invariants are: `len(amp)==2**n`, finite numeric amplitudes, squared norm within `1e-10` of one, valid qubit addresses, a unitary 2 by 2 local gate, and distinct CNOT addresses. Invalid inputs raise before gate mutation. `norm()` retains its historical name but returns **squared** Euclidean norm. `probs()` intentionally returns raw squared magnitudes for diagnosis, even after invalid public-list mutation; transformations and observations validate first.

Run from the repository root:

```sh
python3 20-quantum-computing/code/test_simulator.py
python3 20-quantum-computing/code/measurement_experiment.py
```

The dense test oracle constructs each output amplitude by summing over all input indices, agreeing on non-target bits. It uses different loops than the optimized pair update. Tests also exhaust all basis states for every distinct 3-qubit CNOT pair, test a complex phase-bearing gate, check partial collapse without destroying unrelated coherence, and reject invalid gates and addresses. These are independent checks of bounded cases, not a proof covering every floating-point circuit.

| Symptom | Likely defect | Discriminating observation |
| --- | --- | --- |
| `H;H` does not undo | Saved only one old amplitude | Compare against dense matrix multiplication |
| Norm preserved but wrong qubit flips | Endian/address convention | Test `X` on each address separately |
| Bell state stays unchanged after CNOT twice, but first CNOT wrong | Faulty permutation can be involutory | Exhaust basis truth table, not only inverse test |
| Measuring deterministic q1 destroys q0 interference | Collapsed entire register | Prepare `|0+>`, read q1, apply H on q0 |
| Shot results sometimes omit a sample | Cumulative floating-point tail | Assert output length and use a nonzero fallback bin |
| Forced impossible branch divides by zero | Missing probability check | Condition `|0>` on outcome one |

## 8. Cost, trust boundary and limits

An n-qubit dense state needs `2**n` complex amplitudes. A hypothetical packed complex128 array alone needs `16*2**n` bytes: 20 qubits use 16 MiB and 30 use 16 GiB, before any overhead. This Python list uses additional memory; the numbers are representation arithmetic, not measured process memory. The included process caps n at 20 before allocation. A serialized vector can still consume resources while being supplied to `from_amplitudes`; do not expose this teaching API directly to untrusted network input.

`sample(S)` costs `O(S*2**n)` in this deliberately simple implementation. A cumulative table and binary search could reduce repeated selection cost; first establish matching probabilities and deterministic semantics. Shared mutable states are not thread safe. A production service would additionally need request budgets, isolation, cancellation, API versioning and input-size checks before parsing. No such service is deployed here.

Floating-point tolerance permits small norm drift; no claim is made about long circuits or rigorous error bounds. This simulator omits density matrices, channels, decoherence, readout errors, leakage, pulse control, calibration, error correction and quantum algorithm speedups. Computing many amplitudes classically is not a quantum advantage result. The observed measurements here verify implementation behavior against equations, not the physics postulates or a research paper's hardware results.

Continue with the [assessment](assessments/EXERCISES.md), then reconstruct the core without looking at the reference. Source identities and inspected sections are in [SOURCE_VERIFICATION.md](SOURCE_VERIFICATION.md); executed evidence and interpretation are in [the experiment record](experiments/MEASUREMENT.md).
