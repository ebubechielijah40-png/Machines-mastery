# Source verification map

Original interval algorithm, teaching traces, code and tests were written for
this repository. Their correctness arguments follow from the declared project
invariants, not a claim that the arena implements the standard library.

Primary resource inspected on 2026-10-23: WG14, *N1570 Committee Draft*,
2011-04-12, [Programming languages — C](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).
The draft identifies ISO copyright; it is linked as a reference and no substantial
passage is reproduced. It is a C11-era committee draft, not a claim of having
inspected the latest C edition or all subsequent defect reports.

| Inspected locator | Claim scope |
| --- | --- |
| §6.2.4 paragraphs 1–7, printed pp.38–39 | Storage duration and object lifetime; backing-array lifetime differs from project lease state |
| §6.2.8 paragraphs 1–3, printed p.48 | Type alignment requirements and `_Alignas`; no universal eight-byte alignment claim |
| §6.5 paragraphs 5–7 and footnote87, printed pp.76–77 | Representable-expression results and declared/effective type; explains byte-only contract |
| §6.5.6 paragraphs 8–9, printed pp.92–93 | Array pointer arithmetic/subtraction boundary; avoid subtracting unrelated pointers |
| §7.22.3 and §7.22.3.1–5, printed pp.347–349 | Standard allocation/free behavior used only for comparison; this API has a different contract |

Observed compiler flags, sizes and test outcomes are supported by local raw
[evidence](evidence/observed.json), not by the C specification. The fixed capacity,
rounding quantum, metadata layout and fragmentation metric are original project
choices. No upstream allocator implementation was reconstructed or benchmarked.
