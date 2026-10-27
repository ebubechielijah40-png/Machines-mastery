# Controlled synchronization experiments

## S1: Exhaustive finite schedules

Question: can indivisible reads and writes still lose an update? Hypothesis:
separate read/modify/write permits final one; a whole critical section or RMW
excludes it. Hold two workers, initial zero, unit increment and sequentially
consistent transitions fixed. Vary only protocol across split, store-only lock,
whole lock and fetch-add. Enumerate all legal completed paths, record final-value
counts and one failing trace. The combinations-based test independently checks
the 20 split schedules.

The actual executed model returns split `{1:18,2:2}`, store-only lock
`{1:36,2:6}`, and two final-two paths for each correct variant. These are path
counts, not probabilities or sampled OS schedules. The lock variants introduce
extra primitive events, so comparing their total path counts is not a timing
comparison. A different transition granularity changes path counts.

## S2: Defined actual C lost update and repairs

Question: is the split-operation mistake observable without invoking a C data
race? Hypothesis: if both atomic loads precede both atomic stores, both workers
store one; RMW and a whole mutex produce two. Instrument loaded values, ready
count, start gate and final value. Main opens the gate after both loads in the
split case. Each of three modes runs 20 times per compiled configuration.
The harness holds source/compiler/warnings fixed while varying O0/O2/UBSan.

Run `python 05-operating-systems/synchronization/code/experiment.py`.
[evidence/observed.json](evidence/observed.json) retains actual command arrays,
stdout/stderr/status and environment. Every recorded split run passes assertions
for final one and both loaded values zero; repaired modes pass final-two checks.
No unsynchronized plain-integer experiment was executed. Twenty forced runs do
not estimate the frequency of a natural scheduling race. UBSan is not a thread
race detector, and passing it does not prove absence of all data races.

## S3: Predicate wait versus wakeup

Question: which failures arise from skipping a predicate recheck or splitting
release/registration? Hold one item, one producer/consumer, mutex exclusion and
notification semantics fixed. The correct while variant completes all two paths
without the optional wake and all six paths with at most one optional wake.
The if variant with that budget has five completed paths and one safety-failure
path. The split-wait variant without it has four completed and two blocked paths.
All are executed model results with explicit bounded assumptions.

Inspect the complete counterexample traces. The safety witness consumes empty
after a modeled wake without data. The liveness witness signals with no waiter,
then registers too late and blocks despite full=true. An actual runtime need
not exhibit either witness spontaneously; enumeration exposes permitted model
orders directly. Follow up by adding a second consumer and preserving its item
identity rather than assuming one notification reserves one item.

## S4: Actual one-slot transport

Run the same harness: it compiles and executes condition.c under all three
configurations. Control the 1..100 input sequence, slot capacity and predicate
protocol. Measure exact sequence assertions, items, sum, final emptiness and
producer/consumer wait counts. Actual recorded runs show 100 items, sum5050 and
empty-after-join. Wait counts differ across runs/settings and are preserved raw;
no fixed wait count or speed claim is expected.

Alternative explanations: a correct sum alone could hide reordered or duplicate
items, so each next value is checked too. A successful finite run could miss a
rare bug, so the invariant and separate models remain necessary. The toy models
omit allocation errors, cancellation, additional workers and weak memory;
the C implementation adds real API/lifecycle behavior but does not exhaust
host schedules. Extend one dimension at a time and retain failures honestly.
