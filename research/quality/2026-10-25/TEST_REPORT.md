# Actual priority-checkpoint validation

Recovery base:4ced936c22fb4142165b0e831ad5431761a2ce15. [Frozen baseline](baseline/results.json):27/27PASS. [Current verification](verification-final/results.json):28/28PASS, including69 infrastructure tests,57/57 reference groups and actual prior native C/C++/RISC-V/SystemVerilog/VHDL/Rust/Zig/Go/Java runs. The first structure attempt failed on a pending integration-review link; that initial log is retained and the repaired structure rerun passed. Other passing groups were not rerun merely for chronology.

New mathematics:13 tests actually executed; raw deterministic experiment at foundations/mathematics/initial-value-evidence/evidence/observed-2026-10-25.json. [Separate-reader probes](math-reader-probes.json) confirm16 Fraction matrix identities, an independent nonlinear tangent solution, different-support pulse and real callback limit. [Review](math-reader-review.md) documents its scope. No physical measurements, nonlinear universal proof or learner mastery is implied.

The strong-dashboard arithmetic/gates have seven adversarial tests; the quality auditor has a new stale-STRONG-evidence regression. Current strict content audit exited1 with1783 unresolved heuristic findings. [The gate record](content-gate.json) retains counts. It is not a passing content-completeness result. Known source/license warnings remain.

Reproduce from a Git checkout with the documented optional native tools:

```bash
python3 tools/verify_repository.py --report-dir research/quality/new-local-replay
python3 tools/strong_dashboard.py --check
python3 tools/quality_audit.py --json research/quality/new-content-risk.json
python3 research/quality/2026-10-25/review_math.py
```

The source-only ZIP has no Git metadata; its two Git-only whitespace groups must be reported BLOCKED. The included complete bundle restores those checks. New replay directories preserve historical observations. Full-source extraction/manifest/bundle replay results belong in the external delivery receipt, avoiding self-referential ZIP hashes.
