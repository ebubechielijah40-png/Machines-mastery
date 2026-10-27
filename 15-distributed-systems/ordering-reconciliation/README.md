# Ordered events and a convergent replicated map

Two replicas can accept writes during a communication gap and later disagree.
Delivering every message once is insufficient when both writes target the same
key and arrival order differs. This unit derives an explicit resolution rule,
implements it, and tests the assumptions needed for convergence. It follows
[sets/relations/proofs](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
[Python values and state](../../02-programming/python-entry/README.md),
and [stream boundaries](../../06-networking/stream-boundaries/LESSON.md).

The implementation is an in-memory deterministic replica model. It supplies no
consensus, authenticated membership, durable recovery or network service. Those
are missing mechanisms, not consequences of an associative merge function.

## 1. First reproduce the failure

Replicas A and B both begin with no key x. A writes x="red" while B writes
x="blue" without communicating. If each applies received writes directly to
a dictionary, A receiving B ends blue and B receiving A ends red. Both saw the
same two writes and still disagree. Replaying an older message can change the
answer again. An arrival-order assignment is not a commutative operation.

This counterexample is also retained in the older
[replication simulator tests](../code/test_replication_sim.py). It motivates a
specific state rule rather than pretending that a leader-election counter
already establishes a consistent replicated history.

## 2. Separate causal evidence from a sorting rule

Events in one process have local order. Sending a message precedes its receipt;
the transitive closure gives a strict happened-before relation. Concurrent
events have no path in either direction. Lamport1978's logical-clock condition
requires a→b to imply C(a)<C(b), with no converse. An increasing local counter
and a receive update above both current and received values preserve that
one-way condition [L78]. The
[paper reconstruction](../../research-paper-reconstruction/domains/distributed-systems/01_lamport_clocks_1978.md)
examines the original paper's larger scope separately.

Our implementation uses local `C←C+1` and receive `C←max(C,message_C)+1`.
For a send at5 received by a process at2, the receive event becomes6; its next
write becomes7. It cannot legitimately claim to precede the message it observed.
An unrelated process may also have a local event at7: integer inequality alone
does not establish that a message or causal influence occurred.

Records contain key, string value or deletion marker, positive counter and
origin ID. Order stamps lexicographically by(counter,origin). Thus(1,"B")
is larger than(1,"A") by an arbitrary but deterministic tie rule. Origin
spelling is not a measure of authority, importance or physical recency.
Unique origins and no counter reuse are model premises.

State transfer and a send event have different information. An unchanged map
may contain its latest write at counter1 even though the sender's clock has
advanced to22. `Envelope` carries the send counter as well as records so the
receiver orders its receipt after22. Merely taking the maximum record counter
would forget intervening sender events. `merge` intentionally offers only
record-observation ordering; use `send`/`receive` for a message-event model.

## 3. Derive the state join from a single-key maximum

For each key retain the record with the greatest stamp. Missing is less than
any actual record. On a valid history, a stamp names one immutable event,
so equal stamps cannot name different payloads or keys. The code rejects a
conflict visible in a merge before publishing any state.

For one key, max has three crucial identities:

`max(a,a)=a`

`max(a,b)=max(b,a)`

`max(max(a,b),c)=max(a,max(b,c))`.

They are idempotence, commutativity and associativity. Each follows because
the result is the largest element of the same finite set, regardless of
duplication, ordering or grouping. Applying the rule independently per key
preserves these identities for maps, with records sorted by key only for
deterministic presentation.

Consequently, replicas receiving the same valid record set eventually have
the same state even if delivery order and duplicate counts differ. This
conclusion assumes eventual delivery of the relevant records, or full states
that dominate them. During a permanent partition the record sets can remain
different indefinitely. The merge law is not an availability or time bound.

The map state joins idempotently, but the receive **clock** advances on each
receive event. Repeating a message therefore need not leave the complete
Replica object unchanged. Conflating state convergence with clock equality
would give a false test specification.

Worked conflict: A publishes(1,A,"red"), B publishes(1,B,"blue"). Both retain
blue after full exchange. A then observes B and writes a higher counter, so
its later write wins. The resolution discarded one concurrent value; it did
not ask a person which intention was correct or preserve a multi-value conflict
for application review. A merge can be mathematically convergent and still
use an unsuitable product policy for bank balances or collaborative edits.

## 4. Deletion needs retained evidence

Dropping a key from a dictionary is indistinguishable from never having seen
it. Suppose B holds an old value while A deletes it. If A merely erases its
record, a later stale state from B brings the value back. Our deletion is a
record with value=None and a higher stamp: a tombstone. It participates in the
same maximum rule but is absent from `visible()`.

After the tombstone reaches both replicas, replaying the old value cannot
replace its larger stamp. Naively deleting tombstones breaks that argument;
the test suite constructs the resurrection directly. Safe collection requires
knowledge about all possible old senders, retention, acknowledgements or epochs.
No such membership/recovery protocol exists here, so tombstones are retained.
An empty string is a legitimate value; None has the distinct deletion meaning.

## 5. Validate an entire transition before mutation

Frozen records and tuple snapshots prevent ordinary external mutation of a
published snapshot. Input validation checks key/value/origin lengths, exact
integer counters and an upper clock bound. Before receipt, build and validate
the candidate joined state and next clock. Only then change clock and map.
A malformed later record must not leave an earlier valid record half-applied.

This is local failure atomicity under the program's exceptions, not disk
atomicity or a transaction across independent machines. In particular, process
failure destroys all state. Restarting the same node ID at zero can reuse
stamps and violate the valid-history premise. A production design would need
durable monotone metadata or a new incarnation identity and a validated recovery
protocol. The [transaction-log project](../../projects-guided/p07-storage-engine/README.md)
teaches one durable mechanism, but attaching it requires a combined ordering,
commit and recovery argument.

Validation is also not authentication. A caller can forge a large counter or
another origin ID in a syntactically valid Record. It can dominate future
writes or exhaust the bounded clock. The implementation does not authenticate
origins, rate-limit keys or cap total state size. Discarded history is not
fully retained, so a conflicting old stamp may no longer be detectable from
the winners alone. The merge algebra is conditional on globally valid histories;
its local conflict checks do not establish that premise against an adversary.

## 6. Test and investigate the real contract

Python3.10+, standard library only. From repository root:

```bash
python3 -m unittest discover -s 15-distributed-systems/ordering-reconciliation -v
python3 15-distributed-systems/ordering-reconciliation/experiment.py
```

Tests independently enumerate all24 permutations of four original records,
add duplicate deliveries, compare the expected winners, check join laws,
retain tombstones, expose naive collection and verify rejected inputs leave
state and clock unchanged. Envelope tests distinguish send time from the
largest stored write time. Overflow is explicit rather than wrapping.

[Experiments](EXPERIMENTS.md) states the question, controls, actual observations
and limitations. Attempt [exercises](EXERCISES.md), use [hints](HINTS.md) only
after an attempt, then compare [solutions](SOLUTIONS.md). Reconstruct a
three-replica schedule and the convergence proof from a blank file before the
[guided workbench](../../projects-guided/p11-distributed-kv/README.md).

No result here establishes linearizability, causal delivery, a majority commit,
exactly-once execution, physical last-write time or safe network deployment.
Those are distinct specifications requiring different mechanisms and evidence.
