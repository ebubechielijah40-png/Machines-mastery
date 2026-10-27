# Required bridges

First complete [the C compile/link and pointer-length lesson](../../04-computer-systems/compile-link/README.md).
You must compile two translation units, distinguish an undefined symbol from an
invalid runtime access, and explain why a pointer alone does not encode length,
permission, or lifetime. This project adds explicit allocation metadata.

Practice a small array insertion and deletion before implementing blocks: move
entries right from the end when inserting, and left from the removed index when
deleting. Reversing the insertion loop overwrites entries before copying them.
Use half-open intervals; show that `[0,8)` and `[8,24)` touch but do not overlap.
Review integer division and derive rounding for 7, 8, 9 and 256 with quantum 8.

Entry test: draw the five states in the README worked example without code.
Explain why one 16-byte request fails when sixteen isolated 8-byte holes exist.
If either is unclear, rework those traces before inspecting the reference.

Tools are a C11 compiler and Python 3.12+. The harness uses strict warnings and
GCC/Clang-style UBSan flags. If your compiler lacks UBSan, report that specific
run BLOCKED; do not silently report the full harness passed. No external
allocator library is needed.
