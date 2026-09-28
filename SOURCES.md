# Sources and Provenance

## Evidence boundaries

Resource identity records live in [RESOURCE_REGISTRY.md](RESOURCE_REGISTRY.md). The canonical fields include the original URL, check date, verification scope, license status and local availability. An opened landing page supports identity only unless the scope explicitly says more. No full book has been locally inspected. No external repository implementation has been traced or executed.

The owner's 2026-09-26 specification is the source of the curriculum scope and operating policy; prerequisite sequencing and project plans are explicit design choices, not claims made by the registered authors. See [LEARNING_SYSTEM.md](LEARNING_SYSTEM.md).

## Claim registration

Use [templates/claim.md](templates/claim.md). Add a record to `claims` in [catalog.json](registries/catalog.json) with `id`, `label`, `statement`, `resource_ids`, `locator`, `artifact`, `status`, `assumptions`, and `evidence` (repository-relative paths). Labels are SOURCE, DERIVED, EXPLANATION, EXTERNAL, INFERENCE or UNCERTAIN. Human review must confirm that cited evidence supports the precise claim; a validator cannot do this.

For a book, record the inspected edition and printed page/section plus PDF page index where applicable. For code, record commit SHA, path, symbol and inspected line range. For a web source, record page/heading and access date. For a derivation, identify premises and show steps. Never fill missing locators from memory.

## Source intake and validation

1. Establish lawful local availability without copying purchase records or personal information into Git.
2. Read the title/copyright page or upstream metadata. Preserve LICENSE/NOTICE as required; unknown reuse rights block copying.
3. Fingerprint the actual file with `python3 tools/fingerprint.py PATH`. This prints metadata only and changes no progress state.
4. Inspect readability, diagrams and location mapping; record observations in the book's SOURCE_INDEX. Hashes do not validate contents.
5. Add reviewed metadata to the registry and mark local availability only after inspection. Keep changed editions as distinct source versions.
6. Revalidate source hashes and exact locators before using an existing reconstruction. Record corrections rather than silently changing evidence.

## Setup verification log

Checks dated 2026-09-26 used opened original/official pages. Exact successful URLs and bounded claims are in each resource record. No search snippet was accepted as evidence. The Petzold companion introduction verifies second-edition bibliographic identity, not the edition of a nonexistent local file. Nand to Tetris home, software and license pages support the first project's limited attribution record.

Primary-page failures remain explicit: K. N. King's book site was unreadable through the browser; OpenStax chemistry/physics detail pages yielded no readable body. Crafting Interpreters' website also failed; its original repository and LICENSE were available. Some book author lists and licenses remain unverified. These failures do not justify substituting secondary summaries.

No external URL availability checker runs automatically: it could only test reachability, not truth. Reopen and inspect the actual source when a claim or implementation needs it.
