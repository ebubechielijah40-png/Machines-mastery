# From sorted keys to byte pages

A recovered log can reconstruct a dictionary, yet each restart still replays its
history and a range query still needs an ordering mechanism. This unit builds an
original B+ index whose nodes are actual fixed-size encoded byte pages. A search
must choose page identifiers, decode their bytes and preserve separator rules;
there is no library B-tree underneath it.

**Scope: developed bounded index, broader database domain PARTIAL.** It implements
unique signed64-bit keys, byte values of at most24 bytes, insertion/replacement,
leaf/internal splits, ordered ranges, bottom-up bulk loading and strict snapshot
validation. A read-only bridge rebuilds it from the existing project's complete
WAL transactions. It does not implement deletion, concurrent writers, in-place
file updates, atomic snapshot publication or log compaction. A valid tree is not
proof that a multi-key transaction committed.

## Start with the prerequisite, then attempt the build

Use [algebra/functions](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md),
[finite words](../../foundations/mathematics/finite-representations/README.md),
[proofs/invariants](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md) and
[Python entry](../../02-programming/python-entry/README.md). Be able to order a
list, divide an integer capacity, trace a loop and distinguish a value from its
byte representation. The [WAL project](../../projects-guided/p07-storage-engine/README.md)
is required for the final rebuild milestone, not for the first page/search work.
SQL is not required to understand this mechanism.

1. Study the [complete mechanism and worked traces](LESSON.md).
2. Attempt the [guided milestones and exercises](EXERCISES.md).
3. Use [hints](HINTS.md) after recording your attempt; then compare with
   [independently checkable solutions](SOLUTIONS.md).
4. Reconstruct `get`, one split and the byte-page decoder before opening all of
   [the reference implementation](bplus.py).
5. Run the [controlled experiments](EXPERIMENTS.md), explain a failed claim and
   produce the [build/review evidence](TESTS_AND_LIMITS.md).

## Run

Python3.10+ standard library suffices. Run from the repository root:

```sh
python3 -m unittest discover -s 07-databases-data-systems/page-index -v
python3 07-databases-data-systems/page-index/experiment.py
python3 07-databases-data-systems/page-index/experiment_rebuild.py
```

The reference tests use exact byte vectors, every permutation of six insertions,
seeded dictionary comparisons, every small bulk-load tail, all snapshot cuts,
single-bit mutations and checksum-valid graph corruptions. They also test a
valid-but-mixed snapshot and all byte cuts of a transactional source log.
[Actual run evidence](evidence/validation.json) records commands and output; it
never establishes a learner's mastery or the behavior of another host.

To rebuild an index from a compatible project log:

```sh
python3 07-databases-data-systems/page-index/rebuild.py --wal /path/to/teaching.wal
```

This command is read-only. Its accepted subset uses canonical decimal signed64
string keys and UTF-8 string values fitting24 bytes. It rejects incompatible
records instead of silently truncating/coercing them. It replays the full log,
so it is not a checkpoint/replay-skipping optimization. No external dataset,
network service, account or installation is required.

[Source scopes](SOURCES.md) distinguish inspected primary documentation/course
material from this original format, algorithms, derivations and observations.
The existing [relational/isolation unit](../query-isolation/README.md) explains
what queries mean; this index explains an access path. One does not replace the
other.
