# Learning System Operating Policy

## Authority and session scope

Read [AGENTS.md](AGENTS.md) completely at every new session, then this policy and [PROGRESS.md](PROGRESS.md). This policy preserves the owner's setup specification of 2026-09-26. AGENTS.md remains unchanged; its descriptions of the initial empty scaffold are historical. Current paths and commands are in [README.md](README.md).

Infrastructure generation is not learning. Do not infer mastery, completed experiments or original authorship from generated files. Work on one bounded source unit, inspect its quality, then stop for learner engagement. Never automatically reconstruct a whole book.

## Evidence discipline

Never invent facts, quotations, source contents, locations, equations, citations, URLs, authorship, licenses, repository behavior, execution logs or results. If reliable evidence is unavailable, use exactly: **UNVERIFIED — verification required.** Prefer omission to plausible detail.

Use these labels at claim level where needed:

| Label | Meaning and obligation |
| --- | --- |
| [SOURCE] | Supported by the supplied original; include edition/revision and exact inspected locator. |
| [DERIVED] | Show derivation, premises, assumptions and their source IDs. |
| [EXPLANATION] | Original explanation of cited material; do not attribute new wording or inferences to the author. |
| [EXTERNAL] | Name and locate a different inspected source. |
| [INFERENCE] | State the inferential step and plausible alternatives. |
| [UNCERTAIN] | Record the missing evidence and a way to resolve it. |

Source priority: locally supplied original → official specification → original paper → official documentation → original repository → hardware/vendor datasheet → standards organization → university/research institution → authoritative technical reference → secondary explanation. Search snippets are discovery aids, never evidence. Random blogs, content farms and unsourced summaries are not authorities. Web identity verification does not establish chapter contents, code behavior or reuse rights.

Register important claims using [the claim template](templates/claim.md). Record source identity, locator, revision/date, evidence and uncertainty. Recheck changing APIs, security guidance and external links when used. A file hash identifies bytes; it does not establish legitimacy, correctness or authorship.

## Two persistent models

Treat these as the owner's organizing models, not established learner knowledge:

```text
REALITY → observation → measurement → raw data → representation
→ collection → transmission → storage → transformation → analysis
→ information → interpretation → knowledge/conclusion → decision

DATA → representation → transmission → computation → storage
→ protection → verification
```

Working vocabulary for this system (definitions to refine against domain sources): data are recorded representations; information is data interpreted in context; a claim is an assertion; evidence bears on a claim under stated assumptions; a fact is an established state of affairs, whose evidential basis must still be inspectable; truth concerns whether an assertion corresponds to reality; knowledge is an account warranted by evidence and reasoning, open to correction. These terms are not synonyms.

Security controls may support provenance, integrity, authenticity, confidentiality, availability and access history under a threat model. They do not establish that a measurement or claim corresponds to reality. Scientific reasoning evaluates that separate question. A valid signature over a false measurement does not make the measurement true.

## Book and concept workflow

Inspect the actual local source first. If absent, record **SOURCE NOT PRESENT**. Do not replace it with an internet summary. Verify edition, title page, readability and location scheme; distinguish printed pages from PDF indices. Create BOOK_MAP before reconstruction. Classify units as MUST STUDY DEEPLY, REFERENCE, OPTIONAL DEPTH or HISTORICAL/CONTEXT based on dependencies, never on difficulty alone.

For each important concept explain its purpose, problem, prerequisites, mechanism, inputs, outputs, internal state, assumptions, constraints, edge cases, failure modes, interactions and implementation consequences. Show how to observe or test it, a minimal implementation plan, differences from real implementations, supporting evidence and remaining uncertainty. Analogy may introduce; mechanism must complete the account. Connect only to concepts already established or explicitly mark the dependency as pending.

Use [chapter reconstruction templates](templates/chapter-sections.json). Generate only sections with substantive source-grounded work; record justified omissions in GAPS. Do not copy chapters, closely paraphrase long passages or make a prose substitute for a copyrighted book. Use original mechanisms, derivations, diagrams, examples and experiments. Keep necessary short quotations attributed and limited. Respect artifact-specific LICENSE/NOTICE requirements; do not assume public access permits adaptation or redistribution.

## Projects and experiments

Projects progress through A reproduction → B independent reimplementation → C controlled experimentation → D original extension. Do not advance to extension without understanding. Attribute original work, creators, organization, source, license, reproduced elements, independently implemented elements and modifications. Unknown authorship stays unknown. Generated scaffolds are not implementations.

Study repositories from architecture to operations: purpose, entry points, components, control/data flow, structures, interfaces, dependencies, state, storage, networking, security boundaries and tests. Then trace a meaningful operation end-to-end with source paths and a pinned commit. Do not explain code behavior from filenames alone.

