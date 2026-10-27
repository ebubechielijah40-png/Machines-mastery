# Book Processing

Use [BOOK_REGISTRY.md](../BOOK_REGISTRY.md) for intake status and [RESOURCE_REGISTRY.md](../RESOURCE_REGISTRY.md) for candidate identities. Future books stay registry entries until selected; do not create empty book trees for the whole reading list.

## Intake

Create `books/<book-slug>/README.md`, a `source/README.md` with local storage instructions, and `generated/BOOK_MAP.md`, `CONCEPT_INDEX.md`, `PREREQUISITES.md`, `SOURCE_INDEX.md` when a book is selected. Start from [the book intake template](../templates/book-intake.md). `python3 tools/scaffold.py book RESOURCE_ID book-slug` prepares these without inventing contents.

Store originals under `source/`; Git ignores them. Inspect the actual file before recording edition, content structure or source status. Fingerprint with [the local tool](../tools/fingerprint.py). Absent means SOURCE NOT PRESENT. Unreadable means blocked, not processed. Do not use a web summary as the missing book.

## Map before reconstructing

BOOK_MAP records inspected chapters/sections, dependency order, foundational/supporting/advanced roles, depth class, curriculum links and project/experiment relevance. SOURCE_INDEX records edition, SHA-256, readability checks, locator convention and important claim locations. CONCEPT_INDEX links established concepts to their actual artifacts. PREREQUISITES distinguishes tested learner evidence from assumed background.

Create `generated/chapters/<chapter-number>/` only after inspection and source mapping. Use [chapter templates](../templates/chapter-sections.json), preserving the source's chapter identifier. Generate only sections with useful work; record omitted sections and reasons in GAPS. Register each reconstructed unit in the catalog's `chapters` collection. Never label an intake scaffold a processed chapter.


## Developed selected companion

[Crafting Interpreters: lexical binding and closures](crafting-interpreters/README.md)
now has an original executable chapter11 companion, inspected source map,
worked traces,12 tests, actual negative-control experiments and separated practice.
Its whole-book reconstruction remains PARTIAL; other registered entries are not
silently counted as processed.
