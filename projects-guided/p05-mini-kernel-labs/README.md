# Build an inspectable OS mechanism workbench

A kernel must decide who executes and what memory an executing program may
access. This project builds deterministic models of those two decisions, then
compares their boundaries with actual host process observations. It does not
boot, emulate an instruction set, or modify your host kernel. The larger
mini-kernel project remains PARTIAL; this executable model sequence is a
bounded, testable foundation for a later xv6 or hardware-backed build.

Start with [prerequisite bridges](PREREQUISITES.md) and attempt each
[checkpoint](CHECKPOINTS.md). The [OS guide](../../05-operating-systems/SELF_CONTAINED_GUIDE.md)
contains the full mechanism derivations; this project teaches how to turn those
rules into an inspectable input → transition → evidence interface. Keep
[hints](HINTS.md) and [solutions](SOLUTIONS.md) separate from your first attempt.

## 1. State the machine before implementing a policy

Our scheduling machine has one CPU and integer ticks. A job has a unique name,
arrival tick, and positive service requirement. It has no I/O or additional
bursts. Its remaining work decreases only while it owns the CPU. Arrivals wait
in a ready queue; input order resolves equal-arrival ties. A timeline interval
is half-open `[start,end)`, so consecutive intervals share a boundary without
sharing a tick.

FCFS runs a chosen job to completion. Round robin runs at most q ticks, then
returns an unfinished job to the back. At a slice's end, newly arrived jobs are
enqueued **before** that unfinished job. This rule matters: the workload alone
does not specify a unique trace until boundary ordering is fixed.

An explicit switch-cost interval can occur between different jobs. The model
charges neither an initial dispatch nor a same-job continuation, and resets
that predecessor state after idle. These are declared modeling choices, not
claims that every real kernel has zero cost for those events.

## 2. Derive a complete scheduler trace

Take A = (arrival 0, service 5), B = (1,2), C = (2,1), q = 2 and switch cost 0.
At time 0 only A is ready; it runs to 2 and has three ticks left. B and C have
arrived, so the queue becomes B,C,A. B finishes at 4; C finishes at 5; A runs
5–7 and then 7–8. The final adjacent A slices remain separate in the trace to
show quantum boundaries even though no different-job switch occurs.

| Job | First execution | Finish | Response | Turnaround | Waiting |
| --- | --- | --- | --- | --- | --- |
| A | 0 | 8 | 0 | 8 | 3 |
| B | 2 | 4 | 1 | 3 | 1 |
| C | 4 | 5 | 2 | 3 | 2 |

Response = first execution − arrival. Turnaround = finish − arrival. With no
I/O in this model, turnaround consists only of useful service plus all time
not executing, so waiting = turnaround − service. Mean turnaround is 14/3;
mean response is 1. The service sum is 8, equal to elapsed time because this
run has no idle or switch intervals. Adding a switch cost changes waiting and
elapsed time without changing useful work. Never label those extra ticks
additional service.

Use conservation as an independent check: each job must accumulate exactly its
requested service; intervals partition the entire observed time from zero;
and finish cannot precede arrival plus service. A scheduler that generates the
expected final time but duplicates one job and omits another is still wrong.

## 3. Translate addresses instead of treating them as universal numbers

The memory machine uses 8-bit virtual addresses, 16-byte pages, and 32 physical
frames. Virtual address v is decomposed by integer division:

\[
VPN=\lfloor v/16\rfloor,\quad offset=v\bmod16,
\quad PA=16\cdot PFN(VPN)+offset.
\]

There are 16 virtual pages and four offset bits. A two-level page table divides
the four VPN bits into two directory bits and two leaf bits. VPN 2 therefore
uses directory 0, leaf 2. For v = 45 = 0x2d, VPN = 2 and offset = 13. Mapping
VPN 2 to PFN 7 yields PA = 7×16 + 13 = 125 = 0x7d. Physical addresses require
nine bits here because the physical frame space exceeds one virtual address
space. That is allowed by the model.

The directory stores only allocated leaf tables. This illustrates sparse
mapping rather than memory savings in Python object bytes: dictionary overhead
would overwhelm an 8-bit toy. Do not compare host dictionary size to real page-
table memory and infer a hardware result.

Every mapping contains permissions and a user-access flag. An absent mapping
raises NOT_PRESENT; a mapped but disallowed access raises PROTECTION. A TLB miss
is neither of those by itself: it requests a table walk. A repeated permitted
read can hit the TLB. A repeated disallowed write must still fail even when its
page is cached. “Cached address” does not imply “authorized access.”

The TLB uses fully associative least-recently-used eviction. Capacity zero
forces table walks. `map` and `unmap` invalidate the affected VPN so cached
translations cannot survive the project's supported mapping changes. An actual
multicore OS needs additional coherence and invalidation mechanisms; separate
Python AddressSpace objects are a simpler isolation model.

## 4. Build a bounded, reproducible command interface

[The JSON driver](code/kernel_workbench.py) calls the original
[OS models](../../05-operating-systems/code/models.py). It does not duplicate
those mechanisms. It accepts mode `schedule` or `translate`, reads at most
1 MiB, validates resource bounds, and emits an input SHA-256 with results.
The hash identifies the exact input bytes, including whitespace, rather than
claiming that the model or result is correct.

From the repository root, with Python 3.12+:

```bash
python projects-guided/p05-mini-kernel-labs/code/kernel_workbench.py schedule <<'JSON'
{"jobs":[["A",0,5],["B",1,2],["C",2,1]],"quantum":2}
JSON
python projects-guided/p05-mini-kernel-labs/code/kernel_workbench.py translate <<'JSON'
{"mappings":[[2,7,"r"]],"accesses":[[45],[45],[45,"w"],[64]]}
JSON
python -m unittest discover -s projects-guided/p05-mini-kernel-labs/code -p 'test_*.py' -v
python -m unittest discover -s 05-operating-systems/code -p 'test_*.py' -v
```

The translation run predicts: PA 125 miss, PA 125 hit, PROTECTION, NOT_PRESENT.
The committed [raw run record](evidence/observed.json) contains actual driver
stdout for those deterministic models. It is an independently executed model
result, not a measurement of your host's MMU. The underlying model tests cover
remapping, eviction, dirty/accessed flags and every virtual address, while the
workbench tests cover process/JSON boundaries and resource rejection.

## 5. Tie the model to a real boundary without confusing them

Run [the host experiment](../../05-operating-systems/code/experiment.py). Its
file, pipe and child-process observations are actual local OS behavior. The
same JSON record labels the scheduling and address outputs as model results.
This distinction is essential: a correct toy translation cannot establish that
an actual page fault, context switch, or privilege change occurred on the host.

The model is useful because it exposes all its state and lets you construct
counterexamples. A real system adds interrupt entry, registers, ABI, privilege
levels, device I/O, page-table formats, concurrent CPUs and crash recovery.
The next physical-kernel milestone must select an architecture and inspected
kernel source/version, boot it in a controlled emulator, capture console traces,
and connect those traces to the model. That work is explicitly still missing.

Submit a transition specification, hand traces, JSON cases, independent tests,
raw experiments and a reconstruction. The [rubric](CHECKPOINTS.md) rewards
explaining failure and transfer, not adding unsupported completion claims.
