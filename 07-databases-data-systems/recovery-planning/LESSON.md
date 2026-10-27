# From one selected generation to a recoverable computation

## State and history have different representations

The previous index gives sorted byte pages. The previous log gives ordered
transaction batches. We want a restart to reconstruct the same committed state
while avoiding replay of the entire historical log. This needs a protocol that
chooses a consistent base and the suffix that follows that base. Independently
valid components can still describe different moments.

Represent a selected generation g by immutable image `index-g.bpi` and mutable
suffix `wal-g.wal`. The canonical `CURRENT` manifest names g, its base version
and the image digest. The state invariant is:

`state = apply_in_order(base_image(g), complete_verified_suffix_batches(g))`.

The index uses the existing unique signed64-bit key/at-most24-byte-value codec.
The store accepts UTF-8 text fitting that value field. It does not truncate a
long value, coerce booleans into keys or silently change a noncanonical decimal
WAL key. Empty transactions are refused; repeated operations in one batch apply
in their listed order. A later put replaces an earlier put for the same key.
This is a key/value store, not an implementation of SQL table semantics.

Deletion reveals why final-state dictionaries are insufficient for suffixes.
Let the base be `{1:A, 2:B}`. The suffix is `delete(1), put(3,C)`. Replaying that
suffix from an empty dictionary produces `{3:C}`. Updating the base with that
dictionary gives `{1:A,2:B,3:C}`, incorrectly resurrecting1. Correctly applying
the actual ordered operations to the base gives `{2:B,3:C}`. A deletion that has
no effect on an empty dictionary can have a decisive effect on a nonempty base.

`_load` first asks the existing WAL decoder to validate every complete frame,
checksum and local transaction sequence. It then walks those verified frame
operations and applies them to the base, including deletions. It does not scan
past corruption or infer that a corrupt complete frame is harmless just because
it appears at the end. An incomplete tail is reported, not silently removed.

A global version is `base_version + complete_suffix_transaction_count`.
If a checkpoint contains120 transactions and its suffix contains3, the version
is123. A new checkpoint retains123 while resetting its new suffix's local frame
number to1 for the next commit. Global version and frame-local sequence are
different quantities. Resetting the global version would make a stale client
version appear current again. A uint64 exhaustion guard refuses further writes.

## Publish a pointer only after its dependencies exist

Updating an image in place can expose mixed old/new pages. Instead, construct a
new complete image and empty suffix under a fresh generation name. Keep the old
selected generation until the new one has been published. All paths live in one
trusted local directory; `CURRENT` replacement stays on that filesystem.

The publication steps and their process-crash interpretations are:

| Last completed step | What CURRENT selects in the observed process-kill model | Reason |
| --- | --- | --- |
| New index written and synced | Old generation | No pointer change |
| New empty suffix written and synced | Old generation | New files remain unselected |
| Generation directory synced | Old generation | Names exist, pointer still old |
| Temporary manifest written and synced | Old generation | Temporary file is not CURRENT |
| Temporary manifest replaces CURRENT | New generation visible | One filename replacement chooses both components |
| CURRENT directory synced | New generation | Publication metadata sync has returned |
| Unselected files collected and directory synced | New generation | Old state is no longer required by cooperating readers |

The underlying Linux API documentation distinguishes file synchronization from
directory-entry synchronization and specifies atomic name replacement; exact
inspected scopes are in [SOURCES](SOURCES.md). The table is our protocol argument
and actual **process-kill** model. Atomic visibility is not a universal physical
power-loss guarantee. A device that lies about flushes, another filesystem's
semantics, a failed sync or a system crash can violate assumptions we did not
experimentally establish. Directory creation/provisioning and its ancestors are
the caller's responsibility; the constructor does not establish a durable root
directory on every filesystem.

Generation names are random identifiers, not authority proofs. Image/manifest
SHA256 checks detect accidental changes when expected bytes are preserved. They
do not authenticate a history against an adversary who can rewrite both files
and digests. A damaged selected image raises an error even if an older valid
generation exists. Silently choosing that older image could discard acknowledged
transactions while making the database look healthy. Recovery to a different
history requires an explicit operator decision and external reconciliation.

## Coordinate readers, writers and garbage collection

Every operation opens and locks the same `LOCK` inode. Snapshots take a shared
lock; commits/checkpoints/repair take an exclusive lock. Shared readers can
coexist, while a cooperating writer waits for them. A checkpoint's exclusive
lock covers reading the current state, publishing its replacement and optional
collection. Thus no cooperating reader still depends on an old path when it is
unlinked. This simple design trades concurrency for an understandable argument.
It is not MVCC or lock-free snapshot acquisition.

