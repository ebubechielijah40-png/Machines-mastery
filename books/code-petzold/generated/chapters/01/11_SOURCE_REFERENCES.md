# Sources and claim ledger

R-CODE: Charles Petzold, *Code: The Hidden Language of Computer Hardware and Software*. Supplied 25-chapter PDF, copyright 2009, paperback preface dated August 16, 2000; numbered edition unverified. All locators below are **1-based physical PDF pages**. Fingerprint and prior visual inspection are in [SOURCE_INDEX](../../SOURCE_INDEX.md) and [intake evidence](../../../../../research/code-source-intake.json).

Only Chapter 1, PDF 6–10, is reconstructed. The existing structural mapping of later chapters is not content reconstruction. The page 7 table was visually checked during intake; this unit uses only its recorded E, T, A and N entries. No source images or full extraction are redistributed.

| Claim | Label | Locator / reasoning |
| --- | --- | --- |
| C-CODE-01 | SOURCE | PDF 6–8, shared code and symbolic/physical distinction; page 7 table |
| C-CODE-02 | SOURCE | PDF 8, relative mark and gap durations; book says about two dashes for word gap |
| C-CODE-03 | SOURCE | PDF 9 opening, scale ambiguity between senders |
| C-CODE-04 | SOURCE | PDF 9, letter-case distinction absent |
| C-CODE-05 | SOURCE | PDF 10 closing, vocal realization of dot/dash patterns |
| C-CODE-06 | DERIVED | A versus ET collision after deleting boundaries; premises C-CODE-01/02; formal proof in 06_FORMALISMS |
| C-CODE-07 | DERIVED | Boundary-sensitive decoder invariant; premises C-CODE-01/02 and lab EOF rule |
| C-CODE-08 | DERIVED | Non-injective normalization cannot have an exact inverse; C-CODE-04 and collision proof |
| C-CODE-09 | DERIVED | Mark count differs from duration cost; C-CODE-02 and PDF 9 frequency discussion; E/T example |

[SOURCE] describes what this inspected text supports, not a universal standard. [DERIVED] describes original reasoning with stated premises. [EXPLANATION] describes our instructional model. No external Morse standard was inspected, and 6τ word gaps are **book-local**, not a standards-compliance claim. The code intentionally uses exact integer timing and a tiny alphabet; the book's approximate physical description does not establish this software interface.

Authorship: original exercises, model, diagrams and implementation prepared by the assistant for this repository; source concepts attributed above. No copied chapter prose, table images or source code. No license to redistribute the original PDF is inferred. Review rights separately before publishing original-source material.
