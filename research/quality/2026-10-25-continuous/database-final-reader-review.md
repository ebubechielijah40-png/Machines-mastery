# Independent recovered database review —2026-10-25

Reviewer: recovered_database_gate, separate from the author of the new database
mechanisms. This is an internal team review, not an external specialist audit,
physical durability certification, production deployment or learner assessment.
Only database-final-reader* evidence files were written by this reviewer.

## Inspected scope and preserved boundary

Read AGENTS.md, DEPTH_STANDARD.md, current progress, the immutable databases card
in registries/strong_progress.json and the connected database route. Inspected
the recovered recovery-planning store, planner, stream, tests, complete lesson,
22 exercises, separated hints/solutions, experiment protocol/raw evidence and
source map. Reviewed representative existing query/isolation, byte-page index
and transactional WAL instruction and reran their suites.

The frozen scope fingerprint remains
`573d7e18d7ace1de6c7d2d8e8e2090ffcfa97d86f819268f3aa62e2139b07516`.
No scope, denominator, criterion weights or registry scores were changed.
The later uncommitted event-time build was pruned before recovery; no such code,
test or result is counted. The recovered stream is one immutable ordered source
partition with grouped count effects and one consumed offset.

## Actual fresh execution

[Exact commands and logs](database-final-reader-tests.json) record53 passing
Python test methods:17 recovery/planning,16 page index,10 query/isolation and10
WAL tests. The new suite actually creates and kills its own direct child
processes at eight publication phases, checks lock release and two serialized
writers, exercises explicit tail repair, tombstones, optimistic conflicts,
transactional source replay, join multiplicities and resource failures.
An application SIGKILL leaves the host kernel and its caches alive; none of
these tests is relabeled as a physical power-loss observation.

The independently selected [reader probe](database-final-reader-probe.py) and
[raw output](database-final-reader-probes.json) add the following checks:

- A batch deletes, replaces and deletes the same base key while retaining both
  signed64 key extrema. Checkpoint/reopen preserves the expected state.
- A stale optimistic write leaves every retained file byte hash unchanged.
- An unselected invalid generation does not change selected state and is
  collected only after a valid replacement is published.
- A complete checksum-invalid frame makes both snapshot and repair refuse;
  its evidence bytes remain unchanged rather than being truncated as a tail.
- 729 pairs of three-key multiplicity vectors are executed by each of nested,
  forced left-build hash and forced right-build hash plans:2187 comparisons
  against an independent product-of-multiplicities Counter oracle. Duplicate
  complete rows and negative keys are retained correctly.
- An extreme-valued stream contribution cancels to a retained zero total;
  another group remains−7. Checkpoint/reopen/replay preserves the source and
  offset, applies zero duplicate effects, and rejects a gap without byte changes.

The JSON retains actual Python/platform and SHA256 of all three new mechanism
files. These probes are additional finite examples, not a proof of every
history or a general database correctness theorem.

## Technical and instructional judgment

The base-plus-suffix representation is taught accurately. The worked deletion
counterexample explains why suffix.data cannot simply update a checkpoint:
an empty-state dictionary loses tombstones. Global version versus local frame
sequence is explicit and remains stable across checkpoint. Publication orders
dependent image/suffix creation and synchronization before CURRENT replacement;
selected corruption fails instead of guessing an older, possibly stale state.

The stable-inode advisory lock and exclusive collection argument are coherent
under the declared cooperating-client/local-filesystem contract. Snapshot,
commit, repair and checkpoint do not silently upgrade shared locks. The
optimistic precondition correctly addresses a stale client computation that
serialized writes alone cannot fix. The text distinguishes rejected writes
from uncertain acknowledgement after a complete append/sync boundary.

Join instruction derives `sum(Lk*Rk)`, preserves bags, distinguishes estimates
from results and states transparent work units. It does not pretend row grants
are byte quotas or that Python hashing is an external-memory database executor.
The skew/grant failures are meaningful negative controls. The stream induction
correctly depends on immutable source identity/history and one transaction
covering progress plus effects. Mutated historical payloads and remote effects
are explicitly outside that conditional guarantee.

The lesson supplies mechanisms and intermediate examples rather than directions
to explain them later. Assessments require publication schedules, invariants,
duplicate counterexamples, cost derivation, failure reasoning, reconstruction
and transfer. Explained solutions are separated from the learner attempt.
Prerequisite links connect proofs/programming, WAL, query meaning and byte pages
in a usable order. The new unit is a substantial bounded educational build.

The source map records exact primary scopes and intellectual/implementation
boundaries. This reviewer checked that map and its connections; fresh original
web-page inspection is attributed to the author, not invented as this reader's
work. No full books, external benchmarks or unavailable physical studies are
represented as reconstructed. Runtime/hash evidence is separate from source
documentation versions and rights statements.

## Recommended score and gate

| Criterion | Four marks | Score | Reviewed reason |
| --- | --- | ---: | --- |
| Instruction |2,2,2,1|87.5|Substantial worked mechanisms and failures; full frozen breadth still incomplete.|
| Implementation |2,2,2,1|87.5|Runnable publication/locking/compaction/planning/local stream internals; wider streaming remains absent.|
| Reproduction |2,2,2,2|100|Fresh suites, independent multiplicity/state probes and real controlled failure tests.|
| Assessment |2,2,2,1|87.5|Specific separated tasks, explained solutions and transfer; broader domain assessment unfinished.|
| Prerequisites |2,2,2,1|87.5|Coherent taught route and observable milestones; later streaming prerequisites still need units.|
| References |2,2,2,1|87.5|Exact selected maps, environment/hashes and honest limits; broader scope verification remains.|

With25/20/20/15/10/10 weights, readiness advances80.00→90.00. Core tests pass,
independent review is present and no critical conceptual error was found in
the inspected mechanisms. The bounded recovery/planning/local-stream unit
merits STRONG after integration checks.

**The complete unchanged databases domain remains PARTIAL.** Its frozen scope
explicitly retains broad streaming as unfinished. One strictly ordered immutable
partition does not teach partition coordination, event time versus processing
time, out-of-order/late data, watermark/window finalization or the corresponding
failure/restart boundary. No recovered implementation supplies those mechanisms.
This reader therefore sets scope_breadth_confirmed=false despite90.00 readiness.
The numeric threshold cannot substitute for that qualitative gate.

The next concrete local closure is an assessed bounded multi-partition/event-time
investigation with a separately computed batch oracle, explicit late-data/window
policy and a stated durable progress/restart contract. It needs no new external
permission, private dataset or hosted service. Estimated3–7 active development
and review hours, low confidence, is an engineering range rather than a promise.
Broader SQL/optimizer search, spilling, MVCC, distributed storage, production
operation and original full EXCELLENT breadth remain separately PARTIAL.
