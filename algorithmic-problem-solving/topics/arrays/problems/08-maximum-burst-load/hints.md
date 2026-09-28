# Hints — Maximum Contiguous Burst Load

1. First identify what information from the already-processed prefix is actually necessary for the next decision.
2. Kadane's recurrence: the best interval ending at i either starts at i or extends the best ending at i-1.
3. State an invariant before writing code. If you cannot state what is already guaranteed after each iteration, the implementation is not yet justified.
4. Only after a second attempt, compare your design with the optimal approach described in `solution.md`.
