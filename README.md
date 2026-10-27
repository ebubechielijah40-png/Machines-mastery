# Machines Mastery

A permanent workspace for learning computational systems, data systems, security, scientific reasoning and experimental research through source inspection, implementation and evidence.

**Current quality checkpoint:2026-10-25. The original full mandate remains incomplete.**
The GitHub-ready ZIP contains only repository files at its root. Extract it into
your clone and follow [the push instructions](PUSH_INSTRUCTIONS.md); no files need
to be deleted. Checksums and optional recovery history are separate downloads.
The33/33 STRONG objective remains unfinished. The [STRONG readiness dashboard](STRONG_PROGRESS_DASHBOARD.md) keeps fixed
scopes, criterion-level marks and separate original-mandate status. Mathematics,
finite inference and programming now meet their fixed STRONG gates. The [initial-group report](INITIAL_NEAR_STRONG_REPORT.md) is historical; its decision pause has been removed. Domain gates remain stricter than passing tests or numeric readiness.
Read [the domain scorecard](FINAL_EXCELLENCE_AUDIT.md),
[verified progress](EXCELLENCE_PROGRESS.md) and
[remaining work](EXCELLENCE_REMEDIATION_BACKLOG.md). Developed units now connect
foundational mathematics and programming to executable systems, scientific and
AI mechanisms. All twelve coursebook entries have subject-specific routes;
their broad scopes remain partial, and many language/research/topic pages still
need substantial instruction. Passing structural checks is not evidence of
educational excellence.

The purpose is capability: explain mechanisms, reproduce existing work, build independent implementations, design experiments and evaluate what observations actually support. Generated documents do not establish understanding.

## Start or resume a session

1. Read [AGENTS.md](AGENTS.md), [LEARNING_SYSTEM.md](LEARNING_SYSTEM.md) and [PROGRESS.md](PROGRESS.md).
2. Follow [the progressive study route](STUDY_ROUTE.md), demonstrate its prerequisite exit tasks and record learner evidence in [PREREQUISITE_GRAPH.md](PREREQUISITE_GRAPH.md). Check source and license status.
3. Learners study the internal reconstruction and prerequisite bridges. Authors inspect primary sources before writing. Record predictions and attempts before consulting solutions.
4. Preserve source locators, actual outputs, uncertainty and attribution. Assess only what the learner demonstrated.
5. Run the checks below, record meaningful changes and update PROGRESS last with one concrete next action.

The portable archive does not bundle the copyrighted *Code* source. A previously prepared first-unit reconstruction is preserved with explicit source-status limits. [Open the first learning unit](books/code-petzold/generated/chapters/01/README.md) after the prerequisite bridge, or start with [START_HERE](START_HERE.md). Learner study and mastery remain NOT STARTED.

## Navigation

| Area | Use |
| --- | --- |
| [Self-contained curriculum](MASTER_CURRICULUM_SELF_CONTAINED.md) | Learner-facing route including quantum machines and deep cryptography; registry curriculum remains historical/core index. |
| [Prerequisites](PREREQUISITE_GRAPH.md) / [knowledge graph](KNOWLEDGE_GRAPH.md) | Planned dependencies versus relationships established by learning artifacts. |
| [Resources](RESOURCE_REGISTRY.md) / [sources](SOURCES.md) | Stable resource IDs, verification scope, provenance and claim tracking. |
| [Books](books/README.md) / [book registry](BOOK_REGISTRY.md) | Intake, source fingerprints, maps and bounded chapter reconstruction. |
| [Repositories](repositories/README.md) / [repository registry](REPOSITORY_REGISTRY.md) | Original upstreams, revision pinning and architecture-first study. |
| [Projects](PROJECT_REGISTRY.md) | A reproduction → B reimplementation → C experimentation → D extension. |
| [Experiments](EXPERIMENT_REGISTRY.md) | Hypotheses and observations stored separately, with raw evidence. |
| [Mastery](MASTERY.md) | Evidence-based learner states, never inferred from file counts. |
| [Research](research/README.md) / [notes](notes/README.md) | Research questions, logs, corrections and unaided learner work. |
| [Templates](templates/README.md) / [tools](tools/README.md) | Reusable contracts and inspectable, local Python tooling. |
| [Audit](SYSTEM_AUDIT.md) / [overnight report](OVERNIGHT_REPORT.md) | Setup evidence, decisions, limits and handoff. |

