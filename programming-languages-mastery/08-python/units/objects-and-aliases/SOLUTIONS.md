# Reasoning checks

1. After outer append, a is[[0]] and b is[[0],[1]]. After inner append, a is[[0,2]]
   and b is[[0,2],[1]] because their first child is still shared.
2. A correct deep clone has a distinct outer list and distinct copied inner list,
   but clone[0] is clone[1]. For a cycle x[0] is x, clone[0] must be clone. Allocate
   and memoize the empty destination before cloning children. Arbitrary class
   cloning is deliberately outside this list-only extension.
3. append changes the referenced list, leaving tuple references unchanged;
   assignment to t[0] would replace a tuple entry and raises TypeError.
4. Check `container is None`, then allocate inside the function. A false-value
   check replaces an intentional empty caller list, breaking the mutation contract.
5. `a={'x':[]}; b=a.copy(); b['x'].append(1)` changes the child visible through a.
   Immutable Fraction values plus binding replacement avoid that failure in the
   bounded interpreter; general mutable object rollback needs another design.
6. Assert is/is not only for intentional shared/distinct objects; use == for
   contents. Immutable cached results simplify sharing but may require conversion;
   deep copies cost graph traversal/allocation and need resource/custom-type rules;
   shared mutable results require caller coordination and can leak state across tasks.
