# Source Index — Code

## Inspected local source

- Resource: R-CODE.
- Path: `books/code-petzold/source/code-charles-petzold.pdf`.
- Size: 9,670,974 bytes; 363 physical PDF pages; no PDF encryption reported by `pdfinfo`.
- SHA-256: `2fa522b604039c033b22c03e0e4259cfba59973212130442887e12ecd2044864`.
- Provenance: the user supplied the file directly in the designated directory. Inspected in place; no assistant download, copy, move or deletion. Earlier acquisition history is UNVERIFIED — source required. No personal purchase information collected.
- Git: ignored by `/books/*/source/*`; no tracked files under the source directory during intake. Preserve the original bytes.
- Inspection record: [code-source-intake.json](../../../research/code-source-intake.json).

## Identity and edition

[SOURCE] PDF page 2 gives the title, Charles Petzold and copyright 2009. PDF pages 4–5 contain a preface labeled for the paperback edition, ending August 16, 2000. The file has 25 numbered chapter headings.

[UNCERTAIN] No explicit numbered edition statement was found in the inspected front matter. Record **supplied 25-chapter text, copyright 2009, paperback preface 2000; numbered edition unverified**. Do not label it the second edition or borrow the second-edition website's locators. PDF metadata reports calibre conversion; this is reported software metadata, not evidence of lawful acquisition or original publication date.

## Locators and readability

Use **1-based physical PDF pages**, including the initial page with no extracted text. These are not printed book pages. Internal references to original pagination do not establish a universal page offset for this converted file.

Text extraction succeeded. Chapter 1, PDF 6–10, was read completely. PDF 2, 7 and 8 were rendered and inspected visually: title/author page, letter-code table and timing illustrations are readable. The embedded table/diagram contents are missing from plain text extraction, so they were checked visually. A `.-`, E `.`, T `-`, N `-.` were verified in the page 7 table.

Other chapters were inspected only for structural headings and start locations. Their detailed contents and illustration completeness remain unverified. No later chapter was reconstructed.

## First-unit source locations

| ID | Physical PDF location | Supported scope |
| --- | --- | --- |
| S0 | 2, 4–5 | Title, author, copyright statement, paperback-preface label/date. |
| S1 | Chapter 1, 6–8; table on 7 | Shared code mappings and distinction between symbolic notation and physical signal. |
| S2 | Chapter 1, 8, timing prose and diagrams | Relative mark durations; internal, character and word gaps in this text. |
| S3 | Chapter 1, 9, opening paragraph | Relative timing and ambiguity across different sending speeds. |
| S4 | Chapter 1, 9, frequency/case discussion | Shorter codes for common letters; no uppercase/lowercase distinction. |
| S5 | Chapter 1, 10, closing discussion | Alternative vocal realization of the dot/dash distinction. |

[SOURCE] Page 8 describes dot duration τ, dash 3τ, internal gap τ, character gap 3τ and a word gap of about two dashes (6τ). The lab follows this **book-local idealization**. No external Morse standard was verified, so the lab does not claim standards compliance, physical tolerances or measured performance.

## Claim and copyright boundaries

The first unit's SOURCE_REFERENCES file identifies source-backed premises and original derivations. The decoder, collision examples, diagrams and exercises are original educational work, not algorithms or wording attributed to the author. No full extraction or book images are stored in versioned artifacts. Original redistribution rights remain unverified; this study workflow grants none.
