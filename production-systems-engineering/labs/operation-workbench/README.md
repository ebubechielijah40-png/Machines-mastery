# From a correct operation to an observable, recoverable service

A counter can add correctly and still fail its user: a retry can add twice, an
old result can be replaced with a new total, or a queue can hide seconds of delay
behind a fast database query. This original build makes those failures visible
at one small boundary. It runs actual threads and SQLite transactions on local
files. It has no public HTTP endpoint, deployed infrastructure or contractual SLA.

Before starting, work through [Python entry](../../../02-programming/python-entry/README.md),
[process/synchronization reasoning](../../../05-operating-systems/SELF_CONTAINED_GUIDE.md)
and [transaction/isolation schedules](../../../07-databases-data-systems/query-isolation/README.md).
Know fractions, percentiles, a transaction's commit point and the difference
between elapsed time and CPU work. The earlier [ledger](../event-ledger/README.md)
is a useful comparison: its bounded cache assumes a single writer; this unit
uses no cache and makes concurrent request identity an explicit storage invariant.

## Define the user's operation before choosing a metric

The operation is `(request identity, integer delta)`. A first successful identity
changes one counter and stores the result returned at that commit. An identical
retry returns that stored result. Reusing the identity for a different delta is
a conflict. Request labels are not authentication, and the same label cannot be
safely shared by unrelated principals in a real system without an identity policy.

Suppose A adds5, producing5, and B then adds7, producing12. A's retry must return5,
not the current counter12. Returning12 would preserve the final state but change
A's response. Store both the delta and original response with A. An idempotent
*effect* and an idempotent *response* are different contracts.

The two required invariants are:

1. Counter = sum of deltas in the retained operations table, from initial zero.
2. Each retained identity has exactly one immutable `(delta, result)` pair.

`BEGIN IMMEDIATE` obtains the SQLite writer transaction before looking up the
identity. If the identity is absent, update the counter and insert the response
in that transaction. Commit makes both changes visible together. A conflict or
precommit exception rolls back both. A second writer cannot sneak a competing
same-key insertion between lookup and update while the first writer transaction
holds its place. It can wait or receive a busy failure instead. This is a local
serialized database argument; it does not establish a distributed global order.

The proof assumes the database/schema are trusted, all writers use this path,
keys are retained and the counter starts at zero. Directly editing a row, deleting
deduplication history or routing a retry to an unrelated database breaks premises.
No finite retry policy can turn a discarded identity into a permanent guarantee.

## Follow the states across a lost reply

| Last reached phase | State after reconnect | Safe action with the same retained identity |
| --- | --- | --- |
| Before commit; transaction rolled back | No effect/no stored response | Retry may apply the operation |
| Commit returned, response discarded | Effect and response retained | Retry returns the retained response |
| Commit outcome not known to caller | Cannot infer state from silence | Reconcile by identity; do not invent a new identity |

`fault='after_commit'` deliberately raises `UnknownOutcome` after an actual
commit. This models a lost reply, not a failed write. The controlled process
experiment also kills a directly spawned application process while it is parked
before or after commit. Those are observed application crashes. They are not
power cuts, kernel crashes or tests of a disk controller's flush promises.

The file database uses WAL and `synchronous=FULL`. Selected SQLite primary
semantics are mapped in [SOURCES](SOURCES.md). A successful local crash test is
still weaker evidence than a durability guarantee over all hardware/filesystems.
The repository's [original WAL build](../../../projects-guided/p07-storage-engine/README.md)
teaches framing/recovery below this library boundary; do not attribute that
mechanism's implementation to this SQLite wrapper.

## Bound work before accepting it

The experiment service has two worker threads and six admission slots. A slot
covers a running **or waiting** request, so at most six operations have been
admitted concurrently. `ThreadPoolExecutor` alone does not give this bound: its
internal waiting work could grow while callers continue submitting. Acquire a
nonblocking semaphore before submission, and release it in the worker's finally
block. An unavailable slot produces an immediate overload observation.

The finite measurement session accepts at most4096 eligible offers by default.
After that it explicitly refuses a new window; it does not silently discard old
measurements and leave the denominator wrong. This bound is for a lab session.
A real service needs durable/streamed metric aggregation and retention policies.

Before applying an operation, the worker checks the request's elapsed deadline,
including waiting time, then checks again after the injected dependency delay.
Already expired queued work has no effect. A started SQLite operation can still
finish after the target: these checks are not instruction-level cancellation or
a hard bound on filesystem stalls. It is recorded as slow even if it commits.
If a caller independently abandons a running write, reconciliation remains
necessary; cancellation of a future does not undo a transaction already committed.

## Instrument the boundary that the user experiences

For each eligible operation record four clock readings:

- `issued`: intended arrival in the controlled generator;
- `offered`: when the generator actually submitted the operation;
- `started`: when a worker began, or immediate admission rejection time;
- `ended`: when the finite result was observed.

The ordering is `issued ≤ offered ≤ started ≤ ended`. Therefore

`latency = (offered-issued) + (started-offered) + (ended-started)`.

