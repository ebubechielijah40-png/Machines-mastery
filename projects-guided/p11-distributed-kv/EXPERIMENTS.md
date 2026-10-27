# Predict a partition and stale replay

Question: which states can disagree during a communication gap, and when does
the chosen join rule reconcile them? Hypothesis: concurrent local writes differ
until the captured full states are delivered; both then select the same maximum.
A retained newer deletion should withstand an older live replay.

Hold node IDs, stamp order, record values and validation rules fixed. Delay only
delivery. The [input](example.json) writes red at A and blue at B, reads both,
captures both messages, crosses deliveries, deletes at A, sends that deletion,
then replays the old B message. Record local counters and final immutable records
as well as visible maps. Use the commands in [README](README.md).

The [actually executed output](evidence/observed.json) retains the full trace.
It observed different early reads and equal empty visible maps at the end,
with a deletion record still stored. Compare with the core's independent
[24-order experiment](../../15-distributed-systems/ordering-reconciliation/EXPERIMENTS.md).
These are specified local schedules, not observed network faults or crash tests.

Alternative explanations for disagreement include missing delivery, different
rules, reused stamps or a defect. Follow up by restarting an identity, dropping
a tombstone, forging a counter or omitting the Envelope clock. Preserve each
counterexample. Before adding a socket or WAL, write the new delivery/commit
and recovery semantics; their guarantees do not compose by file import alone.
