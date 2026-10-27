# Predictions, controlled procedure and actual observations

Run `python3 07-databases-data-systems/recovery-planning/experiment.py` from the
repository root. Python3.10+ standard library, local POSIX locking/directory sync,
temporary writable directories and directly spawned child processes are required.
Never direct the kill worker at a process other than its own trusted test child.
The experiment discards its synthetic data when finished and prints JSON; retain
new runs under new names instead of replacing historical observations.

## Questions and predictions

1. Can a killed checkpoint select a mixed image/log pair? Predict old selection
   before replacement and new selection after it, with identical logical state.
2. Can compaction preserve120 commits' final state while reducing suffix replay?
   Predict unchanged global version/live rows and an empty new suffix.
3. Does a serialized write alone protect an increment computed from an earlier
   snapshot? Predict lost update without a precondition and rejection/recompute
   with the global optimistic version.
4. Does a uniform distinct-count estimate remain accurate for a hot key? Predict
  909 estimated outputs versus8110 actual; test a stale row-grant refusal.
5. Does a repeated source batch duplicate local effects? Predict zero new effects
   after checkpoint/reopen. Also predict that mutated old payloads are silently
   skipped, falsifying an unconditional exactly-once claim.

## Controls and instrumentation

Use fixed synthetic keys/values,120 deterministic compaction transactions, the
same source events, the same key distributions and named publication hooks.
Change only the selected kill hook, optimistic precondition, skew/statistics or
source-payload premise for each comparison. Instrument child exit codes, selected
generation identity, reconstructed rows/global version, actual WAL/file bytes,
declared/actual join work and newly applied event counts. Source SHA256 and actual
Python/kernel versions travel with each output. No wall-clock performance result
is inferred from byte counts or work counters.

## Actual executed record

[observed-2026-10-25.json](evidence/observed-2026-10-25.json) is the actual experiment.
[tests-2026-10-25.txt](evidence/tests-2026-10-25.txt) records17 passing test methods.
The publication experiment actually killed8 directly created processes with
SIGKILL: the first four hooks selected the old generation; the remaining four
selected the new. Every recovered logical state and global version agreed.
The current raw JSON contains the exact compaction bytes/file counts and source
hashes, so a changed implementation can be distinguished from a replay.

The stale read-modify-write run ended at2 without a precondition, despite two
intended increments from1. Optimistic rejection plus recomputation ended at3.
The skewed join produced8110 rows while estimating909. The stale row grant was
refused. The immutable batch retry applied0 effects, and altered past payloads
also applied0: source immutability is a premise, not a checked provenance claim.
The separate byte-prefix model checked every cut of one encoded two-operation
frame and exposed either the base or the entire batch, never one operation.

## Interpretation and limits

These results support the declared finite local contracts. An application kill
retains the running kernel/cache; it does not reproduce a controller, power or
filesystem crash. Explicit prefix rewriting is a separate fault model, not an
observed physical torn write. Shared/exclusive advisory locks depend on every
client obeying the same stable-inode protocol. Row grants are not byte quotas;
the cost model is not actual CPU/disk performance. Local stream progress cannot
control remote effects or authenticate a mutable source. Successful tests do
not establish a complete database system or learner mastery.

Follow up by measuring repeated real I/O costs with controlled caches/data sizes;
testing no-space/sync-error recovery; implementing external-memory hash partitions;
and designing independently retained stream-source versions. Such experiments
need new protocols and evidence, not relabeling this record.
