# Predict before executing

1. Starting `a=[[0]]; b=a.copy()`, predict effects of `b.append([1])`, then
   `b[0].append(2)`. Draw two stages, identifying which lists are shared.
2. Starting `inner=[]; a=[inner,inner]`, what sharing should deepcopy preserve?
   Implement a memoized list-only clone supporting cycles and test it independently.
3. Predict tuple/list behavior for `t=([1],); t[0].append(2)` and for assigning
   `t[0]=[3]`. Why does tuple immutability allow one but prohibit the other?
4. Design an API whose optional container argument creates a fresh list when
   omitted but mutates an explicitly supplied empty list. Why is `if not container`
   wrong for that contract?
5. Explain why a copied dictionary rolls back the mini-language's bindings but
   not arbitrary nested mutable updates. Give a one-step counterexample.
6. Rebuild the semantic assertions from memory without using literal id() values.
   Transfer the reasoning to a cache returning mutable nested results. Propose
   an ownership policy and state its time/memory trade-off.
