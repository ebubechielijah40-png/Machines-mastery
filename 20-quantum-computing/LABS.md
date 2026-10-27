# Quantum labs

## Lab 1 — phase is not probability
Prepare |0>, apply H, then H again. Predict |0>. Insert Z between the H gates and predict |1>. Run the local simulator and explain how the probability distribution after the first H was identical in both cases while final outcomes differed.

## Lab 2 — Bell state
Create |00>, apply H to qubit 0, then CNOT(0→1). Inspect probabilities: only 00 and 11 should have nonzero ideal probability. Explain why repeated measurements correlate but no chosen message is transmitted.

## Lab 3 — state-space scaling
Calculate the packed complex128 representation lower bound `16*2**n` bytes for n=10,20,30,40 without allocating these vectors. If measuring actual process memory, choose small n under an explicit memory budget and distinguish Python-list overhead from packed storage. Never allocate a 30- or 40-qubit state on a normal laptop to reproduce this arithmetic. The local simulator deliberately caps n at 20. Explain why exact dense simulation grows exponentially.

## Lab 4 — sampling error
For a qubit with p(1)=0.3, simulate 100, 1,000, 100,000 measurements and compare empirical frequency to p. Explain `O(1/√shots)` sampling-error scale.

## Lab 5 — Grover toy model
Implement amplitude-amplification for a tiny state space or trace it symbolically. Count oracle calls and compare with linear classical search. Separate query complexity from total hardware cost.

## Lab 6 — noise thought experiment
Apply an artificial bit-flip probability after each gate in a classical Monte Carlo wrapper. Plot success probability vs circuit depth. This is not a full quantum noise model; explain what it omits.
