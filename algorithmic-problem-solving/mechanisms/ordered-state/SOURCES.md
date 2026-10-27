# Inspected primary mechanism scopes

MIT OpenCourseWare6.006, Fall2011, instructors Erik Demaine and Srini Devadas;
selected course PDFs actually inspected2026-10-23:

| Source | Scope | Supported mechanism |
| --- | --- | --- |
| [Lecture4](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/8ebfeb1c645b10b3709919603e7d51be_MIT6_006F11_lec04.pdf) | slides3–14 heap property,array relatives,repair,bottom-up build and level-cost sum | Our min-heap uses zero-based indices and an original stable serial tie policy; it is not a copy of the source's one-based max-heap pseudocode |
| [Lecture5](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/d9c745bbfb610e9e53f6aef4261f3805_MIT6_006F11_lec05.pdf) | pp2–5 ordered-query motivation,search invariant,insertion and minimum | Ordered tree foundations; unique-key overwrite, iterative size repair and rank/select are derived here, with their own tests |
| [Lecture8](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/d3e4d64266d481c74c9e7c15e09999fe_MIT6_006F11_lec08.pdf) | pp2–5 finite keys,buckets,chaining,collisions and uniform-hashing assumption | Distinguish equality from collisions and conditional average work; our rolling hash has no claimed universal-hash guarantee |
| [Lecture9](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/160b3b5f9da2e03815ca1e6ee0dba62a_MIT6_006F11_lec09.pdf) | pp1–2 capacity changes,rehashing,geometric growth and amortization | Relocation cost reasoning; the present map grows at.75 load and never shrinks, so it does not implement all source policies |

Original code, examples, practice and operation-count observations are repository
work. The source's example code, diagrams and substantial text are not bundled.
MIT/credited material rights and OCW terms remain with those sources. Author
course pages are references, not a claim that a full book was reconstructed.
Princeton algs4 chapter URLs returned403 in this batch and are not counted as
inspected chapter contents. Independent dict/sorted oracles establish finite
local contracts, not the correctness of every lecture statement or a production
performance guarantee.
