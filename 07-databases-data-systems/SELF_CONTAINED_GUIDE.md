# Databases and data systems: persistence before abstraction

**Original full-mandate classification: PARTIAL.** The fixed foundational STRONG
gate is reviewed separately in [the33-domain dashboard](../STRONG_PROGRESS_DASHBOARD.md).
The original entry lesson remains below, followed by the now-developed query,
index, checkpoint/planning and stream progression. No reference output certifies
learner mastery or a deployed database.

## Begin with a failure you can explain

A Python dictionary is an in-process association of keys and values. Restarting its program constructs a different dictionary. Serializing it gives bytes, but a second question appears: which state should be recovered when a transfer updates two keys and the write stops halfway through?

Study [the recoverable-log project](../projects-guided/p07-storage-engine/README.md). It teaches a byte format, ordered transaction batches, checksums, bounded parsing, sync acknowledgement, unknown outcome, incomplete-tail policy, original code and byte-cut experiments. Start with its memory baseline; then derive the storage representation before viewing the reference.

The distinction is foundational: **durable representation**, **transaction visibility**, **query semantics**, **access methods** and **concurrency rules** solve different problems. A successful checksum does not make a business invariant true; a transaction can atomically store an incorrect result. A sync request does not implement authorization. A fast in-memory lookup says nothing about restart cost.

## Connect the log to relational data

Suppose a logical relation `Sample(id, instrument, reading)` contains `(1,"A",2.1)`, `(2,"A",2.4)` and `(3,"B",9.0)`. Selecting rows whose instrument is A yields the first two rows; projecting their readings yields 2.1 and 2.4. The mean is `(2.1+2.4)/2=2.25`. An SQL expression can state that request:

```sql
SELECT AVG(reading) FROM Sample WHERE instrument = 'A';
```

This is a logical request. A storage engine decides how its rows and indexes are encoded and recovered. A query executor decides whether to scan rows or use an index; an optimizer estimates costs. These concerns interact but should not be confused. An index trades additional stored state and update work for an alternate access path; it does not change which rows satisfy the predicate.

The [query/isolation unit](query-isolation/README.md) now teaches original bag
selection/projection/joins, grouping, NULL and actual SQLite transaction schedules.
Complete those worked traces before adding physical access paths. The existing
[SQLite index lab](../production-systems-engineering/labs/sqlite-index/README.md)
supplies a runnable plan comparison: preserve query results as an independent
oracle and inspect `EXPLAIN QUERY PLAN` before a performance claim.

## What changes at the next boundary

The log project requires one exclusive owner. Two writers that both recover last transaction 8 can both choose ID 9; appending individually valid records does not prevent that race. Isolation and concurrency control need an enforceable rule for overlapping operations. They are not supplied by a checksum or by calling a method `commit`.

At larger history sizes, sequential replay grows even when only100 live keys
remain. The log project measures this directly. The next
[byte-page index](page-index/README.md) now teaches fixed-size encoding, search,
splits/ranges and bottom-up loading through actual bytes, without pretending that
a page checksum proves transaction atomicity. Its read-only bridge still replays
the whole authoritative log; preserve that simpler mechanism for comparison.

The [checkpoint/planning build](recovery-planning/README.md) then adds a selected
immutable B+ generation plus suffix WAL, manifest publication, stable-inode locks,
global optimistic preconditions and compaction. Compare a deleted base key with
an empty-state suffix replay: the latter loses a tombstone and resurrects data.
Use actual process-kill and byte-cut evidence to separate visibility, logical
atomicity and the stronger physical persistence claims that were not tested.

The same build derives duplicate-preserving nested/hash joins and a transparent
cardinality/cost estimator. Its hot-key experiment demonstrates poor estimates
without changing correct result multiplicities. A row grant is enforced against
actual build rows; it is not a promise of bounded bytes for arbitrary payloads.

A batch pipeline processes finite input; a stream introduces ongoing progress,
identity and replay. The developed one-partition count investigation commits
offset and effects together, survives checkpoint/restart and rejects gaps. It
also executes a counterexample where altered historical payloads are skipped:
the immutable-source premise needs independently protected provenance. This
finite build does not supply multi-partition event time, source-retention
operations or exactly-once external payments/emails.

## Evidence to produce

Complete the log's [milestones](../projects-guided/p07-storage-engine/CHECKPOINTS.md),
[exercises](../projects-guided/p07-storage-engine/EXERCISES.md), tests and experiments.
Then derive a bag/NULL query, reconstruct an index split, trace a manifest
publication and reject a stale read-modify-write plan. Produce new predictions,
test outputs, annotated failure evidence and the
[checkpoint/planning reconstruction assessment](recovery-planning/EXERCISES.md).
Learner evidence must be saved independently of prepared reference outputs.

## Remaining instructional work

The foundational pieces above now contain original worked mechanisms and actual
local experiments. Full SQL/modeling/constraint coverage, broad optimizer search,
external-memory execution/spilling, incremental B+ deletion/rebalancing, LSM
merges, multi-version concurrency, distributed storage, event-time/watermarks,
warehouse/lake operations and live production recovery remain unfinished in the
larger mandate. Source/version/lineage graphs connect to the separately assessed
[provenance build](../security-cryptography-mastery/provenance/LESSON.md).
These remaining full-scope gaps must not be hidden by a bounded STRONG rating.
