# Inspected index sources and original format

Root inspected2026-10-23, corroborating the author's selected original inspection:

- Berkeley CS186 [Note4 B+Trees](https://cs186berkeley.net/notes/note4/), Properties,
  Insertion and bulk-loading discussion: sorted routing intervals, equal leaf
  depth, leaf data versus internal routing and split propagation. The course's
  order convention is not silently substituted for our byte-derived capacities.
- SQLite official [file format](https://www.sqlite.org/fileformat.html), §1.2 Pages
  and§1.6 B-tree Pages: reference evidence for real page/record organization.
  Our magic, sizes, fixed cells, CRCs and snapshot are original and **not SQLite**.
- SQLite official transaction/atomic-commit distinctions are already scoped in
  the [query/isolation source map](../query-isolation/SOURCES.md) and
  [WAL project sources](../../projects-guided/p07-storage-engine/SOURCES.md).
  A valid page image is not an atomic multi-page commit; the retained mixed
  snapshot is an independently executed counterexample.

The codecs, validation traversal, algorithms, capacity/height proofs, worked
traces, staging policy, oracle tests and synthetic experiments are original.
No source diagram, code implementation, textbook chapter or source problem set is
copied. Public originals retain their own attribution/terms. No whole B-tree
literature survey, storage-engine compatibility or physical disk result is claimed.
