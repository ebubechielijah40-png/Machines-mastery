# Partition, reconcile, delete and replay

Question: does the declared keywise maximum converge under different delivery
orders, and which larger guarantees remain absent? Hypothesis: valid unique
stamps and eventual delivery make the map independent of order/duplicates;
retaining a newer tombstone prevents stale resurrection.

Hold the immutable record set, tie rule, initial empty replicas and validation
rules fixed. Vary delivery order and repetitions. The script first makes
conflicting writes during a modeled partition, exchanges full states using
timestamped Envelopes, writes after receipt, deletes a key and replays a stale
message. It then enumerates all24 permutations of four records plus duplicate
deliveries. Instrument complete state, visible state, local counters and winner
equality, not only a printed final value.

Run the test and experiment commands in [the lesson](README.md). The
[retained actual execution](evidence/results.json) observed two different values
during the partition, equal B-first winners after exchange, A-after-receive
after the causally later write, and empty visible maps after deletion/stale
replay. All24 enumerated orderings matched the independently chosen final state.
This is a specified in-memory schedule experiment, not observed network loss,
crash recovery, a clock-synchronization benchmark or a consensus reproduction.

The negative controls are blind dictionary assignment and tombstone deletion;
tests retain explicit divergent/resurrected outputs. Alternative explanations
for nonconvergence include incomplete delivery, conflicting reused stamps,
different tie rules or a defective implementation. Correct convergence under
these schedules does not select the right concurrent user intent.

Follow up with a persist/restart protocol, authenticated membership and bounded
state synchronization. State the new assumptions before claiming a stronger
guarantee. Inject stale snapshots and uncertain acknowledgements, and measure
whether application invariants survive as well as whether dictionaries agree.
