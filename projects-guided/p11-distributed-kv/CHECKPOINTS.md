# Build in observable increments

1. **Reproduce divergence.** Implement blind dictionary assignment on two nodes.
   Make concurrent writes to one key, deliver in opposite orders and preserve
   the disagreeing outputs. Explain why every write arriving is insufficient.
2. **Order events.** Implement local increment and receive-above-both clocks.
   Check the send5/receive-at2 trace. Demonstrate that clock inequality does
   not imply causation for two unrelated local events.
3. **Publish immutable writes.** Define exact record fields and validate types,
   lengths and positive counters before mutation. Reject an invalid second
   record without publishing the first one from that rejected transition.
4. **Join states.** Keep the largest(counter,origin) per key. Derive the three
   maximum identities, then check every delivery permutation of a tiny record
   set against independently chosen winners. Do not apply idempotence to the
   receive clock itself.
5. **Represent deletion.** Add a higher-stamp tombstone. Replay an old live
   snapshot; then remove the tombstone deliberately and reproduce resurrection.
6. **Carry a send stamp.** Advance a sender without writing, capture an Envelope
   and compare full receive ordering with bare-record observation. Explain
   what information was missing from the snapshot.
7. **Build the scenario interface.** Use typed JSON events, bounded input/events,
   unique node/message labels and duplicate-field rejection. Add a real CLI
   success and malformed-input test, retaining per-stage errors.
8. **Investigate and reconstruct.** Predict the supplied14-event trace, execute
   it and explain every clock/value change. Rebuild the clock, join and scenario
   dispatcher from blank files, then change to three nodes and a different tie
   rule. State which guarantees survive and why.

At each milestone submit the mechanism and reasoning, not just a printed pass.
