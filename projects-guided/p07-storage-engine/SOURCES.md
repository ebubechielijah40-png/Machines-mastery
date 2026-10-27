# Source verification and original-work boundary

Verified on 2026-10-22 by inspecting the following primary documentation bodies through the available web reader. Web pages are mutable; no upstream release hash or archived snapshot was obtained. These records establish the inspected claim scope, not reproduction of SQLite internals.

| ID | Author/maintainer and original source | Inspected locator | Supported claim scope |
| --- | --- | --- | --- |
| DB-S1 | SQLite project, [Atomic Commit In SQLite](https://www.sqlite.org/atomiccommit.html) | Introduction; §2 Hardware Assumptions; §3.5 Creating A Rollback Journal File; §3.6 Changing Database Pages In User Space | Rollback journaling saves prior contents before modifying database pages; hardware/OS assumptions matter to atomicity and persistence. This page addresses rollback mode. |
| DB-S2 | SQLite project, [Write-Ahead Logging](https://www.sqlite.org/wal.html) | §2 How WAL Works; §2.1 Checkpointing; §2.2 Concurrency; §2.3 Performance Considerations | SQLite WAL appends revised data and records commits; checkpointing transfers changes; reader end marks and a single writer are distinct mechanisms. Sync settings affect durability. |
| DB-S3 | SQLite project, [Database File Format](https://www.sqlite.org/fileformat2.html) | §1.2 Pages; §4.1 WAL File Format; §4.3 Checkpoint Algorithm | SQLite uses bounded pages, WAL headers/frames and its own checksums; checkpoint ordering includes synchronization. The educational format is deliberately different. |
| DB-S4 | Python Software Foundation, [os module documentation](https://docs.python.org/3/library/os.html#os.fsync) | `os.fsync` entry; web response identified Python 3.15.1 documentation | `os.fsync` maps to platform sync functions; buffered Python files require flush before sync. The lab uses unbuffered files and records its actual interpreter version. |

The custom frame layout, prefix proof, Python encoder/recovery implementation, exercises, diagrams-in-prose, byte-cut protocol and measured outputs are original work for Machines Mastery. No upstream implementation is copied. This unit is not a chapter reconstruction, SQLite file-format replica, or independent reproduction of SQLite's durability guarantees.

Reuse rights for the entire upstream documentation were not audited. Only links, source identity and short original factual summaries are retained; full upstream pages are not redistributed. No blanket license is assigned to third-party text. Technical scope is inspected, while legal terms outside that scope remain unverified.

The [machine-readable record](source_verification.json) preserves URLs, verification date, exact sections and limitations. New claims about an upstream version must be rechecked against that version rather than inferred from this retrieval.
