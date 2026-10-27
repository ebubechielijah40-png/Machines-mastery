# Build an ideal quantum statevector simulator

The problem is to predict outcome distributions while retaining coherent phases that probabilities alone discard. Build a small local Python implementation, derive each transformation, then investigate which observations distinguish coherent preparations from classical mixtures. This project now has a runnable [reference](../../20-quantum-computing/code/simulator.py), [tests](../../20-quantum-computing/code/test_simulator.py), and an [executed mechanism experiment](../../20-quantum-computing/experiments/MEASUREMENT.md). None establishes learner mastery or physical hardware behavior.

Use Python 3.10+; no external packages, accounts or physical apparatus are required. Work only on local synthetic states. Begin with [prerequisites](PREREQUISITES.md), study the [derivation lesson](../../20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md), and make an attempt at each [checkpoint](CHECKPOINTS.md) before opening [hints](HINTS.md) or [solutions](../../20-quantum-computing/assessments/SOLUTIONS.md).

## Architecture and design decisions

`State(n)` owns `2**n` complex amplitudes; array index x represents the binary string `q[n-1]...q0`. A local gate updates amplitude pairs sharing all other bits. CNOT permutes basis indices. Observation is either nonmutating sampling of fresh preparations or a projective measurement that changes one specimen. A caller-owned RNG makes experiment streams reproducible without resetting a seed before every observation.

These choices avoid constructing a `2**n by 2**n` matrix for ordinary gates, keep bit ordering testable, and make the difference between preparing many copies and measuring one explicit. A slow dense matrix-action oracle is retained in tests for small n. Validation rejects nonunitary gates; silently renormalizing arbitrary transformations would hide a mechanism error.

## Deliverables and verification

Save your implementation, a written basis/index contract, hand traces for `H;Z;H` and Bell preparation, independent gate tests, one failed-test debugging log, experimental predictions and raw outputs, and a limitations note. Use [TESTS.md](TESTS.md) for acceptance criteria and [EXPERIMENTS.md](EXPERIMENTS.md) for the controlled investigation.

Reference commands from repository root:

```sh
python3 20-quantum-computing/code/test_simulator.py
python3 20-quantum-computing/code/measurement_experiment.py
```

To test your own implementation without copying the reference, place a copy of the test file beside your own `simulator.py` in a separate attempt directory, then execute the test there. Preserve the reference unchanged. The dense oracle checks output amplitudes, not only normalization; a wrong unitary can preserve norm perfectly.

## Evaluation rubric

Score each dimension 0 (absent), 1 (partly correct), or 2 (correct and independently explained): representation contract; complex arithmetic; local-gate derivation; CNOT truth table; phase/interference example; partial measurement; malformed-input tests; independent oracle; experiment evidence/interpretation; reconstruction and transfer. No total score alone confers mastery. Any wrong bit convention, invalid probability normalization, impossible branch acceptance, fabricated observation or unexplained copied implementation requires remediation before a successful build claim.

After a delay, close the source and rebuild initialization, a local gate, CNOT and partial measurement from your saved contract. Run the tests only after completing the attempt, explain each failure, then extend to measuring an arbitrary qubit in a three-qubit state. [Production limits](PRODUCTION.md) make clear why this is a local teaching tool, not an online execution service.
