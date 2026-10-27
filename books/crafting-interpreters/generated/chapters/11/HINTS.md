# Hints after a serious attempt

1–3. Draw dictionaries as boxes; keep a separate arrow for the use→target binding.
4–5. Count parent edges, not frame boxes. A function's parent comes from declaration.
6. Ask whether the new name should already shadow an outer name while unready.
7–9. Distinguish two calls to the factory from two calls through one returned function.
10–12. Resolution traverses text without taking branches; runtime global slots are
special. Declare a function's own name before visiting its body.
13–15. A syntactically identical use can have a different lexical address; traversing
one node once does not make the search through h scopes free.
16–18. Extend validation, traversal and evaluation together. A changed semantic rule
is a language design choice with new tests, not a patch to one lookup line.
19–20. Consider host allocation, recursive traversals, errors after side effects and
untrusted Python access. Use deliberately different values in every frame so a
wrong address becomes visible.
