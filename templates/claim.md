# Claim Record Template

- ID: assign a unique C- identifier.
- Label: SOURCE / DERIVED / EXPLANATION / EXTERNAL / INFERENCE / UNCERTAIN.
- Statement: one bounded, testable or source-checkable assertion.
- Resource IDs: only sources actually inspected for this assertion.
- Locator: exact edition and location, or pinned commit/path/symbol; otherwise UNVERIFIED — source required.
- Artifact: repository-relative Markdown path containing the explanation.
- Status: VERIFIED / UNVERIFIED / CONTRADICTED.
- Assumptions: model, scope and conditions.
- Evidence: repository-relative paths to inspected records or actual raw outputs.

For derivations, write premises and steps. For inferences, state alternatives. Separate direct source content from the author's interpretation and your explanation. A VERIFIED label requires human review of entailment; automated path checks cannot establish truth.
