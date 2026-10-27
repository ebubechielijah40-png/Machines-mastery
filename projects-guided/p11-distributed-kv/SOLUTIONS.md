# Reference reasoning and assessment

The core [worked solutions](../../15-distributed-systems/ordering-reconciliation/SOLUTIONS.md)
cover clock arithmetic, join identities, delivery permutations, tombstones and
failure atomicity. The reference [dispatcher](code/workbench.py) maps one typed
input event to one core transition and records observable results. A send stores
an immutable Envelope; later delivery does not recreate the sender's current state.
That detail makes delayed/stale messages a real modeled distinction.

For the example, equal first-write counters select B by the arbitrary origin
order. Each cross receipt advances above both local and sender clocks. A's
subsequent deletion has a larger stamp than either concurrent value. B receiving
it also hides the key; replaying B's older captured message cannot undo it.
The terminal visible dictionaries agree but retain tombstone evidence.

Rubric: derivation/invariants30%, runnable state/interface20%, independent
failure/ordering tests20%, experiment interpretation20%, unaided transfer10%.
A solution fails the conceptual requirement if it calls convergence consensus,
claims disk recovery from an in-memory snapshot, or silently deletes the
information needed to reject stale writes. Reconstruct a three-node example
with changed key/value names rather than memorizing this trace.