Before execution, observed result is **NOT YET OBSERVED**. Separate prediction from measurement. Record question, hypothesis, variables, controls, setup, procedure, measurements, actual raw output, analysis, alternatives, errors, conclusion and follow-up. Capture environment and commands actually used; failed runs are evidence too. Never relabel setup tests as curriculum experiments.

## Progress and quality gates

Use [MASTERY.md](MASTERY.md). Learner evidence is required for every advancement, including delayed unaided recall and transfer for MASTERED. Agent-generated explanations do not establish learner capability. Knowledge-graph edges require cited learning artifacts; dependency plans live separately in PREREQUISITE_GRAPH.

A project is complete only when applicable build, test, documented behavior, mechanism explanation, failure testing, attribution, license, experiment, result and reference checks pass. Record explicit reasons for genuinely inapplicable checks. Never waive a gate just to reach completion.

End each session with validation, meaningful CHANGELOG entries, evidence links and a small concrete next action in PROGRESS. Preserve failed evidence and corrections rather than rewriting history.

## Boundaries and stop conditions

Preserve user material. No publication, pushes, remote creation, purchases, signups, unrelated repository changes, destructive operations or secret exposure. Local commits are permitted but not required. Keep security experiments on controlled local, intentionally vulnerable or explicitly authorized systems; no external attacks. Use synthetic or public non-sensitive data first.

Stop the affected task and document missing/unreadable sources, unclear attribution or required licenses, contradictory evidence, credential requirements, publication risk, destructive changes or unauthorized targets. Continue independent infrastructure work when safe. Never bypass a blocker by guessing.

## Self-contained study and just-in-time foundations

The source/evidence layer grounds authoring and verification. The normal learner route is internal: prerequisite bridge → original deep reconstruction → mechanisms/diagrams → examples → questions → experiment → implementation → debugging → mastery review. Original books, specifications and papers are optional for checking exact language, resolving ambiguity, disagreement or advanced research. Do not require an entire source or external tutorial to understand a prepared lesson. Preserve sources and attribution; write bounded original teaching, not chapter substitutes or copied prose.

Before preparing each unit, inspect mathematics, physics, electronics, chemistry/materials, statistics/probability, programming and prior systems dependencies. Record all seven in PREREQUISITE_BRIDGE.md; a genuine nonrequirement needs a reason. If learner evidence is absent, route through the exact internal prerequisite lesson first. If that lesson is not prepared, mark the main unit's learner gate BLOCKED; do not proceed as though the learner knows it. An author may prepare a dependent exemplar in advance, but preparation is not learner readiness.

Each prerequisite teaches a motivating problem, intuition, concrete example, visual where useful, quantities/units, formal definition, derivation, variable changes, limits, system application, experiment, practice and transfer. Default practice: five basic, three application, two reasoning, one challenge, one experimental and one transfer task, with hints and solutions separate. No experiment output is fabricated; unavailable equipment means EXPERIMENT PREPARED — NOT YET PERFORMED.

Use the catalog's required edges and lesson metadata; rerender PREREQUISITE_GRAPH after dependency edits. `tools/learning_gate.py UNIT_ID` reports missing learner evidence without changing it. Machine-checkable gates complement, not replace, human prerequisite diagnosis. Never force all mathematics before programming or all physics before hardware.

The permanent reconstruction route is observe → decompose → model → hypothesize → instrument → experiment → inspect → derive → reproduce → rebuild → modify → verify. Ten practice levels supplement existing project stages: observe, explain, reproduce, reimplement, break, debug, modify, extend, reconstruct without reference, investigate an unfamiliar related system. See [reconstruction drills](reconstruction-drills/README.md). No curriculum certifies mastery of every possible machine.

## Applied and production engineering

For each major topic, prepare a realistic scenario and executable investigation where practical: concept → simple example → real scenario → implementation → test → measurement → failure → debugging → scaling → production design → experiment → explanation. Required code work cannot be replaced by a prose quiz. Before optimization establish a correct baseline and a measurement method. Record distributions, resource limits, workload and tool versions; Big-O is growth, not exact runtime.

Serious projects add ASSUMPTIONS, BENCHMARKS, FAILURES, SECURITY, OBSERVABILITY, SCALABILITY and POSTMORTEMS to the existing project evidence documents, plus ADRs for significant decisions. Use the production track across phases rather than postponing it. Scale the same system in controlled stages, preserving correctness and recovery comparisons. Code that demonstrates a failure is not automatically a repaired production design. Agent measurements never become learner mastery.

Applied MASTERED reviews require explain, implement, test, debug, measure, optimize, handle failure, scale, secure and operate evidence where applicable; document genuinely inapplicable criteria with reasons. Use bounded local failure injection and synthetic data. No external attacks, real secret exposure, uncontrolled resource exhaustion or unapproved deployment follows from an educational scenario.
