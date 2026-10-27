# Quality remediation ledger — audit is not completion

This repository mixes substantial educational work with scaffolded or abbreviated material. A folder, a word count, a validator success, or an AI-generated document is **not** evidence that a learner has mastered a topic or that every subject is covered deeply.

## Evidence categories

- **Working example:** code runs and has relevant tests; limited to tested environments.
- **Worked lesson:** technically specific explanation with derivation and exercises, not generic instructions.
- **Reference trail:** original sources and their claims can be traced; license and provenance checked separately.
- **Guided project:** independent build milestones, code, debugging, tests, experiments, limits and attribution.
- **Paper reconstruction:** actually read the original, extract methods, baselines, results and limitations; never infer a paper's results from its title.

## Current assessment

| Domain | Conservative classification | Main missing proof |
|---|---|---|
| Repository organization | Strong | Check consistency across all tracks |
| Algorithms | Partial to strong | Audit problem diversity and solution/test independence |
| Language mastery | Partial | Replace generic repeated documentation with language-specific mechanisms and tested exercises |
| Mathematics and physics | Partial | More derivations, hardware experiments and prerequisite assessments |
| Electronics/HDLs | Partial | Physical measurement evidence and external toolchain checks |
| Operating systems, networks, databases | Partial | End-to-end annotated builds and systematic fault injection |
| Security/cryptography | Partial | Threat-model-to-implementation guided labs and independent review |
| Machine learning/AI | Partial | Complete small training loop, tokenizer, Transformer, RAG and agent evaluation |
| Computational biology | Partial | Sequence/genome analysis pipelines, evidence and statistics |
| Quantum | Introductory to partial | Circuit derivations, simulations, realistic device/control limitations |
| Research papers | Scaffolded to partial | Source-verified dossier for each claimed work, including actual reported evidence |
| Guided projects | Partial | Fully executable milestones and reproducible observations |

## Upgrade batch — this release

- Detailed [attention derivation](16-machine-learning/21_ATTENTION_FROM_FIRST_PRINCIPLES.md) includes manual example, causal leakage, limits and assignments.
- Executable pure-Python [attention lab](16-machine-learning/labs/README.md) contains tests checking causal properties; it is untrained and not a GPT model.
- Added [training/evaluation case study](16-machine-learning/22_TRAINING_AND_EVALUATION_CASE_STUDY.md) to anchor regression in measurement bias, leakage, shift and production constraints.

## Priorities still outstanding

1. Inspect original books and papers as evidence, preserving exact edition and passages used. Produce original explanations rather than copies.
2. For each major subject, implement one complete learning path through guided project tests and an unfamiliar transfer exercise.
3. Reconstruct *actual* papers from verified primary content before claiming quotas. Authors' methods/results must be sourced, not guessed.
4. Separate prepared experiments from measured results and reviewer evaluation from self-declared completion.
5. Test real toolchains/hardware where possible; clearly mark equipment-dependent experiments as not yet run.

Do not mark the whole repository "excellent" until independent reviews can demonstrate the required depth across representative units in every core domain.