## Local commands

Python 3.10+ and Git are sufficient for infrastructure; no third-party Python packages are required. Project-specific toolchains are selected only when needed.

```sh
python3 tools/validate.py
python3 tools/check_publication.py
python3 -m unittest discover -s tools/tests -v
python3 tools/render.py --check
git diff --check
```

Edit [registries/catalog.json](registries/catalog.json) for structured records, then run `python3 tools/render.py`. It updates marked generated indexes only. Never edit those indexes directly. Planning prose, learning artifacts and PROGRESS are maintained manually. Validation checks all owned Markdown files, including untracked files; Git diff alone cannot check a repository before its first commit.

## Source, attribution and storage

Keep legally available book originals in `books/<slug>/source/`; that content is ignored by Git except its intake README. Keep raw private data under a `private/` or `raw-private/` directory. Review paths before copying; do not store secrets in logs. Ignoring a file does not remove it from an existing Git index or history.

Inspect the exact source before mapping chapters. Build original educational explanations instead of reproducing the author's prose. Preserve upstream attribution and license notices. No blanket license is assigned to third-party works or to the owner's future work.

The original registry projects remain evidence-gated, and `projects-guided/` adds assisted-learning project paths across systems, data, security, biology and quantum computing. No learner experiment is automatically considered observed and no subject is mastered.

## Connected expansion

Begin with [counting, quantities and units](foundations/mathematics/counting-and-units/README.md), because no prerequisite learner evidence exists; then return through the bridge to the existing Code Chapter 1 reconstruction. Original sources are optional for verification during normal study.

| Track | Purpose |
| --- | --- |
| [Foundations](foundations/README.md) | Just-in-time mathematics, physics, materials, statistics and programming bridges |
| [Languages](programming-languages-mastery/README.md) | Fourteen dependency-timed language routes, including Zig and RISC-V |
| [HDL](hardware-description-languages/README.md) | SystemVerilog/Verilog and VHDL descriptions, tests and hardware boundaries |
| [Electronics](hardware-electronics-mastery/README.md) | Physical quantities through digital construction |
| [Reverse engineering](reverse-engineering-systems/README.md) | Systematic investigation and black-box reconstruction |
| [Machines](general-machine-systems/README.md) | Energy, information, control and physical interfaces |
| [Algorithms](algorithmic-problem-solving/README.md) | Derivation, proof, application and 20-problem release quotas |
| [Paper seminar](research-paper-reconstruction/README.md) | Source-gated research reconstruction and 10-paper domain quotas |
| [Production](production-systems-engineering/README.md) | Build, measure, fail, recover and scale |

[Expansion report](SYSTEMS_MASTERY_EXPANSION_REPORT.md) distinguishes full exemplars from scaffolds and records validation limits. [Reconstruction drills](reconstruction-drills/README.md) and [unknown-system challenges](unknown-system-challenges/README.md) test generative understanding. Nothing is marked studied or mastered.

## Self-contained completion layer

The repository includes a mixture of developed bounded learning units and draft
navigation layers. The intended self-contained scope is not fully implemented:

- [Start here](START_HERE.md)
- [Self-contained study protocol](SELF_CONTAINED_STUDY.md)
- [Dependency-driven route](STUDY_ROUTE.md)
- [Capability map](CAPABILITY_MAP.md)
- [Limits and reality](LIMITS_AND_REALITY.md)
- [Coursebook wrappers and their current limitations](coursebooks/README.md)
- [Security & cryptography mastery](security-cryptography-mastery/README.md)
- [Computational biology deep handbook](18-computational-biology/DEEP_HANDBOOK.md)
- [Quantum computing and machines](20-quantum-computing/README.md)
- [Guided project ladder](projects-guided/README.md)

These artifacts are instructional preparation, not learner mastery.

## Verified bounded units in this checkpoint

These entries identify developed mechanisms, not completed subject domains.
Each linked unit supplies its own sources, practice, implementation and evidence.
Use [the route and exit tasks](STUDY_ROUTE.md) to enter at the right prerequisite.

