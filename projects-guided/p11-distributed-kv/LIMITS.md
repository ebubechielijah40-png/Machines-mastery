# Exact boundary

This is a fresh, deterministic in-memory scenario per invocation. It assumes
unique origins, no counter reuse, valid stamp histories and relevant eventual
delivery. It models neither real network queues nor a persistent failure domain.
No consensus, causal broadcast, linearizability, quorum commitment, automatic
membership, exactly-once operation or physical last-write time is implemented.
Snapshots discard losing history; local conflict detection is therefore incomplete
against forged/reused old stamps. Tombstones have no safe collection protocol.
Input/event caps do not make this a general hostile-code or resource-isolation service.