These terms are generator lag, queue wait and worker residence. They are all
elapsed durations. SQLite work, lock waiting and an injected sleep contribute
to the last term; a single residence number cannot separate them. Record process
CPU time separately. Sleeping consumes elapsed time without equivalent CPU work.
`perf_counter_ns` supplies interval readings; the integer nanosecond unit is not
a claim of nanosecond clock accuracy. The primary timer scope is in SOURCES.

The generator uses scheduled arrivals. Request i is intended at `start+i*gap`.
If it falls behind, it retains that intended timestamp, so generator lag appears
in latency instead of silently disappearing. A sequential client that waits for
one reply before making the next slows its offered load when the system slows.
It answers a different question and can conceal queue pressure. Our finite
single-process generator also consumes scheduling resources and is not an ideal
independent arrival source; inspect its actual lag in the raw observations.

## Derive the SLI, budget and burn rate

The declared eligible population is every syntactically valid operation offered
during this finite session, including overload, deadline, conflict and unknown
responses. Invalid schema calls are rejected before entry into this population.
That choice is explicit; a customer-facing metric might use another justified
boundary. A good event has a known successful or duplicate response **and**
`latency ≤30 ms`. A fast overload response is bad.

For N eligible events and G good ones, SLI=G/N when N>0. For target t=0.95,
permitted bad events are `N(1-t)`. With B=N-G, remaining budget is `N(1-t)-B`.
Burn rate is `(B/N)/(1-t)`: bad-event rate relative to its allowed rate.

Example:100 offers,90 good,10 bad. The budget permits5 bad;5 too many were used.
Burn rate=.10/.05=2, and the SLO fails. If another90 offers are rejected in1 ms,
reporting the successful10 requests alone would manufacture100% success. The
correct denominator is100 eligible offers. An empty window has no defined ratio
and no pass; the implementation returns null for its SLO result.

Use exact fractions for counts/budgets, then convert ratios for display. With40
requests this target permits2 bad events. A single event changes the measured
ratio by2.5 percentage points. One small run passing95% is not a confident
estimate of long-term95% reliability or a policy agreed with actual users.

Sort a sample of n latency values. This lab defines quantile q by nearest rank,
index `ceil(q*n)-1`. For `[1,2,9,100]` ms, p95 is100 ms. Another interpolation
convention can report another number. State the convention and denominator.
Aggregating shard p95 values by averaging is generally not the p95 of all
requests: merge the samples or compatible histogram counts first.

## Build it in milestones

1. Write the A/B/retry trace by hand. Implement a single transaction and prove
   which statements commit together. Compare against an incorrect two-commit build.
2. Store identity, delta and original response. Test same/different payload retries
   and concurrent same-key calls. Distinguish a busy response from a lost commit.
3. Add a finite record type and four timestamps. Verify conservation of eligible
   offers even when admission rejects work. Do not calculate SLOs from successes only.
4. Add workers plus a running-and-waiting semaphore. Use an event-gated worker to
   force overload; do not rely on the host randomly getting busy.
5. Add pre-application deadline checks, then demonstrate that already-started
   operations are not safely undone by ignoring their replies.
6. Execute paired load cases and the two process-crash phases. Derive a corrective
   action from the observed bottleneck, then inspect what the correction trades away.

Reference: [operations.py](operations.py). Try the milestones and
[exercises](EXERCISES.md) before opening [hints](HINTS.md) or [solutions](SOLUTIONS.md).
The test suite is an independent observable contract, not a requirement to match
private variable names. Do not read the reference first and call transcription
an unaided reconstruction.

```sh
python3 -m unittest discover -s production-systems-engineering/labs/operation-workbench -v
python3 production-systems-engineering/labs/operation-workbench/experiment.py
```

Tests cover rollback, unknown reply/restart, competing same-key threads, original
response retention, finite admission, queued expiry and exact SLO arithmetic.
[Experiment procedure and actual observations](EXPERIMENTS.md) and
[the observed incident analysis](INCIDENT.md) explain what ran and what did not.

## Operating and extending the boundary

Metrics needed for this build include eligible/good/status counts, generator lag,
queue/residence/total samples, active admission, durable operation count and
identity conflict count. A real request trace would attach a correlation ID to
all stages; high-cardinality request IDs do not belong in every metric label.
Separate counters/histograms from detailed bounded logs. Do not log real private
payloads or keys just to imitate an observability stack.

A release should pin runtime/schema/configuration, validate migrations on a copy,
exercise an old client against the new version and check a rollback path. Reverting
application code cannot automatically reverse an incompatible schema/data change.
Back up through an engine-supported consistent snapshot rather than copying an
active database file while ignoring its WAL. Restore into another location,
validate invariants and reconcile known operation identities before promotion.
The next [recovery and observability build](RECOVERY_AND_OBSERVABILITY.md) now executes create-only backup/restore, pooled telemetry and a loopback release/rollback rehearsal. Protected remote deployment and service-scale operation remain unfinished.

For an exposed version, add authenticated principal-scoped identities, transport
security, byte/connection limits, authorization and durable retention limits.
Enforce overload before expensive work. Add bounded retries with the same key,
backoff/jitter and a total attempt deadline; blind retry storms can consume the
remaining capacity. Durably coordinate key expiry with the maximum retry horizon.
This original lab makes those design decisions visible; it is not a secure
internet service, production orchestration platform or a full SRE course.