| Unit | Runnable mechanism and evidence |
| --- | --- |
| [Mathematical core](foundations/mathematics/core/README.md) | Algebra, proofs, geometry/complex numbers, maps, calculus and optimization with exact alternative checks |
| [Probability and inference](foundations/statistics/probability-inference/README.md) | Finite Bayes/moments, exact coverage, score intervals and independence failures |
| [Numerical reasoning](foundations/mathematics/change-error-and-evidence/README.md) | Secants, finite error, variance, bias and propagated uncertainty |
| [Programming entry](02-programming/python-entry/README.md) / [graphs](algorithmic-problem-solving/topics/graphs/README.md) | Python execution and twenty distinct graph problems with proofs and independent oracles |
| [Byte CPU](01-computation/toy-cpu/README.md) / [compile and link](04-computer-systems/compile-link/README.md) | Explicit instruction traces, symbols, relocations, optimizer observations and failed links |
| [Operating systems](05-operating-systems/SELF_CONTAINED_GUIDE.md) / [synchronization](05-operating-systems/synchronization/README.md) | Scheduling, translation/TLB, real descriptors, lost updates and condition predicates |
| [Stream boundaries](06-networking/stream-boundaries/LESSON.md) / [queries and isolation](07-databases-data-systems/query-isolation/README.md) | Split reads/EOF, local HTTP, bag/NULL operators and actual SQLite schedules |
| [Authenticated provenance](security-cryptography-mastery/provenance/LESSON.md) / [count privacy](13-privacy/count-release/README.md) | Typed input/lineage/replay failures; ideal Laplace proof and finite-sampler limitations |
| [Replica reconciliation](15-distributed-systems/ordering-reconciliation/README.md) | Logical clocks, state joins, tombstones and executable message schedules |
| [RC dynamics](hardware-electronics-mastery/02_RC_TRANSIENTS.md) | Exact/finite-step response, measurement loading and uncertainty |
| [Storage recovery](projects-guided/p07-storage-engine/README.md) | Transaction frames, torn tails, corruption and recovery |
| [Attention](16-machine-learning/labs/DERIVATION.md) | Local derivatives, causal masking and incremental K/V reuse |
| [Model training](16-machine-learning/training/README.md) / [retrieval and tools](16-machine-learning/retrieval-agents/README.md) | Actually trained tiny causal decoder, BPE, leakage/shift controls and bounded deterministic controller |
| [Motor control](17-embedded-robotics/control-path/README.md) | Energy, sensing, saturation, feedback, delay and simulation limits |
| [Sequence alignment](18-computational-biology/02_SEQUENCE_ALGORITHMS.md) | Global/local recurrence, traceback and synthetic analysis |
| [Population and phylogeny](18-computational-biology/population-phylogeny/README.md) | Finite drift/selection, likelihood, distance inversion and clock-model failures |
| [Quantum measurement](20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md) | Tensor ordering, phase, projection and conditional states |
| [Quantum noise](20-quantum-computing/noise-correction/README.md) | Density/channel invariants and ideal repetition-code recovery |
| [Paper practicum](projects-guided/p16-research-reproduction/README.md) | Source-inspected clocks/FFT/privacy/MapReduce dossiers and actual bounded mechanism experiments |

Run `python3 tools/verify_repository.py` for recorded validation and
`python3 tools/quality_audit.py --report-only` for unresolved content risks.
Report-only records an inventory, not a quality pass. See
[reproducible integration](INTEGRATION.md) for this locally committed checkpoint.

## Latest verified ZIP continuation

[Current progress](EXCELLENCE_PROGRESS.md) connects actual new materials/device/
timing/HDL,page-index,DP/structure,native-language,ML-family,lexical-binding,
operations and binary-reconstruction units. Follow [STUDY_ROUTE](STUDY_ROUTE.md)
for prerequisites and exit tasks. [PUSH_INSTRUCTIONS](PUSH_INSTRUCTIONS.md) restores
the included history on a review branch for your manual push. The whole project
remains incomplete; [the domain audit](FINAL_EXCELLENCE_AUDIT.md) and retained
content-risk inventory give the precise boundaries.

[CONTRIBUTING](CONTRIBUTING.md) documents the checks used by the GitHub workflow. Local replay outputs are ignored; curated experiment and review evidence remains versioned. Green checks do not certify educational completeness.
