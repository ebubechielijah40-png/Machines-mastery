# Inspected primary scopes and original work

Accessed2026-10-25. These are selected documentation scopes, not full book or
paper reconstructions. No original page text, diagrams or large excerpts are
redistributed. The format, Python mechanisms, proofs, workloads, failure cases
and assessments are original repository teaching work.

| Primary resource and authorship | Exact inspected scope/version | Supported boundary |
| --- | --- | --- |
| Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), HTML rendering by Michael Kerrisk | DESCRIPTION, ERRORS and COLOPHON; man-pages6.19, page date2026-02-08, rendered2026-09-09 | File synchronization versus directory-entry synchronization; error/storage assumptions. This is not proof of this host's physical power-loss behavior |
| Linux man-pages project, [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) | DESCRIPTION atomic replacement/open descriptors; EXDEV and NFS BUGS; same6.19/page date2026-02-08 | Same-filesystem name replacement and its documented limits; not a standalone multi-file durability protocol |
| Linux man-pages project, [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | DESCRIPTION open-file-description locks/close, LOCK_SH/EX/NB; NOTES advisory nature and upgrade/nonlocal caveats; same6.19/page date2026-02-08 | Cooperating local lock protocol. No general NFS/SMB, reentrancy or adversarial-file-access assurance |
| PostgreSQL Global Development Group, [Row Estimation Examples](https://www.postgresql.org/docs/18/row-estimation-examples.html), documentation18 §69.1 | Current URL resolved as18 during inspection: cardinality statistics, histogram/MCV assumptions, independence and equality-join examples | Why estimates depend on statistics/assumptions. Our cost units, uniform finite estimator and Python executor are original simplifications, not PostgreSQL implementation or reported benchmarks |

The Linux pages identify themselves as kernel/C-library interface documentation;
their own source notices govern reuse. The PostgreSQL page identifies copyright
1996–2026 PostgreSQL Global Development Group. Rights for wholesale source-page
redistribution were not separately established; only links and original
explanations are included. Live documentation can change. Actual execution uses
the Python/kernel/environment recorded in the raw experiment, not a claim that
the documentation version is the runtime version.

Dependencies preserved from earlier work: the original p07 WAL and page-index
codec are imported directly. Their inspected references and format ownership
remain in [WAL sources](../../projects-guided/p07-storage-engine/SOURCES.md) and
[index sources](../page-index/SOURCES.md). Those prior source claims are not
silently expanded to cover this new publication protocol.

No inaccessible database book, distributed-streaming paper, physical fault study,
external benchmark or hosted production experiment is claimed inspected or
reproduced here. The stream proof is a conditional original argument about one
immutable synthetic partition and one local transaction, with its premise
deliberately falsified in an actual counterexample.
