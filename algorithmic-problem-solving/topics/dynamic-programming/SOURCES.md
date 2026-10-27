# Primary sources and independent extensions

Inspected2026-10-23: MIT OpenCourseWare,6.006 *Introduction to Algorithms*, Fall2011,
course instructors Erik Demaine and Srini Devadas. Selected typed lecture PDFs:

| Original source | Actual inspected scope | Use in this unit |
| --- | --- | --- |
| [Lecture19](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/b6d4083131dd16e7d97f56d04b6e858f_MIT6_006F11_lec19.pdf) | pp1–4 repeated recursion, memoization, dependency order and adding an edge-count state | General state/evaluation reasoning and layered routes; our exactly-k base/source/target semantics are explicit independent contracts |
| [Lecture20](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/9f38f5c9ff4172f8b58be390c89b61d2_MIT6_006F11_lec20.pdf) | pp1–3 state/choice/order workflow, parent pointers and text-layout suffix state | Reconstruction and text-layout mechanism; our squared slack and free final line differ from the source's example cubic badness |
| [Lecture21](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/3484e876d81aba07911a1109f5b5e81e_MIT6_006F11_lec21.pdf) | pp1–5 sequence/interval states, matrix-chain split, edit distance, knapsack and pseudopolynomial cost | Selected foundational mechanisms; source discrepancies below are not reproduced as instructions |

The lecture21 printed p3 edit recurrence says maximum where the stated
minimum-cost objective requires minimum. Its zero replacement-cost sentence does
not supply the LCS equivalence for arbitrary unequal-character replacement. Our
unit distinguishes match cost0, unequal replacement cost1, and the separate
insert/delete-only relation. Lecture19's layered-path printed base/inequality
notation also must not substitute for a precise contract. Here exactly0 edges
reaches only the source at cost0; exactly-k transitions read the previous layer;
'at most' is a minimum over layers. Correctness arguments and finite search
oracles support these choices independently of lecture typography.

All twenty problem statements, examples, Python implementations, hints, proofs
and tests are original repository work for established methods. The package,
counting, maintenance, subset, LIS, grid, reservation, palindrome, bitmask,
Boolean-tree and egg-coverage exercises extend the inspected general state
reasoning; they are not claimed to be exercises copied from those lectures or
full reconstructions of CLRS. Their local derivations identify exhaustive cases
and their independent tests compare actual finite search spaces. This map is
not a claim to have verified every historical origin or inspected a book original.

MIT OCW terms and any credited third-party permissions remain with the sources.
No source PDFs, diagrams or substantial text are bundled. Actual local experiment
observations are [separate](EXPERIMENTS.md); they are not MIT-reported results.
