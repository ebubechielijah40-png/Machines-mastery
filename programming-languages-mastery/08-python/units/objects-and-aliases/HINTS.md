# Hints

1. Outer append changes only b. Following index0 still reaches the shared inner list.
2. Memoize by original object identity before descending. Repeated references and
   cycles require returning an already allocated clone.
3. Ask whether the tuple's immediate reference is replaced or its target mutates.
4. An empty supplied list is false in a truth test, but is still an intentional
   object. Distinguish absence by identity with None or a unique sentinel.
5. Place one list under the same key in both dictionary objects and mutate it.
6. Possible cache contracts include immutable results, caller copies or explicit
   shared mutability. There is no universally free copy policy.
