# Quantum project ladder

## Q-1 Statevector simulator
Implement complex amplitudes, normalization checks, X/Z/H, CNOT, probability calculation, and sampling. Tests should verify norm preservation and known circuits. Then add arbitrary single-qubit matrices with a unitarity check.

## Q-2 Circuit language
Design a tiny textual circuit format, parser, simulator backend, and deterministic test fixtures. Add malformed-input tests and resource estimates (`2^n` amplitudes).

## Q-3 Quantum algorithm notebook
Implement/trace Deutsch–Jozsa, Bernstein–Vazirani, tiny Grover, and phase estimation on small states. For each, compare query count, total simulated work, and what the algorithm actually establishes.

## Q-4 Noise and decoding study
Create simplified channels (bit flip, phase flip, depolarizing approximation), simulate repetition-code intuition, and explain why classical repetition is not itself a general quantum error-correcting code.

## Q-5 Quantum systems architecture
Produce a hardware/software stack design for one modality using public documentation: algorithm → compiler → scheduler → controller → device → readout → decoder. Identify calibration loops, timing, error sources, and what information crosses each interface.
