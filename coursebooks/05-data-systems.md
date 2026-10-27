# Data systems: meaning, query execution and recovery

This developed route uses original WAL, relational and isolation mechanisms.
The full coursebook remains PARTIAL: page layout/B+trees, optimizer design,
compaction, broader concurrency control, streaming and distributed storage still
need deeper implementation and instruction.

## Preserve distinctions before optimizing a query

A missing measurement, known zero and absent row are different states. In SQL,
`amount=NULL` is unknown and is not retained by WHERE; `amount IS NULL` asks a
presence question. A left join first introduces a NULL-extended row for an
unmatched left input, but a later WHERE on a right amount can remove it. Moving
the same predicate into ON changes the preserved result. Read and hand-evaluate
[the SQL unit](../programming-languages-mastery/11-sql/units/null-and-joins/README.md)
before treating an executable query as a correct scientific question.

The [query/isolation unit](../07-databases-data-systems/query-isolation/README.md)
implements bag selection/join/grouping and differentially checks exact results
against SQLite. An index can change access work while preserving query meaning;
its existence does not justify changing which NULLs, duplicates or rows count.
Bind values separately from SQL structure. A correct aggregate over a biased
collection remains a biased description of the target population.

## A successful write response carries a failure contract

The [storage-engine project](../projects-guided/p07-storage-engine/README.md)
frames complete transactions with a CRC, scans recovery state and distinguishes
a torn tail from corrupt committed content. It tests every cut position and
poisons an object after uncertain synchronization failure. Reopening can reveal
bytes written before the caller observed an exception; blind retry can duplicate
an operation. CRC detects selected corruption patterns, not malicious authenticity.
The [provenance build](../projects-guided/p09-secure-pipeline/README.md) supplies a
different authenticated-history mechanism with its own key/trusted-tip assumptions.

## Isolation describes schedules, not one magic transaction keyword

In the locally observed SQLite WAL schedule, an existing reader retains its
snapshot while another connection commits; a fresh reader sees the later values.
A stale reader trying to upgrade to a writer can be rejected. A read/application-
compute/write sequence can overwrite a newer balance unless the operation and
transaction semantics preserve the intended invariant. The unit retains actual
engine/version, exact schedules and result codes; no cross-engine equivalence
is inferred from this one backend.

Exit: derive an outer-join result, reconstruct a WAL recovery boundary and trace
two transaction schedules with predicted/actual values. Explain durability,
atomicity, isolation, authenticity and measurement truth separately. Add a
counterexample where each one alone fails the application's desired guarantee.
