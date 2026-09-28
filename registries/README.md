# Structured Registry

`catalog.json` is the canonical structured record for resources, phases, prerequisite units, projects, selected book intakes, experiments, chapter artifacts, claims, knowledge edges and mastery reviews. Stable IDs must not be reused for different works or concepts.

Run `python3 tools/render.py` after edits to rebuild the seven marked root indexes, then `python3 tools/validate.py`. Unmarked learning artifacts are never renderer outputs. The root KNOWLEDGE_GRAPH, MASTERY and PROGRESS documents include reviewed narrative; keep them consistent with the catalog when evidence changes.

## Source and learning states

Resource verification describes identity only: IDENTITY VERIFIED / PARTIALLY VERIFIED / UNVERIFIED. Local source availability is a separate field. Selected book status is SOURCE NOT PRESENT or INSPECTED; INSPECTED requires actual source path, matching SHA-256, edition and an inspection-evidence file. Do not mark unreadable sources inspected.

Project status: PLANNED / PREPARED / ACTIVE / BLOCKED / COMPLETE. Experiment status: PLANNED / BLOCKED / RUNNING / OBSERVED / ANALYZED. Before observation, `observed_result` must be NOT YET OBSERVED. Evidence values are repository-relative paths to nonempty files, never invented logs.

Unit and mastery states use the vocabulary in MASTERY.md. Templates document claim and assessment record fields; `tools/validate.py` defines required field types. All conceptual and learner evidence collections start empty. A generated chapter record requires an inspected book, real locator and source-ready flag, with MAP, SOURCE_REFERENCES and GAPS artifacts present.

## Versioning and review

Schema version is 1. Before changing fields, update validation and renderer together. Keep unknown metadata explicit, not silently omitted. Preserve edition/revision distinctions when sources change. Passing checks validates structural contracts, not truth; review source support before changing epistemic or learning states.

## Expansion collections

`tracks` connects permanent routes to existing phases/units/resources. `lessons` separates preparation status, artifact path, prerequisite bridge and project/experiment links from learner state. `expansion_plan` records algorithm/paper release quotas and category maps; empty completed lists are intentional. Unit `path` identifies the exact internal artifact when available; optional `applied` flags require additional mastery criteria. Existing IDs and prerequisite edges are preserved or strengthened, never replaced by prepared content.
