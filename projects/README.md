# Project Workflow

See [PROJECT_REGISTRY.md](../PROJECT_REGISTRY.md). Only J-01 is prepared now; later work remains PLANNED. Create a registered project on demand with `python3 tools/scaffold.py project J-02`. The command refuses an existing destination and does not create implementation directories.

Every materialized major project has README, ORIGIN_AND_ATTRIBUTION, DESIGN, ARCHITECTURE, PREREQUISITES, BUILD_LOG, EXPERIMENTS, TESTS, RESULTS and REFERENCES Markdown files. Add `src/` and `tests/` when actual implementation starts.

## Four stages

A — reproduce a bounded educational mechanism from identified original work.

B — implement the idea independently, recording consulted sources and assistance.

C — vary assumptions, break components and measure behavior with preserved evidence.

D — propose and implement an original extension only after demonstrated understanding.

Stage advancement is a reviewed decision, not a generator action. Preserve attribution even when the code is independently written. A license gap blocks importing upstream material, not drafting an independent design.

## Completion

Use the `quality_gates` fields in the catalog and record supporting evidence for build, tests, behavior, explanation, failure cases, attribution, licenses, experiments, results and references. Mark COMPLETE only after all applicable gates pass. A justified `NOT APPLICABLE: reason` is reviewed case by case. No project has passed these gates yet.

## Applied progression and evidence

Use ten practice levels from [observation to unfamiliar-system investigation](../reconstruction-drills/README.md) within the existing four stages. Production-style work also keeps ASSUMPTIONS.md, BENCHMARKS.md, FAILURES.md, SECURITY.md, OBSERVABILITY.md, SCALABILITY.md and POSTMORTEMS.md alongside existing design/architecture/experiments/results. Use the [ADR](../production-systems-engineering/templates/adr.md) and [postmortem](../production-systems-engineering/templates/postmortem.md) templates. Record applicability; do not fabricate a benchmark for an unbuilt project. Before optimizing, implement, test, profile, baseline, load, identify a bottleneck, change, remeasure, inject failure, recover and instrument.
