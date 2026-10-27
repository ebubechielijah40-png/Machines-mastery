# Recover the user's contract, then explain the service

A restart that opens a database is weaker than a recovery that preserves what
users were told. If A received5, B received12, and A's retry receives12 after a
restore, the counter may still be correct while the API contract has changed.
This build connects storage consistency, externally retained receipts, release
compatibility and population-correct telemetry. It runs actual local processes,
SQLite files and loopback HTTP. It teaches operational mechanisms, not a secure
public server or an assurance about a datacentre.

First complete the [operation workbench](README.md): trace A(+5), B(+7), A(retry),
explain a commit point, calculate good/total events, and distinguish a lost reply
from a rolled-back effect. For the lower storage layer, study the
[transaction-frame project](../../../projects-guided/p07-storage-engine/README.md).
For HTTP byte boundaries, use the [framing lesson](../../../06-networking/stream-boundaries/LESSON.md).
Python dictionaries, files, exceptions, fractions, SQL transactions and process
lifetimes are prerequisites; the linked routes teach them before this build.

## What a snapshot must retain

The live state contains a counter and an operation table. A row stores identity,
delta and original result. A recovery unit must keep these together. Backing up
only the counter loses retry identity; backing up only the identities loses the
effect and response. A byte copy made while the live engine can change its
storage may not correspond to one transactionally consistent state.

In WAL mode, committed changes can remain in the WAL while the main file still
contains an older state. Our controlled experiment first checkpoints A and B
into the main file, keeps a connection open, disables its automatic checkpoint,
then commits D(+4). The main file can still say12 while a normal engine reader
sees16. Copying just that main file produces a valid-looking **older** database.
An integrity checker need not reject it: consistent old data is not corruption.

`create_backup` uses SQLite's backup interface through Python. The engine owns
the page-copy and consistency protocol. This is deliberately a library boundary;
our original code supplies generation handling and verification, not SQLite's
internal locking implementation. The selected source scopes are in
[RECOVERY_SOURCES](RECOVERY_SOURCES.md). A completed consistent snapshot is not
necessarily the latest wall-clock state when another writer can progress.
Measure the point represented by the snapshot instead of inventing a timestamp
guarantee from the function name.

Each generation is a new directory with `snapshot.db` and `MANIFEST.json`.
The manifest records a byte digest, a digest of canonical logical state, counter,
operation count, file size, creation time and the actual SQLite version. Its
creation time is an informational wall-clock reading; it neither authenticates
the snapshot nor orders all operations in a distributed system.

Creation proceeds in this order:

1. Create a new generation; an existing one is never overwritten.
2. Ask the engine to copy into a new target in finite page batches.
3. Close copying connections and make the target a self-contained database file.
4. Read one transaction without creating or repairing tables. Check structure,
   expected tables/columns, bounded rows, valid identities/deltas/results and
   `counter = sum(retained deltas)`.
5. Sync the database, then create and sync the manifest, then sync the generation
   directory and its parent. Readers require a complete verified generation.

The filesystem operations describe a POSIX protocol under trusted-directory and
honest-storage assumptions. A killed process may leave an incomplete generation;
a missing manifest prevents promotion. We did not execute a power cut, filesystem
reordering test, full-disk fault or controller-failure experiment. A callback's
elapsed budget is checked between backup steps and cannot interrupt a stalled
native call. The32MiB/10,000-row limits are teaching bounds, not hard kernel disk
quotas or a hostile-input execution sandbox.

## Consistency, authenticity and freshness answer different questions

The byte digest detects a changed file when the expected digest is preserved.
The logical digest checks the representation that this version understands.
The counter invariant detects some inconsistent edits. None proves that every
original result occurred in one historical commit order: rows are sorted by
identity, and that order is not commit order. Nor does a digest authenticate a
file against an adversary who can replace both the file and its manifest.

