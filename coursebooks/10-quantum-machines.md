# Quantum machines: amplitudes, observations, noise and limited recovery

The bounded path here begins with complex arithmetic and ends with an ideal
three-qubit correction experiment. It has original implementations, independent
oracles and raw executed evidence. Quantum algorithm families, compilation,
hardware modalities and research reproductions remain broader incomplete work;
no physical machine or quantum advantage is claimed.

## 1. A state is more than an outcome histogram

Begin the [statevector/measurement lesson](../20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md).
A qubit α|0⟩+β|1⟩ is a normalized complex column:|α|²+|β|²=1. Absolute squares give
Z measurement probabilities, but relative phase affects later interference.
H maps amplitudes by(α+β,α−β)/√2. Thus H;H returns|0⟩, while H;Z;H maps|0⟩ to|1⟩.
The Z in between changes a relative sign invisible to an immediate Z histogram
but visible after recombination. An arbitrary global phase changes no probabilities.

For nqubits the amplitude list has2^n entries. Index x means|q[n−1]…q0⟩ with q0
least significant. A one-qubit gate updates amplitude pairs that differ in one
bit; CNOT conditionally permutes basis entries. This explicit ordering prevents
an apparently normalized but wrong-endian implementation from passing silently.
The existing tests compare local transformations to an independent dense action
oracle on small states, rather than checking normalization alone.

## 2. Observation changes the object being modeled

Preparing many identical states and sampling each is different from repeatedly
measuring one specimen. Partial projective measurement groups amplitudes by the
observed bit, chooses a branch by its norm² and renormalizes only that branch.
A Bell state(|00⟩+|11⟩)/√2 has correlated outcomes; observing one bit removes the
other branch. Repeatedly measuring that same specimen does not produce fresh
independent Bell preparations. The lesson derives this distinction and records
an executed mechanism experiment with seeded synthetic sampling.

The public simulator rejects invalid norms/nonunitary gates and bounds n. It
models ideal pure states, not decoherence. Even a sparse-looking nqubit vector
requires exponential storage in this general representation. A classical teaching
simulation is not evidence that a physical device scales similarly or provides
a useful computational speedup.

## 3. Derive mixed states and expose hidden coherence

Continue to [density/noise/correction](../20-quantum-computing/noise-correction/README.md).
For pure columnψ,ρ=ψψ†; for a preparation mixture, average outer products with
classical probabilities. Do not average vectors as if independently chosen
preparations interfered. A valid density is Hermitian, trace1 and positive
semidefinite. For[[a,c],[c*,b]], a,b≥0 and ab≥|c|² give the2×2 positivity test.

The original example√.8|0⟩+i√.2|1⟩ has density[[.8,−.4i],[.4i,.2]] and the same Z
probabilities as diagonal mixture[[.8,0],[0,.2]]. A Y-basis operation followed by
Z measurement gives(.9,.1) for the pure state and(.5,.5) for the mixture. Thus
Z-only measurement is insufficient to identify coherence. PurityTrρ² is1 for
this pure state and.68 for the mixture, but purity alone cannot identify whether
a state is the intended one or determine a physical error mechanism.

## 4. Noise needs an exact probability convention

A random phase flip applies Z with probability p, giving(1−p)ρ+pZρZ. Diagonals
stay fixed; off-diagonals multiply by1−2p. Purity for the example is
.68+.32(1−2p)²: p.5 destroys its coherence, p1 is a certain known Z and restores
purity1. Increasing a phase-flip probability across the whole[0,1] interval is
not monotonically increasing uncertainty.

General local channels useΣKρK† with completenessΣK†K=I; this guarantees trace
preservation and the required positivity structure. Relaxation transfers excited
population into ground population while damping coherence. At full relaxation
every input becomes pure|0⟩, so a noise process need not always reduce purity.
The code validates channel completeness rather than concealing a wrong transform
by renormalization. Its floating-point tolerance is a numerical implementation
choice, not a hardware calibration uncertainty.

## 5. Recover a limited error without revealing the logical bit

Encode α0+β1 asα000+β111. It is not three independent copies; a tensor cube has
additional terms. Measure parities(q0 XOR q1,q1 XOR q2), whose values agree for
000 and111. The syndrome identifies the subspace of a single X error while
preserving the relative α/β within it. Direct data-bit measurement would reveal
the logical value and destroy its superposition.

The ideal recovery projects by syndrome, normalizes branches separately and
conditionally flips one physical bit. It recovers every single X error on an
unequal complex superposition in the tests. Under independent one-cycle X errors
with probability p, two/three errors become logical X, giving p_L=3p²−2p³.
At.1 this is.028, but at.75 it is.84375; improvement needs0<p<.5 and perfect
recovery assumptions. A Z error has syndrome00 and sends encoded|+⟩ to orthogonal
logical|−⟩. The code is therefore not complete quantum error correction.

## 6. Build, investigate and state what the evidence supports

The [guided simulator](../projects-guided/p15-quantum-simulator/README.md) preserves
its pure-state build and adds density/recovery milestones. The
[stack continuation](../projects-guided/quantum-machine-stack/README.md) connects
contracts, transformations, observations and noise while leaving unimplemented
hardware/compiler work explicit. Exercises, hints and checkable solutions are
separate. Reconstruct amplitude pairing, collapse, density validation, Kraus
application and syndrome recovery without opening reference code.

Nine new tests cover independent entry equations,100 seeded vector/density gate
comparisons, all eight error masks, branch probabilities and invalid inputs.
Executed exact calculations confirm the Y measurement difference, purity sweep,
error polynomial and invisible phase error. These are model calculations without
physical shots, readout errors or device statistics. Inspected IBM documentation
and original-source boundaries are recorded locally; no hardware lifetime or
paper benchmark was reproduced. A next honest extension adds correlated/faulty
recovery noise before generalizing error suppression to an engineering claim.
