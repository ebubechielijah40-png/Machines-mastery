# Networks and replicas: bytes, boundaries and ordered state

This entry connects developed local transport/replica units. The wider coursebook
remains PARTIAL: routing, congestion, reliable transport internals, consensus,
Byzantine failures and production network operation are not completed here.

## A byte stream does not preserve an application record

With a four-byte big-endian length header, payload`abc` is encoded as length3
followed by three bytes. A receiver may get the first two header bytes, then the
remaining header and one payload byte, then the rest. A single read is therefore
neither one record nor a complete header. The [framing lesson](../06-networking/stream-boundaries/LESSON.md)
derives an incremental decoder's states, length/resource limits, EOF truncation
and terminal errors, and tests every two-cut partition of representative streams.
Local socketpair experiments distinguish half-close, EOF and backpressure.

The [HTTP subset build](../projects-guided/p06-http-server/README.md) adds a
specific grammar and lifecycle on top of byte handling. Its narrow GET contract
and rejection/deadline tests are explicit. It does not silently claim full HTTP,
TLS or internet-facing deployment support. Close unused descriptors so a parent
reference cannot prevent EOF; the [shell project](../projects-guided/p02-shell/README.md)
provides a concrete related process-lifetime case.

## Complete delivery still needs state semantics

Two nodes can receive red/blue writes in opposite orders and end with different
values. The [ordered-map unit](../15-distributed-systems/ordering-reconciliation/README.md)
adds unique event stamps and a keywise maximum. Max is associative, commutative
and idempotent, so equal valid delivered record sets converge. The receive clock
still advances for each receipt. Tombstones retain deletion evidence; dropping
them lets stale messages resurrect values. The [replica workbench](../projects-guided/p11-distributed-kv/README.md)
executes delayed and duplicate schedules with raw traces.

A clock inequality does not prove causality; a convergent winner does not prove
consensus or linearizability. Permanent partitions violate the eventual-delivery
premise. Restarted counters and unauthenticated origins can violate valid stamps.
Connecting sockets, persistence and replica logic requires a combined protocol
and recovery argument, not just imports.

## Exit work

Reconstruct framing from memory, predict an incomplete final record, execute the
socket observations, then derive the red/blue/tombstone trace before running it.
Freeze the failure model and explain one counterexample to each stronger claim.
Use the [source-inspected Lamport practicum](../projects-guided/p16-research-reproduction/README.md)
for independent causal-graph checks. Physical timing and production throughput
remain separate experiments with their own instruments and controls.
