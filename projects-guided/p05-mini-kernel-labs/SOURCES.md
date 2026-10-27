# Inspected source map

The authoritative shared record is [the OS source map](../../05-operating-systems/SOURCES.md).
It records exact inspected sections, versions/date scopes and an inaccessible
POSIX endpoint. This project reuses the original repository models, rather than
claiming another independently reconstructed implementation.

| Mechanism in this project | Verified primary-resource scope |
| --- | --- |
| Workload/metrics/FCFS/RR context | Arpaci-Dusseau and Arpaci-Dusseau, OSTEP chapter7, version1.10, §§7.1–7.7, inspected 2026-10-22 |
| Page/VPN/PFN/hierarchy/TLB context | Linux kernel Page Tables documentation, introductory mapping and “MMU, TLB, and Page Faults,” inspected 2026-10-22 |
| Host descriptors/pipe/process interfaces | Linux man-pages dup(2), pipe(7), execve(2), stated DESCRIPTION scopes, and Python3.12 subprocess/os entries, inspected 2026-10-22 |

The tiny address geometry, tie ordering, cost rule, JSON bounds, code, proofs,
exercises and examples are original project choices. Raw records distinguish
actual driver execution of deterministic models from real host OS observations.
No kernel source was inspected or booted by this project, and no full OS book
or POSIX specification reconstruction is claimed. Upstream copyrights and
licenses remain with the linked original resources; no substantial text is copied.
