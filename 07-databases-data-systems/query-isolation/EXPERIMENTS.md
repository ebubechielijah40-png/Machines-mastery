# Actual query/snapshot experiment

Questions: do alternative join algorithms preserve bag meaning while changing
work; does adding an index preserve a logical result; and which version does a
WAL reader see while another connection commits? Predictions: one-to-one keys
produce equal bags with n² nested comparisons and linear build/probe counts;
indexed and scanned results agree; a held reader keeps its old snapshot and
cannot upgrade after another writer commits.

Controls: stdlib implementation, fixed synthetic rows, join key distributions,
query text/arguments, local WAL mode, two connections with explicit transaction
statements and timeout0. There are no threads, timers or nondeterministic sleeps;
the program interleaves real connection calls in a declared order. No claim
about all possible schedules follows.

From repository root:

```sh
python3 -m unittest discover -s 07-databases-data-systems/query-isolation -v
python3 07-databases-data-systems/query-isolation/experiment.py
```

[Actual raw results](evidence/results.json), executed2026-10-23, Python3.12.14,
SQLite3.53.1 on recorded Linux environment:

| n per join side | Nested comparisons | Hash build/probes/candidates | Equal output bags |
| ---: | ---: | --- | --- |
|10 |100 |10/10/10 |yes |
|100 |10000 |100/100/100 |yes |
|1000 |1000000 |1000/1000/1000 |yes |

These are instrumented counts, not elapsed-time benchmarks. The index query
returned the same10 ordered rows out of1000 before/after creating an index.
The recorded diagnostic changed from SCAN reading to SEARCH using reading_device;
no speedup is inferred from those labels.

The reader observed(100,100) before/during the transfer and after B's commit;
its stale upgrade raised code517 SQLITE_BUSY_SNAPSHOT. After rollback it observed
(90,110). A second writer reservation failed with code5 SQLITE_BUSY. Separate
statement stale read/replace produced80; atomic relative debits produced70.
These observations support this local protocol and demonstrate the application
transaction-boundary bug; they do not contradict SQLite serializing its writers.

Alternatives/limits: different journaling, shared-cache settings, versions,
timeouts, malformed data or process failures change the question. No physical
crash, fsync/power-loss evidence, distributed isolation or complete engine proof
is supplied. Hash counts omit Python allocation/hashing costs. Follow-ups: vary
key skew while holding n fixed, bound output memory, compare repeated timings,
add restartable transactions, and test interruption/rollback under a separate
explicit fault protocol. Unrun outcomes remain predictions.