Never replace or delete `LOCK` to indicate that a writer finished. Suppose P1
holds a lock on inodeA, then another process unlinks that pathname and creates
inodeB under the same name. P2 can lock inodeB while P1 still owns inodeA: both
believe they hold the lock. A stable pathname must continue to designate the
same coordination object. Closing the open file description releases its lock
under the documented local API; the tests check release after a killed child.

Locks are advisory in this local contract. A process with file permissions can
ignore the protocol and edit files. Hostile directories, symlinks, copied LOCK
files and network-filesystem lock variants are outside the claim. The design
also avoids shared-to-exclusive upgrades: read/modify/write clients release
their snapshot lock and later use an optimistic version condition instead.
Nested calls that try to acquire an incompatible lock through another open
description can block even within one process; this API is not reentrant.

`checkpoint(collect=True)` is compaction: materialize live state as a new index,
start a fresh suffix, publish, then remove unselected generations and temporary
manifests. Deleted keys disappear from the new base because their effects are
already represented. This does not implement in-place B+ deletion/rebalancing.
It also discards historical audit data: a state checkpoint cannot recover which
past deleted value existed unless a separate history is retained. Compaction
requires temporary space for old and new state simultaneously. Failure can leave
orphans. Finite generation/file budgets require investigation and cleanup rather
than unlimited accumulation. A real engine also needs backup retention, disk
quotas, recovery tooling and an explicit historical-retention policy.

## Why serialization alone does not repair a stale client computation

Suppose key0 contains1. Two clients independently read1 and decide to write2.
Exclusive commit locks serialize the writes, but the final value is still2:
the intended pair of increments was lost outside the write transaction.

| Event | Without a precondition | With expected global version1 |
| --- | --- | --- |
| A reads value1 at version1 | Plans put2 | Plans put2 with expected1 |
| B reads value1 at version1 | Plans put2 | Plans put2 with expected1 |
| A commits | Value2, version2 | Value2, version2 |
| B tries its stale plan | Writes2 again | Rejected: actual version2 differs |
| B rereads/recomputes | No automatic correction | Plans3 from value2 and commits at expected2 |

`expected_version` makes a compare-and-set precondition part of the exclusive
transaction. The store checks it after reacquiring current state and before any
mutation. A rejected caller must recompute its semantic operation from fresh
state; blindly retrying the same stale version never creates progress. The
global version is deliberately coarse: an unrelated key update can force a
retry. Finer per-row versions can reduce false conflicts but need more metadata
and careful handling of absence, deletion and predicate reads.

A busy nonblocking lock and a stale version are different failures. Busy means
the operation did not enter this critical section. Stale means it entered,
examined the version and rejected the proposed state transformation. A failure
after appending or syncing a frame is an uncertain acknowledgement: reopening
may find a complete committed batch. The store does not assert that an exception
means absence. Multi-operation retry identities are not added here; applications
must reconcile their own state/operation identity as the
[production workbench](../../production-systems-engineering/labs/operation-workbench/README.md)
teaches.

Incomplete tails require an explicit `repair_tail` decision. It truncates only
the reported incomplete suffix to the last verified boundary and syncs. It does
not erase a bad complete frame. Copy evidence and decide whether incomplete
unacknowledged bytes may be discarded before invoking repair. The byte-cut
experiment constructs such tails; a process kill alone does not simulate every
disk-level interrupted write.

## Choose physical work while preserving query meaning

The [query unit](../query-isolation/README.md) defines bags and NULL semantics.
This planner deliberately accepts a narrower domain: homogeneous integer
equality keys and text payloads, with no NULL, collation or SQL type coercion.
Output multiplicity matters. If L has two rows with key7 and R has three,
their join contributes six pairs, not one or two.

Let `Lk` and `Rk` be key multiplicities. Exact join cardinality is
`J = Σk Lk Rk`: for each left occurrence, every matching right occurrence
produces a pair. A nested loop performs nm key comparisons and J output
emissions, so our declared work count is `nm+J`. A hash join builds one bucket
list per key on the chosen side, probes the other side and emits each matching
pair. Its count is `n+m+2J`: n+m build/probe events, J bucket-member visits and J
emissions. Retaining a list in each bucket preserves duplicates; assigning one
row per key would change the query.

These are transparent teaching units, not CPU cycles or a promise that hashing
always costs constant time. Python dictionary behavior, payload byte sizes,
allocation, cache misses, skew, collisions and storage reads can change elapsed
cost. The row grant limits the number of build rows, not bytes occupied by
arbitrarily large integer/text payloads. Materialized outputs are limited to
100,000 rows; inputs to2,000 rows each. This is not external-memory spilling.