The experiment intentionally changes D's delta4 to8, result16 to20, counter16 to20,
and recomputes both unkeyed digests in a disposable copy. Consistency verification
accepts the internally consistent false history. A separately retained receipt
`(D,4,16)` blocks its promotion. This negative control makes the trust assumption
observable. Authentic manifests require an independently protected expected
digest or suitable authenticated authority; the [provenance lesson](../../../security-cryptography-mastery/provenance/LESSON.md)
teaches that boundary. This lab supplies neither remote authority nor key custody.

Restoration first verifies a generation and compares all caller-supplied external
receipt triples with its retained rows. Only then does it copy to a new offline
destination, verify the restored bytes/state, and sync that destination's parent.
An existing main file or WAL/SHM/journal sidecar blocks this procedure. Never
replace a database behind an active process: open descriptors and sidecars can
refer to a different state than a new filename suggests. The caller must ensure
the destination is offline and the generation is immutable throughout verification
and copying; these are trusted-path operations without concurrent publishers.

Suppose the backup has A5 and B12. Later C(+4) receives16. Restoring that backup
with the C receipt must fail: C is absent. Restoring with only A/B receipts can
pass while losing C. Thus this check establishes agreement with the supplied
external evidence, not completeness of every real user's history. An empty
receipt list cannot justify zero recovery-point loss.

Define a recovery point by the latest recoverable operation or data boundary,
and define recovery time by explicit start/end events. The release drill measures
restore start through process startup, three HTTP checks and shutdown. It records
that actual elapsed interval, not a pure file-copy duration or promised service
RTO. Comparison across hosts needs repeated trials and equivalent data, caches,
filesystem, runtime and boundary definitions.

## Why distributions must be merged before choosing a percentile

For observations x1…xN and increasing bucket bounds b1…bm, retain cumulative
`Cj = count(xi ≤ bj)`, total N, sum S, and overflow `O = N-Cm`. These invariants
hold: `0 ≤ C1 ≤ … ≤ Cm ≤ N` and `Cm+O=N`. Compatible **disjoint** populations
can be pooled by adding each Cj, N, S and O. Counts are additive because each
event belongs to one contributing population. Repeating the same population
double counts it; format validation cannot determine event membership.

For a nearest-rank quantile q, calculate `r=ceil(qN)`. The first bound with
`Cj ≥ r` is an upper bound on the observed quantile. It is not the exact
latency and does not assume uniform observations inside that bucket. If no
finite bucket contains the rank, return null with overflow information. An
empty population also returns null; inspect N to distinguish the two cases.

Example: workerA has99 requests of1 unit each; workerB has one request of100.
A's p95 is1, B's p95 is100; averaging gives50.5. Pooled population size100 has
rank95, whose value is1. The correct pooled p95 is1. An average of percentile
values ignores how many events generated each value. The histogram retains
counts `[99,100]` at bounds `[1,100]`, so rank95 falls in the first bucket.

Telemetry status labels come from ten fixed categories. Request IDs belong in
bounded diagnostic records, not in a new metric series for every request.
Otherwise cardinality grows with traffic and memory/retention costs grow with
the number of identities. Correlation records should connect offered, started,
committed and replied stages; a metric counter cannot reconstruct a particular
user's missing acknowledgement. Real payloads and keys are not needed in this
synthetic exercise. `validate` checks histogram shape and conservation, not
that a sender measured genuine events or that counts have causal meaning.

## Derive a transparent alert rather than declaring reliability

For target t, N eligible operations and G good ones, `bad=N-G` and
`burn=((N-G)/N)/(1-t)`. With t=.95 and a ten-event window having one bad event,
burn=(1/10)/(1/20)=2. A thirty-event window with three bad events also has burn2.
The teaching rule alerts only if both windows have enough events and burn≥2.
Here minimum populations are10 and30. These chosen constants illustrate a
mechanism; they are not statistically calibrated thresholds or external advice.

