# Test requirements and actual evidence

The [runnable reference tests](../../20-quantum-computing/code/test_simulator.py) use unittest and run directly from any working directory via the file path. The file itself locates `simulator.py` through Python's script directory. It requires only the standard library.

Acceptance checks include: H twice and H/Z/H; separate X qubit-order checks; complex gates against a dense independent oracle for n=1..4; all 3-qubit basis-state CNOT truth tables; Bell preparation/inversion; common-phase invariance; conditional-branch normalization; preservation of unmeasured coherence; sequential Bell measurement agreement; fresh-preparation sampling that does not mutate state; rejection of zero-mass conditioning; tiny positive branch support; malformed n/vector/gate/address/shot arguments; and detection of externally corrupted amplitude arrays.

The [actual captured test output](../../20-quantum-computing/experiments/results/tests-2026-10-22.txt) records 18 passing test methods. Several methods exercise many subcases; 18 is not a count of all inputs or a coverage percentage. This evidence does not establish correctness for arbitrary long circuits, every floating-point value, density matrices, physical noise or a production service. The [experiment output](../../20-quantum-computing/experiments/results/measurement-2026-10-22.json) is additional mechanism evidence, not a substitute for these tests.

For your independent implementation, preserve failed logs as well as passing ones. A copied answer passing a test is reference validation, not a reconstruction assessment.
