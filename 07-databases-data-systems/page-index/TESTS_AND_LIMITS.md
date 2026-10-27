# Executable acceptance and limits

Run from the repository root:

```sh
python3 -m unittest discover -s 07-databases-data-systems/page-index -v
```

The suite checks byte-level representation, capacities, sorted route equality,
all permutations of six insertions, dictionary/range alternatives, bulk-load
boundary tails, resource-failure nonpublication, snapshot truncations/bit changes,
checksum-valid semantic graph corruption and mixed-state acceptance. The rebuild
suite checks all cuts of a short multi-transaction WAL, stale-cache discard,
canonical integer/UTF-8 conversion and complete-frame corruption rejection.
Actual command/status/output is in evidence/validation.json and root verification.
Do not interpret zero discovered tests or a parse-only check as execution.

The implementation is single-threaded and materializes byte pages in memory.
Snapshot round trips use files only as test transport. No deletion/merge,
concurrent cursor, in-place disk updates, fsync, compaction or atomic checkpoint
publication is implemented. CRC32 is not a MAC. The public decoder bounds an
already-materialized byte image; an external reader must enforce byte limits
before allocation. Tests are finite evidence for these declared contracts.
