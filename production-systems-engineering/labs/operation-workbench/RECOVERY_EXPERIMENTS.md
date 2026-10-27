# Executed recovery, telemetry and release investigations

Commands from the repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/operation-workbench -v
python3 production-systems-engineering/labs/operation-workbench/recovery_experiment.py
python3 production-systems-engineering/labs/operation-workbench/release_drill.py
```

The actual records are [recovery JSON](evidence/recovery-observed-2026-10-25.json),
[release JSON](evidence/release-observed-2026-10-25.json),
[initial tests](evidence/recovery-tests-2026-10-25.txt) and
[reviewed tests](evidence/recovery-tests-reviewed-2026-10-25.txt).
Historical October23 load/crash outputs remain separate. These are synthetic
local experiments; no physical measurement or learner attempt is asserted.

## Questions, controls and predictions

**Backup:** Does copying the main file retain a WAL-only commit? Keep schema,
data, engine and host fixed. Checkpoint A/B, hold a connection open, disable its
automatic checkpoint, commit D and compare main-only copy with engine backup.
Prediction: main copy can be stale despite a valid structure. Instrument counters,
receipts, source hashes and actual SQLite version, not just file existence.

**Authority:** Can unkeyed consistency prove an original history? On a disposable
copy alter one delta/result/counter coherently and recompute all hashes. The
negative control predicts acceptance by consistency checks and refusal against
an independently retained conflicting receipt. Never test on another person's
data or alter the original snapshot.

**Telemetry:** Does averaging per-worker p95 reproduce pooled p95? Use the exact
99-at1/one-at100 population, fixed boundaries and sorted nearest ranks. Separately
enumerate3125 five-event populations over `[0,1,2,5,10]` and check pooled buckets
against direct indicator sums. Change shard membership, not the quantile definition.

**Release/recovery:** Can a healthy process violate an old response? Start stable,
retain A5/B12, kill that direct child process, run the explicit response mutant,
test A, then restore stable code. Keep schema/data/old-client contract fixed.
Add C, demonstrate stale-restore refusal, take a newer generation and restore
offline. Instrument returned responses, child lifecycle and explicit elapsed
boundaries; all spawned servers bind only loopback and are cleaned up.

## Actual observations and interpretation

The initial local run used Python3.12.14 and SQLite3.53.1. Main-only backup counter
was12; engine backup counter was16. The consistently rewritten artifact passed
consistency verification; the external D receipt blocked promotion. A newer C
receipt also blocked the stale original generation. This shows both a real
WAL omission and limits of unkeyed/internal evidence; it does not show malicious
tampering is impossible or that an external inventory is complete.

Pooled p95 upper bound was1; the incorrect mean of shard p95 was50.5. Ten/one-bad
and thirty/three-bad windows each had exact burn2 and triggered the chosen rule.
These finite arithmetic checks do not estimate future traffic reliability or
calibrate false alarm rates. An alternative bucket layout would alter bound
resolution; overlapping shards would alter the population itself.

The mutant returned12 for A; restored stable code returned the original5.
The final restored database had counter16, three operations and three matched
external receipts. The first measured restore-through-health-and-shutdown
interval was61,348,837ns; its exact boundary is retained with the value. It is
one host observation, not a speed benchmark, service RTO or promised deadline.
Scheduling/caches/startup explain timing variation and require repeated trials.

Separate-reader review found three telemetry contradictions that author tests
missed: a summary could claim good overloads, an empty population could have a
nonzero sum, and an aggregate could return a deadline outside its validator's
range. The repair checks result composition and the two semantic restrictions;
new regressions cover all three. The pre-repair and reviewed test logs are
retained. Fresh [reviewed recovery output](evidence/recovery-observed-reviewed-2026-10-25.json) and [reviewed release output](evidence/release-observed-reviewed-2026-10-25.json) use distinct filenames to preserve history.

## Limits and follow-up

Process kill retains a running kernel's caches. No power cut, disk reorder,
full-disk, network partition, protected remote backup, authenticated deployment
or service-scale load was executed. The attacker experiment controls both a
disposable snapshot and unkeyed hashes; independent authority is an assumption.
The restore requires trusted immutable source and exclusive offline destination.
Callbacks do not interrupt stalled native calls. Header-level security, long-term
retention, secret custody and real client SLO agreement remain outside this build.

Next experiments: freeze a real source transaction while a concurrent writer
progresses and characterize snapshot selection; kill a publisher at each sync
boundary using an isolated filesystem fixture; vary data/caches across repeated
restore measurements; inject missing/overlapping event windows; rehearse a
backward-compatible migration on disposable data. These are proposed procedures,
not additional observed results.
