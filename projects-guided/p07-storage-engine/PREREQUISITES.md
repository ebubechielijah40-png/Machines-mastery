# Prerequisites and bridges

No prior database engine is required. The concepts below are introduced here because they affect a concrete recovery decision.

| Dependency | Required knowledge and local bridge |
| --- | --- |
| Mathematics | A byte stores an integer from 0 to 255. Four bytes represent an unsigned integer up to `2^32−1`; big-endian puts the most significant byte first. See the byte-format worked example in [the lesson](LESSON.md). |
| Physics | No circuit calculations are needed. Distinguish process memory, kernel cache, and physical storage: a process exiting is a different fault from electrical power loss. |
| Electronics | No hardware construction is needed. Storage devices may have their own volatile caches; this lab does not validate their behavior. |
| Chemistry/materials | Not a dependency: there is no materials experiment or storage-medium model here. |
| Statistics | No probability theory is needed for prefix correctness. For timing, five warm replay samples describe this machine only; median is the middle sorted sample. |
| Programming | Python strings, lists, dictionaries, exceptions, functions, `with`, binary file reads/writes. Run the [working memory baseline](code/starter_memory.py); explain its two printed dictionaries before starting. |
| Prior systems | A process requests writes through an OS. A completed write and an `fsync` request have different roles; the lesson explains that boundary before using it. |

A key/value mapping associates each string key with at most one string value. `put("a","7")` replaces any old value. `delete("a")` removes a key if present. A transaction is an ordered, nonempty list of these operations. Applying `[put(a,9), put(b,21)]` means both changes belong to one visibility boundary.

Before coding, explain why a fresh `MemoryStore()` is empty, why decimal 300 needs more than one byte, and why updating `a` before validating the `b` operation can expose an invalid partial transaction. If these are unclear, trace the examples in the lesson; no external tutorial is required.
