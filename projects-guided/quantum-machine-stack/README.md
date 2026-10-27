# Connect quantum state, observation, noise and correction

Build a bounded local path from complex amplitudes to a density matrix, a
synthetic channel and an ideal repetition-code recovery. This project now has
an executable integration reference, actual output and tests. Algorithm families,
native-gate compilation, pulses, cooling, device readout and architecture dossiers
remain broader stack work; they are not implied by the completed mathematical
kernels. No cloud account, physical qubit or quantum advantage is required/claimed.

## Prerequisites and architecture

Complete [statevector/measurement](../../20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md)
and [density/noise/correction](../../20-quantum-computing/noise-correction/README.md)
in that order, using [the guided simulator](../p15-quantum-simulator/README.md)
for staged construction. Both lessons introduce their mathematics before use,
with worked cases, separate exercises/hints/solutions and source-verification
records. Python3.10+ standard library is sufficient.

A vector contains coherent amplitudes; an outer product yields a pure density.
A gate can evolve the vector or transform the density as UρU†. These routes must
agree before adding noise. A Kraus channel averages physical alternatives with
validated completeness. The encoded three-qubit state preserves logical complex
amplitudes, parity projection returns classical branches, and a conditional X
corrects a single bit flip without observing the logical value.

## Six derivation and implementation milestones

1. Derive local amplitude pairing and implement an ideal gate/CNOT/measurement
   using the existing simulator project. State q0's least-significant position.
   Use dense small-state oracles, not normalization alone.
2. For√.8|0⟩+i√.2|1⟩, hand-computeρ=[[.8,−.4i],[.4i,.2]]. Derive Hermiticity,
   trace and2×2 positivity checks. Reject an invalid trace1 matrix rather than
   silently normalizing it into a different model.
3. Apply H as both vector action and UρU†, compare all entries, and explain why
   equal final Z probabilities would be a weaker check. Then compare the coherent
   input and diagonal mixture in Y basis, predicting(.9,.1) vs(.5,.5).
4. Derive the random-Z channel. Predict at p.5 coherence disappears and purity
   becomes.68; at p1 the known Z preserves purity1. Check Kraus completeness
   independently and reject a scaled2I operator.
5. Encode an unequal complex superposition, inject an X on q1 and derive
   syndrome(1,1). Project/normalize its branch and correct. Test every error mask;
   compare enumerated logical error with3p²−2p³ and show the invisible Z failure.
6. Close references and reconstruct all contracts. Then add a declared correlated
   XXX model or faulty correction probability. Predict the changed logical error
   before coding; do not report that extension as run until its evidence exists.

The [reference runner](run_stack.py) connects the original kernels and emits
source hashes/platform plus each bounded mechanism result. It is a checkpoint
after an attempt, not a complete answer to every quantum-stack objective.

## Execute and assess

```sh
python3 projects-guided/quantum-machine-stack/run_stack.py
python3 -m unittest discover -s projects-guided/quantum-machine-stack -p 'test_*.py' -v
python3 -m unittest discover -s 20-quantum-computing/noise-correction -p 'test_*.py' -v
```

[Actual JSON](evidence/stack.json) records vector/density residual near floating
roundoff, phase-flip purity≈.68, syndrome(1,1), recovery overlap≈1 and enumerated
logical X probability.028 for independent physical p.1.
[One integration test](evidence/tests.txt) passed; the underlying channel/recovery
suite has nine independently grounded tests and the preserved statevector suite
has eighteen. [VALIDATION.md](VALIDATION.md) states those scopes.

Deliver original implementations, hand matrices, parity table, independent tests,
prediction/raw-output records, failure analysis and memory reconstruction. Rubric:
25points representation/contracts,25 independent gates/channels/recovery tests,
20 mathematical derivation,20 honest experiment interpretation,10 reconstruction.
A wrong bit convention, coherently summed measurement branches, unexamined
noise assumptions or invented device observation prevents a successful build.

## Engineering consequences and limits

A general nqubit vector uses2^n amplitudes; a full density uses4^n entries. The
new density engine intentionally handles one qubit, and recovery handles three;
this bounded design teaches the mechanism without allocating a large matrix.
A cycle/entry count is not a physical gate time. Fixed tolerances are not measured
calibration errors, and exact matrix probabilities are not experimental shots.

The runner reads local code and synthetic constants, writes JSON to stdout and
uses no network. Any service for untrusted circuits would require bounded parsing,
isolation, total gate/shot budgets and policy separate from these kernels.
Real hardware adds control faults, readout, reset, leakage, correlations and
measurement latency. Perfect software parity projection does not establish
fault tolerance when its own machinery can fail. Sources are linked in the two
unit verification records; no copyrighted textbook chapter or source hardware
plot is redistributed as our evidence. The full quantum-machine stack remains
PARTIAL overall despite this substantive executable path.
