# Build a recoverable transactional log

A dictionary loses its contents when its process ends. Saving it after each edit still leaves a harder question: what does a reader observe when a write stops halfway through a batch? This project builds a small storage engine that makes transaction boundaries and recovery decisions inspectable.

**Prepared status: STRONG bounded teaching build.** This is an original append-only key/value log with complete-batch recovery, not a complete relational database or SQLite implementation. The broader databases domain remains PARTIAL. Learner mastery remains NOT STARTED.

## Start and tools

Use Python 3.10+ with its standard library. No server, package installation, private data, or external service is required. Run from the repository root:

```sh
python3 projects-guided/p07-storage-engine/code/starter_memory.py
python3 -m unittest discover -s projects-guided/p07-storage-engine/code -v
python3 projects-guided/p07-storage-engine/code/experiment.py
```

The first command demonstrates a working volatile store losing data on reconstruction. The second runs ten tests. The third executes byte-prefix fault injection and bounded replay measurements in temporary files. Use `--output /your/chosen/path.json` to retain a fresh experiment; do not overwrite the dated evidence to pretend it came from another machine.

Read [prerequisites](PREREQUISITES.md), attempt the design checkpoints in [the build sequence](CHECKPOINTS.md), then study [the mechanism and derivation](LESSON.md). Try [exercises](EXERCISES.md) before [hints](HINTS.md) or [solutions](solutions/EXERCISES.md). [Reference implementation](code/wal_store.py) is a comparison target, not the learner's first step.

## What the learner builds

1. A versioned binary format with explicit lengths and a corruption checksum.
2. A transactional batch encoder and a bounded streaming decoder.
3. Prefix recovery with a deliberate incomplete-tail policy.
4. A single-writer API whose acknowledgement follows a sync request.
5. Tests distinguishing missing acknowledgement, incomplete data, and corruption.
6. An experiment explaining why one-key tests cannot demonstrate batch atomicity.

The system has one file and one derived in-memory index. The file is authoritative; replay reconstructs the index. A complete frame represents a commit. The append path is `validate → encode → write all bytes → fsync → update memory → return`. The recovery path is `file header → bounded frame → checksum → sequence → operation validation → apply whole batch`.

Do not use real payment or scientific records. Read [limits](LIMITS.md), [production considerations](PRODUCTION.md), [test scope](TESTS.md), [experiment protocol and actual results](EXPERIMENTS.md), and [verified source map](SOURCES.md) before making reliability claims.

## Secondary-index milestone

After the existing WAL recovery build, implement [the byte-page B+ index](../../07-databases-data-systems/page-index/README.md) and rebuild it read-only from complete log transactions. Explain why valid page checksums can still admit a mixed transaction state. Durable checkpoint publication, locking and compaction remain additional designs.
