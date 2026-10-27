# Actual load, deadline and process-failure experiments

Read the operation identity and SLI definitions in [README](README.md). Predict
which offers will become bad events before executing:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/operation-workbench -v
python3 production-systems-engineering/labs/operation-workbench/experiment.py
```

The retained [observed.json](evidence/observed.json) is an actual2026-10-23 run
using Python3.12.14, SQLite3.53.1 and GCC13.3.0 for other native labs. This
experiment itself uses SQLite through Python. It includes code hashes, monotonic
clock properties, every request's timestamps and final counter/operation rows.
Do not replace it when recording a follow-up. The separate raw test logs cover
controlled contracts; a reference test pass does not certify a service SLO.

## Hypothesis and controlled variables

Two workers can overlap injected sleep, but each admitted request occupies a
slot while waiting and running. At4 ms spacing the offered rate is250/s; a12 ms
sleep alone requires average concurrency3 before database overhead. Two workers
cannot sustain it indefinitely. The six-slot bound limits admitted work rather
than creating more capacity. Predict growing wait followed by deadline/overload.

Each finite case offers40 distinct +1 operations, uses2 workers,6 slots and a
30 ms good-event target. Change only dependency delay between light and slow;
then keep the slow delay and change arrival spacing. Arrival `issued` timestamps
retain intended schedule time, including generator lag. Record actual intervals,
queue wait, worker residence, CPU/elapsed time and statuses.

| Actual case | Delay | Arrival spacing | Good/eligible | Status counts | p95 total | p95 queue |
| --- | --- | --- | --- | --- | --- | --- |
|light|1 ms|4 ms|40/40|40 ok|4.740197 ms|.178194 ms|
|slow dependency|12 ms|4 ms|6/40|6 ok,23 deadline,11 overload|36.146772 ms|23.906875 ms|
|paced slow dependency|12 ms|8 ms|40/40|40 ok|15.920601 ms|.088085 ms|

The slow case used8.560365 ms process CPU over188.918797 ms elapsed; large elapsed
latency here does not imply CPU saturation. Its bad fraction34/40=.85 divided by
allowed.05 gives burn17. The finite target permits2 bad events and has−32
remaining after34. Rejected offers stay in that denominator even when they return
quickly. The paced case reduced offered load to125/s and completed about122.27/s
including the finite tail. It is a tradeoff in offered throughput, not proof
that the same capacity now supports250/s.

These are observed samples, not fixed expected timings. Busy hosts, thread
scheduling, filesystem work, clock granularity and the small40-event window can
change counts and percentiles. A repeat should compare distributions across
several independent runs and declare its arrival schedule before observing data.
The controlled event-gated tests establish admission/expiry behavior without
requiring an accidental load race.

## Actual process kills around commit

The experiment starts its own child, which opens its own transaction and signals
a named phase through an explicit hook. The parent kills only that child after
receiving the phase signal; it then reopens the same temporary database and retries
`crash-operation,+7` with the same key. The two observed cases were:

| Last signaled phase | Exit | State before retry | Retry result | State after retry |
| --- | --- | --- | --- | --- |
|before commit|−9|counter0,no operation row|(7,not duplicate)|counter7,one row|
|after commit|−9|counter7,one row|(7,duplicate)|counter7,one row|

This tests application-process crash and local engine recovery. It does not turn
off physical power, stop the kernel, corrupt a WAL, validate a controller flush or
exercise network delivery. The hook establishes which side of a completed commit
was reached; it is not a measurement of the internal SQLite commit instruction.

## Interpretation, alternatives and follow-up

The data support queue pressure from the constructed slower dependency and a
successful reduction in offered load. They do not establish that every production
bottleneck is the same, or isolate database lock time from worker residence.
The failure outcome is not simply 'add threads': SQLite still serializes writers,
more concurrency can increase contention, and the dependency may itself saturate.
Try a declared matrix of workers, spacing and delay; log every attempt. Compare
load shedding, queue capacity and deadline changes while keeping eligible-user
work in the denominator. Then rehearse backup/restore on a separate database,
validate the counter/identity invariant and write an incident record using only
its actual observations. [INCIDENT](INCIDENT.md) is the analysis of this saved run.
