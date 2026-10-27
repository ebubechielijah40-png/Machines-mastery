# Build milestones and reconstruction rubric

| Gate | Concrete learner task | Observable evidence |
| --- | --- | --- |
| A0 | Write the workload and address-space contracts | Explicit tie order, switch rule, widths, permissions and fault kinds |
| A1 | Derive FCFS and RR by hand | Full interval traces and per-job metrics for the worked workload |
| A2 | Implement the scheduler in a separate learner module | Independent service/time conservation tests and edge cases |
| A3 | Implement quotient/remainder translation first as a flat map | All 256 addresses checked against a direct mathematical oracle |
| A4 | Add sparse two-level tables, permissions and per-space LRU TLB | Fault distinctions, remap invalidation, eviction and isolation tests |
| A5 | Add bounded JSON input/output around the models | Invalid input returns exit 2; hash matches exact input bytes |
| A6 | Run host descriptor/process observations | Raw data labeled host observations separately from model outputs |
| A7 | Rebuild without notes, then transfer | New address geometry or arrival-order counterexample tested independently |

Attempt A2 and A3 before inspecting `models.py`. The workbench is a wrapper;
copying it alone does not reconstruct a scheduler or translator. Likewise,
passing the interface tests does not replace running the deeper model suite.

Rubric, 20 points: state/invariant explanation 4; scheduler derivation and
failure cases 4; translation/authority derivation 4; reproducible evidence 4;
reconstruction and transfer 4. For each category, score 0 absent, 1 terminology,
2 ordinary working case, 3 explained edge/failure case, 4 independently checked
transfer. Undetected stale translation, unauthorized cached access, lost job
service, or labeling toy output as host-kernel evidence blocks a passing build.

The next kernel-backed gate is intentionally not marked passed: boot an
inspected kernel/emulator version, capture entry/context-switch/page-fault
traces, and explain registers, protection and device behavior. The current
project is PARTIAL with STRONG bounded mechanism builds.
