# Repository development guidelines

This is an established educational repository, not an empty scaffold. Preserve
the supplied development archive improvements and all working implementations.
Read README.md, DEPTH_STANDARD.md, EXCELLENCE_PROGRESS.md and the current audit
before selecting the next dependency-aware implementation batch. The user's
current development mandate takes precedence over historical setup policies.

## Layout and instruction

Numbered domains run from01-computation through20-quantum-computing. Additional
tracks contain foundations, language mechanisms, algorithms, electronics, HDL,
physical machines, production systems, research and guided projects. Keep topic
instruction, source scopes, implementations, tests and experiments together.
Guided projects can explicitly share a domain implementation; do not create a
duplicate copy merely to satisfy a local-file heuristic. Public shared bindings
are recorded in registries/project_implementations.json.

Write original explanations, derivations, intermediate examples, progressive
exercises and separated hints/solutions. Define prerequisites before using them.
Include actual runnable mechanisms and failure experiments where appropriate.
Do not replace shallow templates with longer templates, invented citations or
unexecuted results. EXCELLENT is a qualitative evidence classification, never
an inference from counts or validators. Author preparation and agent-run tests
never establish learner study/mastery.

## Sources and generated files

Inspect exact primary-source scopes before attributing technical claims. Record
authorship, version/date, locator, access and redistribution limits. Keep private
source PDFs/full extracted text and secrets outside public release artifacts.
Absent book originals block fresh chapter-specific claims; they do not block
independent original teaching from other inspected sources.

registries/catalog.json owns marked generated indexes. Use tools/render.py to
regenerate those indexes, rather than editing generated blocks by hand. Other
teaching, audit and progress documents are maintained directly. Preserve historical
raw observations; new runs need new evidence files or explicitly recorded replacements.

## Verification

From the repository root:

```bash
python3 tools/verify_repository.py --report-dir research/quality/local-replay
python3 tools/quality_audit.py --report-only --json research/quality/local-content-audit.json
python3 tools/render.py --check
git diff --check
git diff --cached --check
```

The replay covers infrastructure, reference suites, optional native compilers,
controlled independent probes and whitespace. Missing required toolchains are
BLOCKED, not passing execution. Record exact commands, versions, actual outputs,
known limitations and qualitative review. A report-only audit writes a risk
inventory; it never certifies completeness. Review locally trusted test code
before execution and do not run arbitrary source examples during text scanning.

Use Python3.10+ standard library for portable teaching mechanisms unless a unit
states another requirement. Native labs require their documented compiler/runtime.
The integration environment actually used Python3.12.14 and GCC/G++13.3.0;
those observations are not promises about another machine.

## Git and collaboration

Work on a development/review branch. Never overwrite main or force-push without
explicit user approval. Local verified commits are authorized by the development
mandate. Preserve unrelated human changes, inspect the diff and scope commits
coherently. If remote writing fails, keep developing locally and deliver a full
source archive, Git bundle, checksums and reproducible integration instructions.
Parallel work, when authorized, needs disjoint file ownership and integrated
validation; an author's self-review is not independent review.
