# Quantum computing — deep handbook

## 1. What makes a quantum computer different?

A classical bit is modeled as one of two logical states at a time. A qubit is represented by a normalized complex vector in a two-dimensional Hilbert space. The important resources are not “being 0 and 1 at once” as a slogan, but **coherent amplitudes, relative phase, entanglement, controlled unitary evolution, and measurement**.

Quantum algorithms arrange interference so amplitudes associated with useful outcomes are amplified and others cancel. The hard part is designing a transformation whose measurable distribution reveals useful information with fewer resources than known classical methods for a specified problem model.

## 2. Measurement

Measurement in the computational basis returns 0 with probability `|α|²` and 1 with probability `|β|²`, then updates the state in the ideal projective model. You cannot copy an arbitrary unknown quantum state perfectly (no-cloning theorem), and you cannot inspect amplitudes directly from a single system. Reconstructing an unknown state requires repeated measurements in multiple bases and scales poorly with system size.

## 3. Phase and interference

Two states can have identical computational-basis probabilities yet behave differently later because their relative phases differ. This is why a purely probabilistic classical analogy is incomplete.

Example: `H|0> = (|0>+|1>)/√2`; applying H again yields |0>. If a Z gate flips the phase of |1> before the second H, the result becomes |1>. Phase became observable through interference.

## 4. Entanglement

A two-qubit state is entangled when it cannot be written as a tensor product of two independent one-qubit states. The Bell state `( |00> + |11> )/√2` has perfectly correlated computational-basis measurements. Entanglement is stronger than ordinary correlation in ways formalized by Bell inequalities, but it does not enable faster-than-light communication because local measurement outcomes are individually random and usable correlations require classical comparison.

## 5. Gates and circuits

Quantum circuits are sequences of gates. Single-qubit gates rotate state; controlled gates condition an operation on another qubit. CNOT plus arbitrary single-qubit gates form a universal model in the ideal circuit setting. Physical hardware does not execute abstract gates perfectly: control pulses, calibration, connectivity, coherence, crosstalk, leakage, and readout errors matter.

## 6. Algorithms

### Deutsch–Jozsa
A pedagogical example showing how phase kickback/interference can distinguish classes of oracle functions with fewer oracle queries than a deterministic classical algorithm under the promised problem.

### Grover search
For an unstructured search space of size N with an oracle marking solutions, Grover's algorithm uses about `O(√N)` oracle applications, a quadratic rather than exponential speedup. State preparation/oracle cost and hardware overhead matter in real applications.

### Shor
Shor's algorithm reduces integer factoring to order finding, which quantum Fourier-transform techniques can solve efficiently in the ideal fault-tolerant model. This threatens RSA and discrete-log-based public-key cryptography if sufficiently large, fault-tolerant quantum computers become available. The algorithm does not “break all encryption.”

### Quantum simulation
Simulating quantum systems is one of the original motivations for quantum computation. Potential advantages depend on Hamiltonian structure, observable estimation, state preparation, error, and resource costs.

## 7. Noise and error correction

Real qubits interact with environments and controls imperfectly. Decoherence, relaxation, dephasing, leakage, gate errors, and measurement errors reduce fidelity. Quantum error correction encodes logical information redundantly across entangled physical qubits without cloning arbitrary states. Syndrome measurements reveal error information without directly measuring the logical state.

Fault tolerance requires error rates below architecture-dependent thresholds and substantial overhead. A device with many physical qubits is not equivalent to the same number of high-quality logical qubits.

## 8. Hardware modalities

Major approaches include superconducting circuits, trapped ions, neutral atoms, photonic systems, semiconductor spins, and others. They differ in gate speed, connectivity, coherence, fabrication, control, measurement, and scaling constraints. The abstract circuit model hides microwave/laser control, cryogenics/vacuum, electronics, calibration, compilers, routing, and error mitigation/correction.

## 9. Quantum software stack

```text
algorithm
→ circuit / intermediate representation
→ optimization / transpilation
→ hardware-aware mapping and scheduling
→ control instructions / pulses
→ physical device
→ measurement electronics
→ classical decoding / post-processing
```

Understanding a quantum machine therefore still requires classical computers, control systems, signal processing, statistics, and systems engineering.

## 10. What quantum computers cannot do

They do not evaluate every branch and reveal all answers, violate information theory, communicate faster than light, make NP-complete problems known to become easy in general, or automatically accelerate arbitrary code. Speedup is algorithm/problem-model specific and may disappear after state preparation, error correction, communication, or measurement costs.

## 11. Quantum and cryptography

Quantum threat is asymmetric. Factoring/discrete log algorithms threaten RSA/ECC-like public-key systems. Symmetric cryptography and hashes receive at most quadratic generic-search advantages in the standard model, so security levels can be adjusted with larger parameters. Post-quantum cryptography runs on classical computers and is distinct from quantum cryptography such as QKD.

## 12. How to evaluate a quantum-advantage claim

Ask: What exact computational problem? What input model? What classical baseline? Is the comparison asymptotic or measured? Does it include state preparation, error correction, I/O, sampling, compilation, and verification? Is the hardware solving a useful task or a benchmark designed around its strengths? What confidence interval and reproducibility evidence exists?
