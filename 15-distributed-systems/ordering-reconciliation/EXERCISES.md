# Derive, implement and break the merge

1. Trace the two blind dictionary assignments in opposite orders and explain
   why delivery completeness alone is insufficient.
2. A sends at clock5, B receives while at2 and then writes. Derive B's two
   new counters. Give two unrelated events whose counters differ without
   a happened-before path.
3. Derive the three maximum identities. Explain why map join preserves them
   keywise and why the receive clock is not idempotent.
4. Construct three concurrent writes from A,B,C to one key. Enumerate all
   delivery permutations and duplicate messages; check the final winner with
   an independently sorted list of stamps.
5. Trace a deletion and stale replay, then delete the tombstone and reproduce
   resurrection. What additional knowledge would justify safe collection?
6. A sender's latest record counter is1 but its send event is22. Compare
   bare-record merge and an Envelope receive. Which preserves message-event order?
7. Inject one valid record followed by an invalid record and verify that
   rejection changes neither state nor clock. Explain why this is not disk durability.
8. Restart an origin at zero or forge a large stamp. Identify which premise
   fails and whether syntax validation, signatures or persistence addresses it.
9. Reconstruct clock, immutable records and join without the reference. Provide
   a proof of convergence conditional on delivery and valid stamps; name an
   application whose desired semantics are not satisfied by this winner rule.
