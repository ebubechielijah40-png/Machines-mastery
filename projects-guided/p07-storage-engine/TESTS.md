# Executed validation and its scope

Run from repository root:

```sh
python3 -m unittest discover -s projects-guided/p07-storage-engine/code -v
```

The suite contains ten test methods, including exhaustive subcases and a deterministic randomized model. It covers empty/reopened stores, replacement/deletion/Unicode, returned-snapshot isolation, every proper byte cut of a two-key transaction, explicit incomplete-tail repair, corruption followed by valid data, malformed payloads with valid checksums, sequence/version/magic/size checks, input-validation nonmutation, unknown outcome after sync failure, short writes, no-progress writes, and comparison with an independently maintained dictionary across 100 random batches.

[Raw validation evidence](evidence/tests-2026-10-22.txt) records the command, environment and actual output. [Experiment evidence](evidence/byte-cut-2026-10-22.json) records 55 cut cases and replay samples. Tests passing demonstrates the bounded byte-prefix and API contracts on this interpreter. It does not demonstrate arbitrary bit-rot recovery, process-safe concurrency, physical power-loss survival, constant-time behavior or production readiness.

Failure outputs are actionable: a checksum failure identifies a byte offset and stops replay; an incomplete tail reports the safe prefix boundary and refuses writing until explicit repair; a failed commit poisons its writer so the caller must reopen and reconcile unknown outcome.
