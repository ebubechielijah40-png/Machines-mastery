# From a volatile map to a recoverable log

This is an original design and derivation. The limited connections to real SQLite and Python behavior are mapped in [SOURCES.md](SOURCES.md). Our bytes, algorithms, and measurements are not SQLite's.

## 1. Why persistence is not just writing a file

Suppose `a=10` and `b=20`. Moving one unit from `a` to `b` should produce `a=9,b=21`. The invariant is `int(a)+int(b)=30`. An application that writes `a=9` and then crashes before writing `b=21` violates it. A successful ordinary test of each individual assignment says nothing about this failure window.

One earlier approach is to overwrite values in place, preserving old bytes in a rollback journal before modifying the main file. Another is to preserve old state and append new changes. These are different recovery organizations; SQLite documents both [DB-S1, DB-S2]. We choose an append-only design because its entire history can be inspected with a sequential reader. We have no separate data-page file or checkpoint, so this is a log-structured teaching store rather than a full page-oriented write-ahead logging system.

A transaction is an ordered batch. Recovery either applies the entire batch or leaves the previous map. This is **atomic visibility in our recovery model**. It is not a claim that storage writes are physically atomic.

## 2. State, transformations, and boundaries

The persistent state is a versioned sequence of encoded transactions. The derived state is a dictionary plus the last committed transaction number. The input is a nonempty batch of `put` and `delete` operations on strings. The output is a positive transaction number returned after a successful write and `fsync` request.

The invariants are:

- The file starts with exactly seven bytes `MMWAL1\n`.
- Valid transaction IDs form `1,2,…,n`, in file order.
- A frame's complete bytes, checksum, operation grammar, and ID are validated before any of its operations change replay state.
- `valid_end` is the first byte after the last fully accepted frame.
- Recovery never skips damaged bytes in search of a plausible later frame.
- The writer's visible map changes only after its entire frame is written and sync returns successfully.

The final invariant needs careful interpretation. If sync raises an exception, the bytes may already exist in the OS cache or on storage. The caller has an **unknown outcome**, not proof of absence. Recovery may find the batch even though the caller received no acknowledgement.

## 3. Derive a readable binary contract

Newline-delimited text is easy to print but introduces ambiguity when values contain newlines unless escaping is defined. Fixed-width records waste space or impose tiny values. A length prefix makes the boundary explicit while allowing variable-length UTF-8 values.

Each transaction frame consists of:

| Relative byte offset | Size | Meaning |
| --- | --- | --- |
| 0 | 4 | ASCII bytes `TXN1` |
| 4 | 8 | Positive unsigned transaction ID, big-endian |
| 12 | 4 | Payload length `L` in bytes, big-endian |
| 16 | `L` | UTF-8 JSON list of operations |
| `16+L` | 4 | Unsigned CRC32 of the header and payload, big-endian |

Thus frame size is `L+20` bytes. `struct.Struct(">4sQI")` implements the 16-byte header: `>` chooses big-endian, `4s` four bytes, `Q` eight unsigned bytes, and `I` four unsigned bytes. Decimal 300 becomes the four bytes `00 00 01 2c`, since `1×256+44=300`. Counting characters would be wrong for UTF-8: `雪` occupies three bytes even though it is one character.

For transaction 1 with `[("put","a","1")]`, compact JSON is `[["put","a","1"]]`, a 17-byte payload. The frame is 37 bytes; including the seven-byte file header, the next frame begins at byte 44. Confirm these lengths yourself with `len(encode_transaction(...))`; never infer encoded length from a terminal's rendered width.

`L≤1,048,576` is a teaching resource limit. Without it, a corrupted length could ask the parser to allocate gigabytes. This bound limits each frame's encoded payload, not total history or every possible parser resource. The writer validates before appending. It does not accept arbitrary object deserialization or execute contents.

CRC32 detects many accidental changes. It does not prove authorship, confidentiality, or resistance to intentional modification. Anyone who can rewrite the file can recompute a checksum and change the data. Transaction numbers catch some reorderings and missing middle frames; they cannot detect replacing the complete file or deleting a complete suffix.

## 4. A complete two-batch trace

Let transaction 1 set `a=10,b=20`. Its compact payload is 35 bytes, so its frame occupies 55 bytes. It starts at offset 7 and ends at offset 62. Transaction 2 sets `a=9,b=21`, with a 34-byte payload and a 54-byte frame. It starts at offset 62 and ends at 116.

