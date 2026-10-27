# System Audit

Audit date: 2026-09-26. Scope: the complete repository/workspace at `/home/elijah/machines-mastery`, excluding Git object contents from the learning-source inventory. No other workspace root was supplied; no claim is made about books elsewhere on the owner's computer.

## Initial state and preservation

Read AGENTS.md completely before other audit work. The initial repository contained that nonempty contributor guide, four zero-byte files (MASTER_CURRICULUM.md, KNOWLEDGE_GRAPH.md, PROGRESS.md and SOURCES.md), seventeen empty numbered subject directories, and empty books/projects/experiments directories. Environment-owned `.agents/` and `.codex/` were empty and left untouched.

Git was on unborn branch `master`, with no commits and five untracked Markdown files. No tracked files or remotes were found. There was no code, package manifest, test suite, book source, dataset or external checkout. A recursive file inventory included hidden workspace entries and found no locally available *Code* source.

[Initial inventory](research/setup-before.json) preserves exact file sizes/hashes and original top-level directory names. AGENTS.md's SHA-256 was checked after setup and matches the initial value. The earlier instruction not to modify an existing AGENTS.md was retained; detailed owner policy is in LEARNING_SYSTEM.md and linked from README. No nonempty user material was overwritten, deleted or moved.

## Created and modified

Populated the four empty planning files. Created the operational README/policy, prerequisite and mastery systems, resource/book/repository/project/experiment registries, source procedures, templates, quality-control tools/tests, first-book intake, first-project documentation, a planned experiment, audit/changelog/report and subject navigation.

Canonical data: `registries/catalog.json`, containing 45 resource candidates/identity records, 17 phases, 22 prerequisite units, 17 planned projects, one selected book intake and one planned experiment. The chapter, claim, established knowledge-edge and mastery-review collections are empty. Seven marked Markdown indexes are rendered from this catalog; learning narratives and progress are maintained separately.

Only the selected book and first project are materialized. Later projects/books remain registry entries with on-demand scaffolding, avoiding empty implementation trees. No `src/`, project `tests/`, book chapter or experiment `raw/` directory was created without substantive content. Tool tests are infrastructure tests, not project tests.

The exact created/modified/preserved path inventory is in [setup-inventory.json](research/setup-inventory.json). Temporary construction scripts remained in `/tmp`; they are not runtime dependencies.

Final inventory: 79 created files, four populated placeholders and one preserved original file.

## Directory normalization

Renamed only inspected-empty directories; [directory-migration.json](research/directory-migration.json) records all ten moves. Databases became `07-databases-data-systems`; later existing subjects were renumbered to make room for `09-scientific-reasoning` and `12-data-security`. Security became `11-cybersecurity`. The final nineteen subject folders match the requested architecture. Information science/scientific reasoning share P08; cybersecurity/data security share P10. `registries/` is an added technical directory to prevent duplicated machine-readable state.

## Dependency decisions

Kept the requested progression with bounded bridges: evidence logging from U00, process/descriptor concepts before the shell, proof/discrete math before algorithms, probability before inference/cryptography, linear algebra/calculus before advanced regression/ML, and physical/chemical foundations before robotics/biology. Official Modern Robotics prerequisite guidance also supports its math/physics entry gate. Bridges are requirements to verify, not extra completed courses.

Grouped allocator and compiled-program inspection in J-04; grouped TCP/HTTP/networked exercises in J-06. Deferred advanced consensus-paper, research-paper, dataset and hardware selection until their prerequisites and precise research questions exist. The first subject unit is U01; exact book chapter selection awaits source inspection.

## Source verification and limits

Inspected official/original resource landing pages and selected README/LICENSE pages. Each registry record states the exact URL, check date and verification scope. Titles/identities verified online do not imply books were read or code behavior inspected. Candidate records preserve explicit uncertainties rather than guessed authors, editions or terms.

Nand to Tetris identity, creators and website license statement were verified for first-project attribution. No distribution was downloaded or copied; artifact-specific license review remains required before import. Crafting Interpreters' original LICENSE distinguishes code from prose terms; the registry records that distinction. No copyrighted book content was reconstructed.

Missing: all local book originals, pinned external checkouts, learning datasets, learner baseline evidence and domain-specific research sources. The author's *Code* companion identifies a second edition, but no local edition is established. No source outside the supplied workspace was searched or assumed absent.

## Git and security

Created `.gitignore`, `.gitattributes` and `.editorconfig`. Verified ignore matches for proposed book-original, environment, private-data and build-output paths without creating those files. Set local `core.whitespace=trailing-space,space-before-tab` and `core.safecrlf=true`; read back both values. The initial `.git/config` write failed because the mount was read-only; approved elevated execution succeeded. No global configuration or author identity was changed.

No commits, pushes, remotes, publishing, purchases, signups or external attacks occurred. Files remain untracked/uncommitted on the existing unborn branch for review; this is not a claim of an empty Git status. No secrets or private datasets were encountered or copied. Ignore rules are not a secret scanner or backup.

## Validation and encountered issues

The 31-test standard-library suite passed. It exercises duplicate/malformed records, missing resources, cycles, source fingerprints, chapter source gates, result/evidence separation, completion/mastery gates, link detection, source/private exclusions, traversal/symlink rejection and non-destructive book/project/experiment scaffolding. Renderer drift, Git whitespace checks and ignore/config checks passed. Actual command outputs are retained in [validation-2026-09-26.json](research/validation-2026-09-26.json).

An interim validator run reported the then-empty PROGRESS and two not-yet-created report links; these were setup-order issues, repaired before handoff. Browser retrieval failed for King's book page and the Crafting Interpreters website; OpenStax detail pages produced empty bodies. No snippets were substituted as evidence. Known source/license warnings remain separate from structural failures; strict validation intentionally treats them as blockers.

Final structural validation returned zero errors and 47 known source/license warnings. Strict mode returned exit code 1 for those same known gaps, as designed. A one-off inventory helper initially imported script-oriented tooling as a package and failed to resolve `render`; rerunning with the tools directory on its import path succeeded. No inventory was fabricated or partially accepted.

## Assumptions and unresolved risks

Use Python 3.10+ standard-library tooling (tested with Python 3.12.3). No learner competence is assumed. Curriculum ordering is a revisable design, not a validated optimal sequence. Markdown inline destinations are checked; fragment anchors/reference-style links and arbitrary prose claims need manual review. Structural validation cannot prove evidence supports a claim, a license permits reuse, or the learner understands a mechanism.

Live URLs/branches can change; pin editions/commits at intake. No local backup mechanism was configured because no backup destination was supplied. Treat this local-only repository as needing a separately chosen private backup strategy. Do not publish to solve that problem without authorization.
