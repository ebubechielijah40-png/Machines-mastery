# Progressive implementation hints

First write the relevant [checkpoint](CHECKPOINTS.md) attempt. Open only the hint you need.

**Representation:** For index i, `(i >> q) & 1` reads the addressed bit. Pairs on q share all bits except `1<<q`; visit each pair once.

**Gate update:** Save `(a,b)` before either write. Test the complex inner products between both columns of U; checking each column's norm alone misses nonorthogonality.

**CNOT:** Swap only the member whose control is one and target is zero; its partner has the target set. Visiting both ends swaps twice and incorrectly undoes the gate.

**Measurement:** Sum squared magnitudes of compatible indices. Divide surviving amplitudes by sqrt(branch probability), not probability. Reject exactly zero probability before mutation. Measuring q must not reveal the unmeasured register bits.

**Sampling:** A local RNG object avoids changing global random state. Reusing one seed for every individual shot is not a stream of independent preparations.

**Debugging:** Norm one does not mean the right computation. Compare full complex output vectors to a dense small-case oracle and test qubit addresses separately. Additional [conceptual hints](../../20-quantum-computing/assessments/HINTS.md) and [worked solutions](../../20-quantum-computing/assessments/SOLUTIONS.md) are deliberately separate.
