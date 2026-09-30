# Machines Mastery

A permanent workspace for learning computational systems, data systems, security, scientific reasoning and experimental research through source inspection, implementation and evidence.

The purpose is capability: explain mechanisms, reproduce existing work, build independent implementations, design experiments and evaluate what observations actually support. Generated documents do not establish understanding.

## Start or resume a session

1. Read [AGENTS.md](AGENTS.md), [LEARNING_SYSTEM.md](LEARNING_SYSTEM.md) and [PROGRESS.md](PROGRESS.md).
2. Select one unit whose prerequisites have learner evidence in [PREREQUISITE_GRAPH.md](PREREQUISITE_GRAPH.md). Check its source and license status.
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
|

## Local commands

Python 3.10+ and Git are sufficient for infrastructure; no third-party Python packages are required. Project-specific toolchains are selected only when needed.

```sh
python3 tools/validate.py
python3 -m unittest discover -s tools/tests -v
python3 tools/render.py --check
git diff --check
```

Edit [registries/catalog.json](registries/catalog.json) for structured records, then run `python3 tools/render.py`. It updates marked generated indexes only. Never edit those indexes directly. Planning prose, learning artifacts and PROGRESS are maintained manually. Validation checks all owned Markdown files, including untracked files; Git diff alone cannot check a repository before its first commit.

## Source, attribution and storage

Keep legally available book originals in `books/<slug>/source/`; that content is ignored by Git except its intake README. Keep raw private data under a `private/` or `raw-private/` directory. Review paths before copying; do not store secrets in logs. Ignoring a file does not remove it from an existing Git index or history.

Inspect the exact source before mapping chapters. Build original educational explanations instead of reproducing the author's prose. Preserve upstream attribution and license notices. Do not publish solutions or this repository during setup. No blanket license is assigned to third-party works or to the owner's future work.

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

[Reconstruction drills](reconstruction-drills/README.md) and [unknown-system challenges](unknown-system-challenges/README.md) test generative understanding. Nothing is marked studied or mastered.

## Self-contained completion layer

The repository now includes an original self-contained learning layer intended to remove normal dependency on external tutorials/textbook reading:

- [Start here](START_HERE.md)
- [Self-contained study protocol](SELF_CONTAINED_STUDY.md)
- [Dependency-driven route](STUDY_ROUTE.md)
- [Capability map](CAPABILITY_MAP.md)
- [Limits and reality](LIMITS_AND_REALITY.md)
- [Original coursebooks](coursebooks/README.md)
- [Security & cryptography mastery](security-cryptography-mastery/README.md)
- [Computational biology deep handbook](18-computational-biology/DEEP_HANDBOOK.md)
- [Quantum computing and machines](20-quantum-computing/README.md)
- [Guided project ladder](projects-guided/README.md)

These artifacts are instructional preparation, not learner mastery.
