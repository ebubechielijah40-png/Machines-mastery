# Hints after attempting

1–3: Write A's three operations above B's. Choose A's positions, preserving each
row's order. Serializing only stores does not constrain earlier reads.

4–6: Protect the full interval from the read used to compute a result through
its publication. For the defined real experiment, announce readiness **after**
the atomic load and open the gate only after two announcements. Read recorded
worker-local output after joins.

7: A signal is not a stored token for a future waiter. Put the producer's entire
operation between the consumer's release and registration.

8: Draw a wake edge back to lock and predicate check. If the edge skips the
check, ask what authorizes consumption when full is false.

10–11: Head/tail are not enough to distinguish empty from full when both indices
are equal. Add a count or another explicitly derived representation. A wakeup
makes a worker runnable; it does not reserve a slot for that worker.
