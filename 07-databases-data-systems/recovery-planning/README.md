# Publish a database state, then plan and replay its work

A valid B+ image is not an atomic database checkpoint. A lock is not protection
from a client that ignores it. A retried stream batch is not safe unless its
offset and effects share the same commit. This original build connects those
boundaries with a small, inspectable mechanism.

Study the [WAL](../../projects-guided/p07-storage-engine/README.md),
[query/isolation](../query-isolation/README.md), then
[byte-page index](../page-index/README.md) before this unit. Know Python tuples,
iteration, dictionaries, exceptions, integer arithmetic, byte encodings and a
transaction's all-or-none invariant. The
[programming entry](../../02-programming/python-entry/README.md) and
[proof bridge](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md) teach
those prerequisites. Explain why deleting a base key requires retaining a
tombstone in suffix replay before attempting the first milestone.

The scope is a finite local POSIX teaching database: immutable B+ checkpoints,
authoritative suffix WAL, canonical manifest publication, shared/exclusive
cooperating-process locks, optimistic version checks, explicit incomplete-tail
repair and collection of unselected generations. A separate finite planner
compares duplicate-preserving joins. A stream investigation atomically stores
one immutable partition's grouped effects and consumed offset. No external
database engine implements the checkpoint or join beneath these mechanisms.

Start with the [derivations and worked failure cases](LESSON.md), then attempt
[the exercises](EXERCISES.md) before using [hints](HINTS.md) or
[explained solutions](SOLUTIONS.md). The reference mechanisms are
[store.py](store.py), [planner.py](planner.py) and [stream.py](stream.py).

Python3.10+ standard library and a local POSIX filesystem with `fcntl.flock`
and directory synchronization are required. Windows does not silently count
as passing this native contract. No account, dataset, internet service or
third-party Python package is needed to run the lab.

```sh
python3 -m unittest discover -s 07-databases-data-systems/recovery-planning -v
python3 07-databases-data-systems/recovery-planning/experiment.py
```

[Experiment protocols and actual observations](EXPERIMENTS.md),
[source scopes](SOURCES.md) and [author review](REVIEW.md) preserve execution,
attribution and limitations. The integrating reader must perform a separate
qualitative review before changing a domain gate. The code is not a production
storage service, distributed transaction system, physical durability result or
learner mastery certificate. Full SQL optimization, external-memory execution,
multi-partition event time, deployment and comprehensive database breadth remain
larger original-mandate work.
