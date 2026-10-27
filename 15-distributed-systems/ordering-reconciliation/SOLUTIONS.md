# Reference arguments

1. A: red then received blue ends blue; B: blue then received red ends red.
   Both applied both writes. Assignment composition does not commute.
2. B receives at6 and its write is7. Separate processes can have local counters
   2 and7 with no communication, so the converse of the clock condition fails.
3. Duplicate, reorder or regroup a finite set without changing its largest
   element. The proof applies separately to each key, provided a stamp names
   one immutable event. Receive increments a counter, so two identical deliveries
   give the same joined map but different successive clock values.
4. At counter1 for A,B,C, the lexicographic origin rule selects C regardless
   of delivery order. Compare that expected stamp with the implementation's
   output after all six permutations and after duplicates. This tests the
   tie rule, not the desirability or authenticity of C's value.
5. A tombstone at(2,A) dominates a live value at(1,A). Removing the tombstone
   leaves missing, which loses to any actual live record. Safe collection needs
   a proven bound on outstanding old states and eligible replicas/incarnations,
   or another protocol that rejects stale history. This model supplies neither.
6. Bare merge orders after the observed record1 and can remain below22.
   Envelope receipt orders after the actual send event22. A snapshot of only
   winning records cannot reconstruct all sender events.
7. Validation constructs a candidate map and next clock without mutating the
   original. An invalid record prevents publication. A process crash still
   destroys memory; no bytes were synchronously committed to durable storage.
8. Restart can reuse an event identity, violating globally unique stamps.
   Authentication prevents some impersonation but does not by itself prove
   that a legitimate node respected monotonicity. Persisted counters or distinct
   incarnation IDs require a recovery/membership design. Very large valid-looking
   stamps can also exhaust this toy clock; input validation is not Byzantine defense.
9. All replicas joining the same valid record set choose the same keywise
   maximum by the three identities. Eventual delivery is the liveness premise;
   permanent partitions do not satisfy it. Concurrent balance overwrites can
   lose a debit even after convergence, so financial transactions need additional
   operations, invariants, coordination and durable semantics.
