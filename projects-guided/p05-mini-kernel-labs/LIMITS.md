# Scope and unsupported conclusions

The models do not execute instructions or enforce actual process isolation.
They include one CPU, fixed known service bursts, integer ticks, no I/O,
declared FCFS/RR ordering, and an explicit simplified switch-cost rule. They
exclude priorities, interrupts, preemption latency, multiprocessors, starvation
from unbounded arrivals and real kernel scheduling measurements.

The translator uses 8-bit VAs, 16-byte pages, sparse 2+2-bit tables, 32 frames,
per-object LRU caches, permissions and accessed/dirty flags. It stores no payload
memory, performs no hardware privilege transition, and models no swapping,
copy-on-write, shared-cache ASIDs, multicore shootdowns or physical MMU timing.
Mutate mappings through map/unmap; direct mutation of public Python internals
is outside the supported invalidation contract.

The CLI caps raw input at 1 MiB, 32 jobs, arrival/service fields and total service
at 10,000 ticks, 16 mapping records and 100 accesses. These protect the bounded
lab from accidental giant traces, not a hostile public service. It has no network
listener and needs no elevated privileges.

No xv6/emulator/kernel boot has been executed by this unit. Synchronization,
filesystems, device drivers and crash recovery still need separate substantive
builds. The broad mini-kernel project and operating-systems domain remain PARTIAL.