For an estimate, assume roughly uniform key frequencies and compatible domains.
With distinct counts DL and DR, use `floor(nm/max(DL,DR))`. The planner compares
estimated nested/hash work, chooses a smaller build side only if its row count
fits the grant, and executes that explicit plan. Real systems use richer
statistics; the inspected PostgreSQL examples illustrate estimation assumptions,
not a claim that this code reproduces PostgreSQL's optimizer.

Worked ordinary case: n20, m30, DL=DR=10. Estimated J=60. Nested work660;
hash work170. A20-row grant allows a left build. A19-row grant makes this
implementation choose nested loops; it does not secretly allocate a hash table
anyway. If stale statistics claim20 rows but actual build has100, execution
refuses the grant. A more advanced engine could replan or spill; a row estimate
is not permission to ignore the resource budget.

Counterexample: each100-row input has90 copies of key0 plus one each of keys1…10.
Distinct count is11, so uniform estimation gives909 rows. Actual J=90²+10=8110.
The algorithm remains correct, but its predicted work was poor. Count outputs
and measured work separately from estimates. Choosing a good plan does not
prove a cardinality assumption, and a failed estimate is not wrong query meaning.

## Replay a partition without duplicating its committed effects

The stream model has one named immutable ordered source partition. An event is
`(offset,group,delta)`, offsets start at1 and batches contain contiguous offsets.
Two reserved negative keys store source identity and consumed offset. Group keys
are nonnegative, preventing collision with this metadata namespace. Arbitrary
application puts must not be mixed into the same derived-state namespace.

For source-A, process `(1,0,+4),(2,1,+7),(3,0,-1)`. The resulting groups are
0→3 and1→7; retained offset is3. A replay of those three events applies zero
new effects. An overlapping batch starting at2 and ending at4 skips2/3 and
applies only4. A gap from committed3 to proposed5 is refused: the engine cannot
infer event4. It has no out-of-order buffer, watermark or event-time window.

The proof is induction on committed batches. Initially the offset is0 and all
totals are0. Skip offsets already represented; require each new one to be the
next offset; accumulate deltas and the final offset in one ordered transaction.
That transaction commits both effects and progress together, or neither. The
optimistic version ensures another client cannot change the basis between the
snapshot and commit. A killed client after commit can retry the immutable batch
and see zero additional effects. Checkpoint compaction preserves those values,
so replay safety survives restart and history deletion in this model.

The source-immutability premise is essential. If someone changes an old event's
payload while retaining its source identity and offset, our code still skips it.
The experiment actually demonstrates this; it does not claim that a label
authenticates the source. A real pipeline needs protected provenance, retained
source versions, partition identity and suitable change/migration policies.
Reusing a name for different history invalidates the argument.

The transaction also does not cover an external email, remote payment or file
write. Committing the offset before that effect can lose it; doing the effect
first can duplicate it after a crash. Explain the second system's idempotency or
transactional outbox/consumer protocol before promising anything about that
effect. Multi-partition ordering, durable source retention, late data, schema
changes and distributed transactions remain separate unfinished mechanisms.

## Build milestones and observable success criteria

1. Reconstruct base+suffix from verified operations. A checkpointed deletion
   must not reappear. Explain the global/local version distinction by hand.
2. Add create-only generation files and canonical CURRENT publication. Enumerate
   dependency ordering before running the eight named kill boundaries.
3. Add one stable lock inode, shared reads, exclusive writes and explicit repair.
   Demonstrate real incompatible/shared locks and killed-process lock release.
4. Add global optimistic preconditions and a read-modify-write counterexample.
   Recompute after a stale rejection; do not hide conflict with blind retries.
5. Derive the bag cardinality and both work models. Verify multiplicities against
   a Cartesian-product oracle, then falsify the uniform estimate and row grant.
6. Commit partition progress with effects. Test replay, overlap, gap, restart,
   checkpoint, postcommit kill and the mutable-source counterexample.

Deliver original predictions, code, tests, unedited observations, an annotated
state/manifest trace and a limitation analysis. A useful rubric awards25 points
to state/publication invariants,20 to mechanism correctness,20 to independent
failure evidence,15 to assessments/proofs,10 to prerequisite connections and10
to reproducibility/limits. No total compensates for resurrecting a deleted key,
publishing incomplete dependencies, dropping duplicate rows or declaring remote
exactly-once effects from this local count model.

Finally reconstruct manifest publication, one OCC rejection, a duplicate-preserving
hash join and offset/effect commit from memory. Transfer to inventory reservations:
identify which predicates and external confirmations need more than this global
key/value version protocol. Compare your explanation with
[the separated solutions](SOLUTIONS.md) only after writing your own.
