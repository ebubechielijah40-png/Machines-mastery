# Hints

1–2. Mark each point at which bytes are read; a handle's textual scope alone is
not the full access interval. The failing program requires the old read later.

3–5. Inspect the checked lookup before assignment. For rejected ownership, an
Err alternative can carry a tuple including the original Vec.

6–7. Count allocations separately from variable names. Two names after clone
can represent two buffers. The local and field destruction rules differ.

8. Check the length before calling push. Returning an error after push has
already broken the unchanged-on-error contract.

9–12. A returned owned result and an indefinitely borrowed view require different
lifetime arguments. A second thread cannot make a discarded owner live again.
