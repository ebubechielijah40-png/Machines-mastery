# Python syntax with a complete entry build

Start at [the syntax-to-tests bridge](../../02-programming/python-entry/README.md).
It introduces values/types, names, assignment/comparison, indentation, branches,
for/while loops, functions/returns, lists/mutation, exceptions and module/test use
before they become prerequisites for this repository's experiments.

Read the following state transition as source, not mathematical equality:

```python
used = 0
for size in [12, 7, 5]:
    if used + size > 20:
        break
    used = used + size
```

Before each iteration used is the sum of the accepted prefix. The guard prevents
exceeding20 logical payload bytes and break stops before the first oversized
packet. Expected final used is19. A colon/indentation determines blocks; changing
indentation can change which updates occur. Assignment evaluates the right side
before rebinding the name. [The validated implementation and six independent
checks](../../02-programming/python-entry/budget.py) distinguish valid emptiness,
invalid byte counts and prefix admission from maximum-sum packing.

The bridge includes a hand trace, separate exercises/hints/solutions and executed
semantic evidence. Rebuild it without notes before progressing to object aliases,
mathematical loops or the parser project. Python syntax for decorators, classes,
async and patterns is outside this developed entry slice, not silently completed
by one annotated add function.
