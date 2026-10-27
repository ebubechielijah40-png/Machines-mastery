# Experiment: stable binding and shared mutable state

Research question: can one mutable parent-chain lookup implement both declaration-order
lexical binding and escaping shared cells? Hypothesis: ordinary counter closures
will not distinguish it from a resolver, but a later-shadow-declaration trace will.

Controls: run the same immutable AST, same empty initial global frame, same evaluation
order and bounds, changing only the lookup mode. Instrumentation: collect primitive
Print results, interpreter node-step counts, static rejection messages, source hash
and Python/platform version. No external input, native callback or filesystem is
exposed by the language. `experiment.py` writes JSON to stdout; redirection records it.

```sh
python3 books/crafting-interpreters/generated/chapters/11/code/experiment.py
python3 -m unittest discover -s books/crafting-interpreters/generated/chapters/11/code -v
```

Actual run: [observed.json](evidence/observed.json), [tests.txt](evidence/tests.txt).
The12 methods passed. In the late declaration case, resolved mode produced
registry,registry while mutable-chain produced registry,block; both consumed16
node steps under this instrumentation. In the factory interleaving case, both
produced1,1,2 and used47 steps. The unchosen own-initializer branch and top-level
return were statically rejected before execution.

Interpretation: matching the counter's ordinary trace is insufficient evidence
for correct lexical binding. The targeted counterexample isolates changing lookup
targets from changing stored values. Equal node counts do not show equal total
runtime cost: parent searches and fixed-hop traversal can have different lengths,
and this instrumentation does not count individual dictionary probes.

Alternative explanations/limits: the AST runner might still share a resolver/runtime
bug on cases absent from these traces. Permanent tests add independently knowable
scope markers, both sides of assignment, a caller-shadowing contrast, recursion,
arity/type/bound checks and distinct AST occurrence addresses. These are finite
contracts, not a proof of all language implementations. No original Lox benchmark
or whole-book implementation was reproduced.

Follow-up: instrument actual parent edges/dictionary probes at increasing lexical
depth; compare persistent environments, fixed addresses and a display/slot design.
Declare precisely whether each implementation shares cells or copies values before
interpreting the results. Rebuild the mechanism without the reference first.
