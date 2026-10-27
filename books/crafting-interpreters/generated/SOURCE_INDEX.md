# Verified source scopes —2026-10-23

| Original | Exact scope inspected | Byte fingerprint and boundary |
| --- | --- | --- |
| Robert Nystrom, Crafting Interpreters, author-hosted chapter11, Resolving and Binding | §§11.1–11.5: static scope; mutable/persistent environments; separate semantic analysis; declaration state; resolver; environment-distance reads/writes; duplicate declarations and return validation | HTML83744bytes, SHA256356b2dee7da9e69eb3d762a9e662bc1d072d3e0f6e6fb31802b832e04cbcaf8c |
| Same author/book, chapter10, Functions | §10.6 Local Functions and Closures: captured declaration environment, escaping local function | HTML83893bytes, SHA256f6e3384f014d21ded592a257de16cdac2002ef96addf9c712037f94d39cea29c |

Primary URLs: https://craftinginterpreters.com/resolving-and-binding.html and
https://craftinginterpreters.com/functions.html. The whole HTML files were
fingerprinted; fingerprints do not mean all chapter10 prose was inspected.
The original footer identifies ©2015–2021 Robert Nystrom. The work's general
redistribution license was not independently cleared in this inspection; no
original chapters, long passages, diagrams or Java code are included.

The Python grammar, AST classes, bounded runner, experiment data, derivation,
worked marker/counter examples, tests and exercises are newly written here.
The named source supports the selected semantic concepts, not every independent
engineering limit or a claim of full Lox compatibility. Source inspection does
not establish learner mastery or an independent review of our implementation.
