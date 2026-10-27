# Experiment Q-MEASURE-01 — phase, partial measurement and correlated bits

**Status: EXECUTED as a classical ideal-statevector mechanism investigation.** No physical quantum experiment, research-benchmark reproduction or learner assessment was performed. The [lesson](../10_STATEVECTOR_MEASUREMENT.md) supplies all equations; [source verification](../SOURCE_VERIFICATION.md) states the model's source scope.

## Questions and predeclared predictions

1. Can changing only the relative phase change a final observed probability? For `H;P(theta);H`, predict `P(1)=sin²(theta/2)`, giving `0,1/2,1` at `0,pi/2,pi`.
2. Does observing a qubit between two H gates alter the final statistics? Predict unmeasured `H;H` gives zero with probability one. Conditioning either possible middle Z-basis outcome, then applying H, gives 50/50. Discarding the outcome means the same weighted 50/50 distribution.
3. Can direct computational-basis correlation distinguish a coherent Bell state from a 50/50 classical preparation mixture of `|00>` and `|11>`? Predict both have equality probability one in ZZ. After H on both qubits (XX setting), predict Bell equality one and mixture equality `1/2`.
4. Do a local gate and partial measurement behave consistently with the joint-state rules? Predict a local unitary on q0 leaves q1's marginal 50/50. Bell partial measurements must yield equal bits and repeated measurement of the same qubit must agree.
5. How does finite shot count affect estimation? At p=1/2, N independent Bernoulli variables have variance N/4 in their sum. Dividing by N gives frequency variance `1/(4N)`, hence standard error `1/(2 sqrt(N))`. Increasing N from 256 to 4096 divides the expected standard error by four. It does not ensure every individual absolute error shrinks.

## Controls, procedure and instrumentation

Use Python's standard library only; execute [measurement_experiment.py](../code/measurement_experiment.py). The gate model, basis ordering, initial states, seed 1801 for fresh-preparation sampling and seed 990 for the partial-measurement stream are controlled. Independently changed factors are phase, insertion of measurement, preparation type, measurement basis and shot count. Outputs are exact statevector probabilities, conditional branch probabilities and pseudorandom shot counts. The code records interpreter version, OS and actual UTC execution time.

Run from the repository root:

```sh
python3 20-quantum-computing/code/test_simulator.py
python3 20-quantum-computing/code/measurement_experiment.py
```

Redirect stdout to your own new result file to retain another run. Do not overwrite the committed raw evidence when comparing environments. The committed files are [actual JSON](results/measurement-2026-10-22.json) and [actual test output](results/tests-2026-10-22.txt). Timing text in test output and execution timestamps need not match a rerun.

## Actual observations and interpretation

On Python 3.12.14/Linux recorded in the JSON, the three phase-sweep probabilities differed from the symbolic prediction by `0`, `1.11e-16` and `4.44e-16`. This is numerical agreement with the expected interference law at three selected inputs, not a universal error bound.

For 256 shots, 126 ones gave frequency `0.4921875` with predicted standard error `0.03125`. For 4096 shots, 2030 ones gave `0.49560546875`, with predicted standard error `0.0078125`. These are two seeded observations. They do not empirically establish a convergence rate. Both shot sets use the same stream prefix, so they are not independent estimates for a hypothesis test.

Unmeasured `H;H` gave zero probability `0.9999999999999996`. Each explicitly conditioned middle-measurement branch gave `0.4999999999999999` per final bit. This distinguishes conditioning a single observed specimen from repeatedly sampling fresh preparations.

Bell versus mixture equality probabilities were approximately `(1,1)` in ZZ and `(1,0.5)` in XX. The q1 marginal before/after local q0 action differed only at floating-point roundoff. In 512 freshly prepared Bell trials, sequential partial measurements gave 243 `00`, zero `01`, zero `10` and 269 `11` outcomes. This supports this implementation's selected correlations and branch update, not a physical nonlocality or no-signalling experiment.

The JSON's complex128 storage numbers are **calculated representation lower bounds**, not allocations or measured resident memory. Never allocate vectors at n=30 or n=40 to reproduce this arithmetic. The actual simulator has a deliberate n<=20 guard; Python-list overhead raises storage beyond packed complex128 estimates.

## Alternative explanations and limitations

A simulator can agree with its own assumptions even when they do not describe a device. The dense gate oracle and analytical identities provide independent implementation checks, but all computations still share Python floating-point arithmetic. No Qiskit, second simulator or quantum hardware was used as a numerical oracle. Seeded pseudorandomness gives reproducibility, not quantum randomness; one seed cannot establish statistical quality. All represented states are pure conditional states; a mixture is handled by a classical weighted ensemble, not a general density-matrix engine. No channels, calibration drift, physical noise, tomography or Bell inequality violation is modeled.

## Follow-up experiments

Exercise 12 calls for at least 30 independent streams to estimate the sampling-error scaling; it is **NOT YET OBSERVED**. A later extension should add a density-matrix depolarizing channel and distinguish sampling uncertainty from model error. Another extension should cross-check small circuits against a separately installed simulator with the same declared bit convention. Record its exact version before making compatibility claims.
