# Engineering a stronger service

A network extension needs framed serialized records, peer authentication,
validation before clock mutation, bounded queues, timeouts and a protocol for
missing/duplicate/reordered messages. A durable extension needs counter/incarnation
metadata and state committed with an explicit acknowledgement and recovery
contract. The [WAL project](../p07-storage-engine/README.md) and
[framing unit](../../06-networking/stream-boundaries/LESSON.md) teach components,
but a combined service still requires integration and fault tests.

Convergence preserves the selected map rule, not arbitrary application invariants.
A debit, unique reservation or cross-key update may require coordination or a
different operation model. Measure bytes exchanged, state/tombstone growth,
reconciliation lag, rejected messages and restart outcomes under a declared
workload. This execution window measured none of those production metrics.
Do not deploy the workbench as a trusted remote write endpoint.