1. Read seven header bytes and establish the file version.
2. At offset 7 read 16 header bytes. Check the magic and `L=35` bound.
3. Read the payload and four-byte checksum. Validate the checksum over the header and payload together. A payload-only checksum would miss header changes.
4. Check that ID 1 follows the initial ID 0.
5. Parse and validate **every** operation. Only then set both keys. Set `valid_end=62`.
6. At offset 62 repeat the procedure for transaction 2.
7. If all 54 frame bytes exist and validate, apply both updates and set `valid_end=116`.
8. If only the first 30 bytes of transaction 2 exist, report incomplete trailing bytes and return `a=10,b=20`, `valid_end=62`. Applying the first decoded operation before the whole record validates would violate atomicity.

Check the worked lengths against [the executed experiment](evidence/byte-cut-2026-10-22.json), which uses exactly these two batches. Empty history after the file header is a valid empty map. Deleting a missing key is deliberately a no-op. Two updates to one key inside a batch are applied in order, so the later one wins.

## 5. Recovery algorithm and correctness argument

The reader processes one frame at a time. A short final header, payload, or checksum produces an incomplete-tail report. Wrong magic, excessive length, incorrect checksum, a discontinuous ID, invalid UTF-8/JSON, or a wrong operation shape raises corruption. We deliberately do not call every final checksum error a harmless torn write: the reader cannot distinguish an interrupted write from damage to a previously acknowledged frame.

Proof sketch by induction over accepted frames: after zero frames, replay gives the empty mapping defined by the format. Assume accepted frames `1…k` produce their sequential map. Frame `k+1` is fully validated before applying any operation. If invalid, recovery either reports the incomplete suffix with the earlier map or rejects corruption; it never returns a partially applied batch. If valid, applying the whole ordered operation list produces exactly the map for `1…k+1`. This proves prefix replay semantics under the stated byte-prefix fault model. It says nothing about disk firmware honoring flushes or concurrent writers.

Do not scan ahead after corruption. A later-looking `TXN1` may be text within a payload, or may be a real frame whose preceding transaction is missing. Continuing would manufacture a history whose transaction invariants were never established.

## 6. The append and acknowledgement path

`WalStore.commit` validates the entire operation list, encodes one frame, loops until the unbuffered file object accepts every byte, then calls `os.fsync`. Short writes matter: a write API can report less progress than requested. The helper advances a memory view by the actual returned count and fails if no progress is made.

Only after sync returns does the store update its dictionary and return the ID. A write/sync exception poisons the object. Continuing in the same object would risk reusing a transaction ID after unknown partial or complete output. Close it, inspect recovery, and reconcile the operation with the caller instead.

The file is opened unbuffered, so no Python buffer needs flushing. For buffered files Python's docs require flushing first [DB-S4]. `fsync` is an OS durability request with platform behavior; this exercise does not test controllers, media, filesystems, or the persistence of a newly created directory entry. Reading a file after a process error measures kernel-visible bytes, not survival of a power interruption.

Recovery is read-only. Appending after an incomplete tail is rejected until the operator explicitly chooses `repair_tail=True`. That option truncates to `valid_end` and syncs before appending. Copy and inspect a real log before any repair. CRC-corrupt frames are rejected even with that option. A truncated **complete** suffix is indistinguishable from a legitimately shorter history without an independently retained record of the expected last commit.

## 7. Costs and the next abstraction

With `B` bytes of history, replay requires `O(B)` I/O and validation work. Keeping `K` distinct live keys uses `O(K)` mapping entries plus their text. Lookups use the in-memory dictionary; a new process cannot use that index until replay finishes. A batch of `m` operations costs its encoding bytes, its operations, and one sync request. Sync latency may dominate small batches, but batching also enlarges the amount of work whose acknowledgement can be lost together.

Old values and deletions remain in the log. Repeating updates grows restart cost while the live map stays small. This motivates compaction: create a shorter durable representation, then install it without destroying the last recoverable copy. Simply truncating the old log before a replacement is durable makes recovery worse. A safe compaction design is an advanced extension, not an implemented capability here.

A B-tree would instead organize indexed pages with branching that reduces page probes. An LSM-style engine combines sequential writes with sorted immutable runs and merging. Neither follows automatically from having an append-only file; indexing, page formats, compaction, snapshots, and concurrency need their own implementations and correctness arguments. SQLite's page-oriented WAL has different frames, checkpoints, and reader end marks [DB-S2, DB-S3].

## 8. Investigate and transfer

Run [the experiment](EXPERIMENTS.md) only after predicting which prefixes may change either account. Explain why checking just `a` misses half a transfer, why retrying an unacknowledged transfer can apply it twice, and why a checksum cannot enforce a financial invariant. Then complete [the assessment](EXERCISES.md).

Reconstruct the format and recovery state machine on paper without viewing the source. Implement a reader from that drawing and use the existing byte-cut experiment as an independent oracle. Finally, change the requirement to support two processes writing simultaneously: identify the precise read-ID/append race before proposing a lock or consensus system.
