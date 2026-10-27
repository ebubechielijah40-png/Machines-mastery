# Databases Data Systems

Curriculum phase: P07 — Databases and Data Systems. Learning state: NOT STARTED.



## Scope

data models; relational modeling; SQL; indexes; transactions; concurrency; query execution; storage engines; B-trees; warehouses; lakes; pipelines; lineage; metadata; quality.

## Entry and exit

Use the unit-level gates in [PREREQUISITE_GRAPH.md](../PREREQUISITE_GRAPH.md). Target evidence: Build persistence and recovery with explicit transactional boundaries.

## Work placement

Keep subject notes here. Link implementations from [PROJECT_REGISTRY.md](../PROJECT_REGISTRY.md), measurements from [EXPERIMENT_REGISTRY.md](../EXPERIMENT_REGISTRY.md), and verified references from [RESOURCE_REGISTRY.md](../RESOURCE_REGISTRY.md). Do not duplicate book reconstructions here.

## Implemented entry unit

[Build a recoverable transactional log](../projects-guided/p07-storage-engine/README.md) now supplies an original byte-level lesson, runnable engine, all-prefix fault tests, separate assessments and executed evidence. See the [phase guide](SELF_CONTAINED_GUIDE.md) for the honest PARTIAL domain status and remaining scope.

## Developed byte-page index

After transactional WAL and query/isolation, build [serialized B+ pages, splits, ranges and authoritative-log rebuild](page-index/README.md). Distinguish page validity from transaction atomicity using the accepted mixed-snapshot counterexample.

## Publish, coordinate, plan and replay

Continue with [manifest-selected checkpoints, locks, optimistic versions,
compaction, costed bag joins and transactional stream progress](recovery-planning/README.md).
It adds actual process-kill/cut/overlap experiments while preserving the earlier
codecs and query semantics. The source-immutability and local-filesystem premises
are explicit. Full original-mandate completion and the fixed STRONG gate remain
separate in [the dashboard](../STRONG_PROGRESS_DASHBOARD.md).
