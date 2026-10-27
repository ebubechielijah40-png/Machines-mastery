# Model and implementation limits

The fault experiment truncates bytes at a chosen boundary. It does not cut electrical power, emulate a device cache, reorder completed writes, test a filesystem driver, or validate the storage medium. A process-level observation of a complete file is not proof of persistence after host failure.

The engine assumes exclusive caller ownership of both the object and pathname. It provides no process lock, thread lock, snapshot isolation or concurrent-reader protocol. Two writers can reuse IDs, interleave bytes, or truncate one another during repair. Reads of one object's map do not detect outside modification.

File contents are synced before successful acknowledgement. Creation does not sync the parent directory; durability of a newly created pathname is not promised. Existing empty/partial file headers are rejected, including a possible interrupted initial creation. Failed sync has unknown commit outcome; there is no persisted client request ID or deduplication policy.

Only an incomplete final frame can be explicitly truncated. Checksum mismatch or structural corruption fails closed. The implementation cannot detect deletion of a complete suffix, deliberate recomputation of checksums, or replacement by another internally valid log. CRC32 is not a cryptographic authentication mechanism. There is no encryption or access-control system.

The one-MiB payload limit bounds normal per-frame reads, but not total replay time/history, Python JSON parser nesting or writer input enumeration. Inputs and log pathname are locally controlled; a hostile endpoint would need quotas, parser resource controls, authenticated requests and hardened path handling. History and the live-key index can grow until resources are exhausted.

There are no pages, on-disk search index, B-tree, LSM runs, compaction, SQL planner, relational constraints, multi-file transactions, backups, media-corruption repair, schema migration or format upgrade implementation. Deletion retains old plaintext in history. This unit teaches persistence boundaries and transaction-prefix recovery; those missing subjects remain in the broader remediation backlog.
