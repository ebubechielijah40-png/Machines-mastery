# Mastery and Evidence

## Current state

Every unit is **NOT STARTED**. No learner assessments, implementations or learning experiments have been recorded. The `mastery` collection in [catalog.json](registries/catalog.json) is empty. Infrastructure tests assess tooling only.

## State criteria

| State | Minimum evidence |
| --- | --- |
| NOT STARTED | No learner engagement established. |
| MAPPED | Learner identifies the bounded unit, prerequisites, source locations and unresolved terms. An agent-created map alone is insufficient. |
| STUDIED | Dated learner attempt with questions, source references and identified gaps. |
| RECALLABLE | Unaided answers to previously specified retrieval prompts; record errors and assistance. |
| EXPLAINABLE | Learner explains mechanism, assumptions, state changes and failure modes without substituting analogy. |
| APPLICABLE | Correct use on a new problem, with reasoning and limitations. |
| IMPLEMENTABLE | Independent minimal implementation or appropriate formal construction, with tests and attribution. |
| DEBUGGABLE | Reproduce a failure, isolate a cause using evidence, repair it and preserve regression tests. |
| EXPERIMENTALLY VERIFIED | Learner predicts, runs and analyzes a relevant controlled check; raw outputs and alternatives preserved. Scope is the tested mechanism, not universal truth. |
| RECONSTRUCTABLE | Unaided architecture/mechanism or implementation reconstruction, compared to a reference with missed/false assumptions recorded. |
| TRANSFERABLE | Apply the principle to an unfamiliar related system with independently justified assumptions. |
| PRODUCTION-APPLICABLE | Scoped implementation, tests, measurement and security evidence under realistic requirements. |
| SCALABILITY-TESTED | Correct baseline, controlled load increase and comparison with bottleneck and resource evidence. |
| FAILURE-TESTED | Controlled fault injection, detection and recovery verified with actual outputs. |
| OPERATIONALLY-UNDERSTOOD | Explain and exercise observability, release, rollback and incident procedures for the scoped system. |
| MASTERED | All applicable prior evidence, delayed unaided recall, transfer to a fresh problem and reviewed explanation of failures/limits. Unresolved core gaps block this state. |

## Recording and reviewing

Use [templates/mastery-review.md](templates/mastery-review.md). A `mastery` record contains `id`, `unit_id`, `state`, `assessed_on`, `assessor`, `evidence`, `assistance`, `gaps`, `next_review`, and `criteria`. Link actual learner work in `notes/`, implementations or experiment evidence. Write criterion-specific evidence rather than just marking checkboxes.

Proposed review cadence: next session, one week later, then one month later; adjust to actual recall. This is a scheduling policy, not a claim of optimal learning science. Never auto-promote on elapsed time or passing an infrastructure check. Record reassessment and demotion when understanding fails; preserve prior attempts.

For theoretical units, an executable counterexample search or checked derivation may satisfy a practical criterion when justified. An inapplicable criterion requires a written rationale and review; absence of evidence is not inapplicability. “MASTERED” is scoped to a defined unit and model, never an entire field by implication.

## First Code unit prepared — 2026-09-27

The [first unit](books/code-petzold/generated/chapters/01/README.md) and its [assessment protocol](books/code-petzold/generated/chapters/01/12_MASTERY_TEST.md) are ready. CODE-01 is a bounded part of U01; it does not replace the full unit exit gate. All learner states remain NOT STARTED and the mastery collection remains empty. No dated learner attempts, completed learning experiments or assessment results were supplied.

The assistant's decoder tests validate reference software only. E-002 remains PLANNED / NOT YET OBSERVED. Record a learner's original trace, proof, transfer attempt, assistance and delayed recall before considering any advancement.

## Expansion evidence rules

All new foundations, languages, systems exemplars and production labs remain NOT STARTED for the learner. Preparation states (SCAFFOLDED/PREPARED) are distinct from capability states. Production states are scoped capabilities, not automatic steps earned by elapsed time or read pages.

The ten [project practice levels](reconstruction-drills/README.md) supplement existing A/B/C/D stages. Add `debugging`, `reconstruction` and `applied_scope` criterion evidence to MASTERED reviews; the validator requires them. For an applied unit it also requires `tests`, `measurement`, `optimization`, `failure_handling`, `scaling`, `security` and `operations`. A justified inapplicability must describe the scoped reason and review evidence, not silently omit a criterion. Existing delayed recall, transfer, mechanism, failure analysis, implementation and experiment gates are preserved.

Advanced state-specific criteria are enforced in tools/validate.py. Criterion narratives must link actual learner artifacts and explain limits; structural checks cannot assess truth or competence. The prerequisite reporter never promotes states and requires matching evidence-bearing reviews. No state was advanced by the agent's compilation, simulation or benchmark runs.
