# From byte intervals to allocator engineering

A general allocator must obtain correctly typed/usable storage under its
language and platform contract, serve alignment requirements, handle arithmetic
overflow, support simultaneous callers, and return errors predictably. This
project deliberately separates those unsolved obligations from interval layout.
Replacing malloc with this arena would violate the advertised general contract.

First-fit scans and array compaction cost O(B). At larger B, bins, trees or
segregated sizes can change the search/update balance. A policy must be measured
against realistic request sizes and lifetimes; one fragmentation snapshot cannot
rank every workload. Track requested/reserved/live bytes, failures, largest holes,
scan lengths, tail latency, and metadata overhead as separate quantities.

Concurrency introduces shared metadata races and cross-thread lifetime errors.
A single lock may simplify invariant reasoning but add contention. Per-thread
arenas reduce sharing yet can strand free memory and complicate cross-thread
release. Neither is implemented here. Recovery from detected metadata corruption
requires a defined fail-stop or isolation policy; blindly trusting corrupted
sizes can turn one client error into arbitrary memory access.

For sensitive data, releasing a lease is not secure erasure. Define what must
be cleared, how compilers and copies affect that operation, and which backups
or swap copies remain. Instrumentation should avoid exposing payload contents.
Use this reference as an inspectable learning mechanism, not a deployed allocator.
