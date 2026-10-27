# Actual combined initial-group validation

Recovered base:4ced936c22fb4142165b0e831ad5431761a2ce15. Mathematics checkpoint9e1149e was saved before inference development. [Combined verification](verification-final/results.json):28/28PASS, including69 infrastructure tests,57/57 reference groups and actual C/C++/RISC-V/SystemVerilog/VHDL/Rust/Zig/Go/Java execution. No optional native group is BLOCKED in this checkout.

New domain checks:13 dynamics tests and27 finite-inference tests actually passed, together with separate-author reader probes. The statistics experiment fingerprints all five current executable files; those hashes were checked again. [Mathematics review](../2026-10-25/math-reader-review.md) and [inference review](../2026-10-25/statistics-reader-review.md) record exact independent formulas/controls and repaired defects. These are trusted local synthetic models, not physical experiments or historical benchmark reproductions.

The strict content-risk gate exited1 with1791 findings. [Its exact counts](content-gate.json) remain unresolved. The gate is not a pass; source/rights warnings and the original full mandate remain unfinished. Quantitative readiness is the separate fixed-rubric judgment in the dashboard, not inferred from these counts.

Reproduce with the documented tools from the repo root:

```bash
python3 tools/verify_repository.py --report-dir research/quality/new-local-replay
python3 tools/strong_dashboard.py --check
python3 research/quality/2026-10-25/review_math.py
python3 research/quality/2026-10-25/review_statistics.py
python3 tools/quality_audit.py --json research/quality/new-content-risk.json
```

New evidence belongs in new directories. Source-only extraction lacks Git metadata, so its two Git whitespace groups are BLOCKED. The included full bundle restores them. The external delivery receipt records the actual ZIP CRC/byte-manifest/bundle checks and fresh extracted-source replay; no self-referential archive hash is claimed in committed source.