Normally the short window is a suffix of the long window. Do not add their
counts: their events overlap. The caller selects membership/chronology; our
summary has no event-time index to verify that relationship. A short spike with
an otherwise healthy long window does not pass this two-window rule. A sustained
small-volume incident can remain below the population requirement. Empty windows
are insufficient evidence, never100% success. Increasing a deadline can improve
the reported good ratio without making any operation faster. Preserve the
policy and denominator with the measurement.

## Rehearse a release against an old user's expectations

`local_service.py` binds only127.0.0.1 on an ephemeral port. It has a readiness
read and a POST operation with the same two-field contract as the store. The
server is serial; previous threaded admission/load experiments remain the
concurrency study. This local server has body-length/schema checks and a socket
timeout, but Python's basic HTTP server is not a public security boundary.
Do not infer protection against arbitrary local clients, header attacks or
denial of service. It has no authentication, TLS or production request budgets.

The compatibility probe records A's result5, adds B to reach12, then retries A.
Stablev1 returns5. The explicit `mutant-current-response` release returns12.
Checking only a health endpoint or final counter would miss that regression.
The drill rejects the mutant, stops it, starts stablev1 on the same database,
and verifies original responses. Reverting code works here because the schema
and stored representation did not change. A destructive migration cannot be
undone by changing an executable: use a separately tested backward-compatible
schema path or a restore/reconciliation procedure with an accepted data boundary.

The drill actually kills a stable application process, starts the mutant,
rolls it back, tests a stale restore refusal, takes a newer snapshot, restores
to another file, and verifies health plus A/C retries. Killing a process retains
the running kernel's caches; this evidence is weaker than a physical durability
experiment. A local port listening is also weaker than a routed, authenticated,
monitored deployment serving real clients. Keep these limits in incident reports.

## Build and assess the operational boundary

1. Write the A/B/retry state and response table. Explain why summing deltas is
   necessary but insufficient for original-response correctness.
2. Implement new-generation backup and one-transaction logical validation.
   Force a WAL-only commit and predict the naïve-copy outcome before running it.
3. Restore only to an unused offline file. Test missing/newer/conflicting external
   receipts, byte damage, incomplete manifests and consistent hostile rewriting.
4. Implement cumulative buckets and pooling. Check conservation, incompatible
   configurations, overflow and an independently sorted percentile example.
5. Calculate both window burns by hand. Encode an explicit population/deadline
   policy and demonstrate a blind spot without changing the denominator.
6. Add process lifecycle/readiness, old-client compatibility, release rejection,
   rollback and restore. Record exact runtime, source hashes and elapsed boundary.

Deliver a prediction sheet, implementation, test log, unedited raw observations,
one annotated failure trace and a short operational decision supported by evidence.
Assessment allocates25 points to state/receipt reasoning,20 to safe generation
handling,20 to meaningful negative controls,15 to telemetry arithmetic,10 to
release compatibility,10 to limitations/reconstruction. A passing total cannot
compensate for overwriting a live file, accepting a conflicting receipt or
claiming a public reliability guarantee from this lab.

Try [the exercises](RECOVERY_EXERCISES.md), then [hints](RECOVERY_HINTS.md), then
[explained solutions](RECOVERY_SOLUTIONS.md). Reconstruct the manifest protocol,
histogram merge and old-client probe without the reference. Transfer to a job
queue: explain which external job effects lie outside the SQLite transaction
and which receipts would be needed to reconcile a restored queue.

Run from the repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/operation-workbench -v
python3 production-systems-engineering/labs/operation-workbench/recovery_experiment.py
python3 production-systems-engineering/labs/operation-workbench/release_drill.py
```

The [experiment record](RECOVERY_EXPERIMENTS.md) separates predictions, actual
observations and interpretations. The original workbench, cluster and model
serving labs remain available. Remote operations, host failure, sustained-scale
profiling, authenticated deployment, protected backup custody and service-wide
recovery remain unfinished in the larger production mandate.
