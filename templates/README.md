# Reusable Templates

Templates are instructions for future artifacts, not completed learning work. Replace prompts with actual inspected evidence and preserve unresolved fields explicitly.

| Template | Use |
| --- | --- |
| [Book intake](book-intake.md) | Source legality, edition, fingerprint, readability and mapping. |
| [Chapter sections](chapter-sections.json) | Thirteen named reconstruction sections; select only useful sections after source inspection. |
| [Project documents](project-documents.json) | Ten required documents for materialized projects. |
| [Experiment](experiment.md) | Prediction, procedure, observations and analysis with raw evidence. |
| [Repository study](repository-study.md) | Architecture before individual files; trace important operations. |
| [Claim](claim.md) | Claim labels, source locators, premises and uncertainty. |
| [Mastery review](mastery-review.md) | Actual learner performance, assistance and reassessment. |
| [Research log](research-log.md) | Question, search process, evidence and decisions. |

`python3 tools/scaffold.py project J-02` creates a registered project without implementation files. `python3 tools/scaffold.py book RESOURCE_ID book-slug` creates a selected book intake. Both refuse existing destinations and leave learning state unchanged. Review the catalog and rerender indexes after a scaffold.

Use `python3 tools/scaffold.py experiment E-002 experiment-slug --project J-01` to prepare a new experiment with no observations.

Chapter documents require actual source inspection and are deliberately not mass-generated. Copy only the needed named sections from the JSON blueprint after creating a genuine BOOK_MAP. Register each chapter with its source resource, locator, artifact path and source-ready status. Validation rejects chapter records without inspected local book evidence.
