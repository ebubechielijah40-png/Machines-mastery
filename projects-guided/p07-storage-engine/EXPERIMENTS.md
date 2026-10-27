# Transactions under incomplete append and unknown acknowledgement

## Question and hypothesis

Question: can recovery expose half of a two-key transfer if the final append stops after any byte? Hypothesis: every proper prefix of the second frame preserves the first transaction's map; only the complete checksum-valid frame exposes both updates. A separate hypothesis predicts that a sync error does not prove the batch is absent from subsequent recovery.

## Controlled model and procedure

The first transaction sets `a=10,b=20`. The second sets `a=9,b=21`. Independent variable: retained bytes of the 54-byte second frame, from 0 through 54. Dependent measurements: recovered map, accepted transaction count, valid boundary and tail classification. Controls: same encoder, first transaction, reader, keys and values; each case uses a fresh explicit byte fixture in a temporary directory.

Instrumentation is the reference byte encoder and read-only recovery function, with assertions against independently stated expected mappings. The fault model deliberately constructs byte prefixes; it is not a physical power cut or filesystem crash emulator.

Run from repository root:

```sh
python3 projects-guided/p07-storage-engine/code/experiment.py
```

The script also flips one payload bit in a complete frame, injects an `fsync` exception after writing another batch, and measures five warm replay times at each of 100, 1,000 and 10,000 transactions. The replay fixtures retain 100 keys. Timing includes file open/read/checksum/JSON/operation work; fixture writing and syncing are outside that timer. It uses `perf_counter_ns`, with nanoseconds as the stored unit.

## Actual agent-executed observations — 2026-10-22

[Raw JSON, environment and every cut case](evidence/byte-cut-2026-10-22.json) are retained. Fifty-four proper prefixes all preserved `a="10",b="20"`; the full frame exposed `a="9",b="21"`. A flipped payload bit produced a checksum-corruption error at byte 62. After the injected sync error, the live map was empty while recovery saw `{"uncertain":"present"}`. This observes kernel-visible bytes after an injected exception, not durability after real power loss.

| Transactions | File bytes | Retained keys | Median of five warm replay samples, ns |
| --- | --- | --- | --- |
| 100 | 3,889 | 100 | 286,749 |
| 1,000 | 39,800 | 100 | 2,697,521 |
| 10,000 | 407,901 | 100 | 27,548,963 |

The samples show approximately proportional replay cost in this small run while the live map stays fixed. That is consistent with scanning accumulated history; it is not an exact complexity proof or a forecast for another system. The raw file contains all five timings per row, not just these medians.

## Interpretation, alternatives and limitations

Atomic replay follows from validating the complete frame before application; no physical atomic write is assumed. Unknown acknowledgement is a separate failure boundary: the caller cannot infer absence from an exception. CRC failure demonstrates detection of this one mutation, not correction or authenticity.

Warm caches, Python parsing/allocation, CPU scheduling and short timer intervals can affect timing. No cold-cache control, device power experiment, concurrent writer, filesystem reorder model, disk-full experiment, compaction or deployment is included. Every observation here is agent-executed setup evidence, not learner mastery or independent validation of SQLite.

## Follow-up investigations

Predict and test a complete-suffix deletion: recovery will accept a shorter history without external expected-last-ID evidence. Next design persisted request IDs to resolve retries, or an exclusive process lock to enforce ownership. For compaction, enumerate all interruption points before implementation. Record any new experiment separately with predictions and environment rather than editing the old observations.
