# Entry bridge source map

Inspected 2026-10-23, PSF Python3.12 docs (site renders3.12.15); local runtime3.12.14.
Original byte-budget example, contract, proof, code, oracle and exercises are
repository work, not a paraphrased chapter or borrowed project solution.

| Verified primary resource | Inspected scope | Boundary |
|---|---|---|
| [Python tutorial introduction](https://docs.python.org/3.12/tutorial/introduction.html) | §3.1 numbers, assignment/text; list introduction | Syntax/value foundations only; byte counts are our application units. |
| [Control flow](https://docs.python.org/3.12/tutorial/controlflow.html) | for/if/range/break and function/default explanations | Supports syntax used here; not full language mastery. |
| [Modules](https://docs.python.org/3.12/tutorial/modules.html) | Introduction, imports, §6.1.1 script guard and search path | Module/CLI separation. |
| [Errors](https://docs.python.org/3.12/tutorial/errors.html) | §8.1–8.3 syntax/runtime distinction and selected handlers | Error explanation, not arbitrary exception recovery. |
| [unittest](https://docs.python.org/3.12/library/unittest.html) | Basic example, assert methods and discovery CLI | Test-reading/running bridge; finite tests do not prove general correctness. |
| [Data model](https://docs.python.org/3.12/reference/datamodel.html) | §3.1 identity/type/value and mutability | Alias foundation; deeper sharing is taught in the linked Python unit. |

Python docs state PSF License Version2 and 0BSD for examples/code; no substantial
passage or copied example is bundled. This bridge teaches only the Python needed
to start local computational units. Package management, classes in depth,
concurrency, deployment, C extensions and production engineering remain separate.
