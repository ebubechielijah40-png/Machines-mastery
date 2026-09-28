# Quantum prerequisites — taught just in time

## Complex numbers
A complex number is `a + bi`, where `i²=-1`. Quantum amplitudes are complex because phase relationships matter. Magnitude squared `|a+bi|²=a²+b²` contributes to measurement probability.

**Example:** amplitudes `(1/√2, 1/√2)` give probabilities `(1/2,1/2)`. Amplitudes `(1/√2, -1/√2)` have the same individual probabilities but different relative phase; later gates can convert that phase difference into different observable outcomes.

## Vectors
A one-qubit pure state is represented by a normalized two-component complex vector:

`|ψ⟩ = α|0⟩ + β|1⟩`, with `|α|²+|β|²=1`.

The vector is not a classical hidden choice between 0 and 1. The amplitudes evolve coherently until measurement according to the model.

## Matrices
Quantum gates on closed ideal systems are unitary matrices: `U†U=I`. Unitarity preserves total probability and makes ideal evolution reversible.

Pauli X:
`[[0,1],[1,0]]` swaps amplitudes of |0> and |1>.

Hadamard:
`1/√2 [[1,1],[1,-1]]` creates/interferes superpositions.

## Tensor products
Two qubits use a four-dimensional state space with basis `|00>, |01>, |10>, |11>`. State-space dimension grows as `2^n`, which is why exact classical statevector simulation becomes expensive quickly. This exponential representation does **not** mean a quantum computer can simply read all `2^n` amplitudes; measurement returns limited classical outcomes.

## Probability
Measurement probabilities come from squared magnitudes of amplitudes. Repeated shots estimate a distribution. Finite shots add sampling noise even in an ideal circuit.

## Assignment
1. Multiply X and H by basis-state vectors by hand.
2. Verify H applied twice equals identity.
3. Normalize five complex vectors.
4. Compute a two-qubit tensor product.
5. Predict measurement probabilities before running the simulator.
