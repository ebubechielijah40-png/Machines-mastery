# Graph source verification and authorship

Inspected 2026-10-23. The explanations, twenty contracts, code and independent
oracles in this unit are original repository work. Nothing here reproduces a
textbook or asserts a computational reproduction of a research paper.

| Verified primary teaching resource | Inspected scope | Connection and limit |
|---|---|---|
| Erik Demaine, Jason Ku, Justin Solomon, MIT 6.006 Spring 2020, [Lecture 9: BFS](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/196a95604877d326c6586e60477b59d4_MIT6_006S20_lec9.pdf) | PDF pages 1–4: adjacency, distance layers, shortest-path reasoning | Supports representation and BFS assumptions; the graph/examples/code here differ. |
| Same course, [Lecture 10: DFS](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/f3e349e0eb3288592289d2c81e0c4f4d_MIT6_006S20_lec10.pdf) | Pages 1–4: DFS, components, finishing order, cycle reasoning | Supports the traversal/ordering bridge; Kahn and SCC proofs here are independently developed. |
| Same course, [Lecture 12: Bellman–Ford](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/2430d7903a5529451d80c17f89a41fe8_MIT6_006S20_lec12.pdf) | Pages 1–4: at-most-k-edge recurrence, negative witnesses and propagation | Supports arbitrary-weight assumptions and meaning of unbounded distances. |
| Same course, [Lecture 13: Dijkstra](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/d819e7f4568aced8d5b59e03db6c7b67_MIT6_006S20_lec13.pdf) | Pages 1–4, including nonnegative-edge proof and changeable priority queue | Our lazy heap deliberately has a different storage/operation bound. |

MIT OCW course materials are generally offered under CC BY-NC-SA 4.0 with
item-specific exceptions; follow the source's notices before reusing its own
material. These links are verification references; their PDFs are not bundled
or relicensed here. This record verifies the listed sections, not every claim
in an entire course or every historical attribution.

Low-link, greedy exchange, flow/cut, matching and closure claims in LESSON are
presented with original derivations and checkable mathematical certificates.
The tests independently instantiate their definitions on finite input spaces.
No additional source was silently marked inspected; a broader historical/research
source map is remaining work. The lesson states the model and proof assumptions
so learners can audit the reasoning without leaving the repository.
