# Python object graphs and visible mutation

Use [objects-and-aliases](units/objects-and-aliases/README.md) for a complete
worked unit, six tests and actual object/bytecode observations. Assignment binds
a name to an object. Lists contain references to children, so an outer copy does
not imply independent inner state.

For a=[[1]], b=a and c=a.copy(), a and b share their outer list; c has a distinct
outer list but shares the inner [1]. Mutating b[0] changes a's and c's visible
child. Appending a new outer item to c leaves a's outer entries unchanged. A tuple
containing a list can likewise retain the same child reference while that child
mutates. These are graph relationships, not unexplained exceptions to immutability.

[The local model](units/objects-and-aliases/model.py) compares identity and values
without fixed addresses. A deep-copy cycle test checks memoization and shared
substructure; custom class/resource copying remains a separate contract. Rebinding
x=x+[2] and list augmentation x+=[2] produce different alias-visible outcomes,
recorded in [observed.json](units/objects-and-aliases/observed.json).

Portable Python does not guarantee immediate object finalization. Explicitly
close resources or use context managers instead of relying on del/refcount timing.
The linked source map distinguishes Python semantics from local CPython3.12.14
bytecode. Garbage-collector implementation, C-extension layouts and concurrent
memory behavior are not established by these selected list examples.
