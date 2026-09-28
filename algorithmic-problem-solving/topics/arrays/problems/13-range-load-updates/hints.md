# Hints — Apply Bulk Range Load Updates

1. First identify what information from the already-processed prefix is actually necessary for the next decision.
2. Record only boundary changes in a difference array: +delta at start, -delta after end, then prefix-sum once.
3. State an invariant before writing code. If you cannot state what is already guaranteed after each iteration, the implementation is not yet justified.
4. Only after a second attempt, compare your design with the optimal approach described in `solution.md`.
