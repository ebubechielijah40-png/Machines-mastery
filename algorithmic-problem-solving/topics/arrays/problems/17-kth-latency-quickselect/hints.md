# Hints — Select the k-th Latency Without Full Sorting

1. First identify what information from the already-processed prefix is actually necessary for the next decision.
2. Quickselect partitions around a pivot and continues only into the side containing rank k.
3. State an invariant before writing code. If you cannot state what is already guaranteed after each iteration, the implementation is not yet justified.
4. Only after a second attempt, compare your design with the optimal approach described in `solution.md`.
