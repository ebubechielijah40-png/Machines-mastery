# C++ verification scope

Inspected 2026-10-23. Original Buffer, audit, derivations and exercises are local
teaching work. No third-party source is bundled.

- WG21 working-draft text, [class.dtor](https://eel.is/c++draft/class.dtor),
  paragraphs13–14: member/base reverse destruction and implicit destruction on
  scope/exception exit. Inspected rendered text, not merely a search snippet.
- WG21 working-draft text, [class.copy.ctor](https://eel.is/c++draft/class.copy.ctor),
  paragraphs1–2,6–8,15–16: copy/move signatures, implicit declaration conditions
  and memberwise behavior. The mirror renders the evolving draft; it is **not**
  a pinned normative C++17 edition. Follow its own notices for source reuse.
- Actual local g++13.3.0 compilation under `-std=c++17` at three configurations is
  recorded in observed.json. This verifies the selected teaching subset on this
  toolchain, not complete compiler conformance or ABI portability.

The N4950 PDF was attempted but could not be parsed by the retrieval tool; no
contents or license verification are claimed for that unavailable PDF. Full
standard, allocator failure, library moved-from guarantees, atomics and ABI
chapters remain outside inspected/validated scope. Standard-draft links support
stated ownership/lifetime mechanisms; complexity and class-specific invariants
are derived directly from the original implementation.
