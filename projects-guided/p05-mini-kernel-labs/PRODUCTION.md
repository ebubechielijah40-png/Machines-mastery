# Engineering implications

A deterministic model makes decisions reproducible but omits asynchronous
interrupts and hardware timing. Before comparing with a real kernel, pin kernel,
architecture and emulator versions, define the observable event, and ensure the
instrumentation itself does not dominate it. A time measured around a Python
function is not a hardware context-switch latency.

Useful production-style evidence includes workload identity, policy/config,
queue length, per-job service/waiting, switch/idle accounting and rejected input
counts. Report metric units and aggregation windows. A mean can hide an individual
job's long wait; preserve per-job records or distribution information.

A production virtual-memory implementation treats cached translation as cached
authority. Mapping changes, concurrent CPUs, permissions and frame reuse require
an ordering/coherence protocol. The model's immediate per-object invalidation
illustrates only one state obligation. It supplies no proof for those concurrent
protocols. Likewise, an input hash supplies provenance, not authenticity or
access control.

For a later kernel build, use an isolated emulator, versioned source checkout,
reproducible image, serial logs, bounded failure injection, and known recovery
procedure. Tie an assertion to a specific register or table entry instead of
claiming the whole OS works because a boot banner appears. These are future
deliverables, not evidence already produced here.
