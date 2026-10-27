# Computer systems: one connected execution path

This phase now starts with [from two C files to a running process](compile-link/README.md).
It supplies an original source→object→symbol/relocation→executable investigation,
worked pointer/length/lifetime cases, recorded machine output, exercises and tests.
The scope is deliberately bounded: a full loader, complete ABI, cache hierarchy,
threading and kernel are not delivered by that one build.

Follow the existing [C byte-parser lesson](../programming-languages-mastery/01-c/units/01-byte-parser/LESSON.md)
first if byte bounds or C pointer expressions are unfamiliar. Then study the
compile/link unit, build the [bounded arena allocator](../projects-guided/p04-memory-allocator/README.md),
and continue into [OS execution, scheduling and address translation](../05-operating-systems/SELF_CONTAINED_GUIDE.md).
The [shell project](../projects-guided/p02-shell/README.md) combines actual child
processes and descriptor lifetimes after those mechanisms are understood.

A failed link, an invalid pointer and an unresponsive child are different classes
of failure. This route teaches how to distinguish them through observable state
and exact contracts rather than treating every error as “the code does not work.”

Run the compile/link tests from the repository root:

```sh
python3 -m unittest discover -s 04-computer-systems/compile-link -v
python3 04-computer-systems/compile-link/run.py
```

Current domain classification remains PARTIAL. These are developed bounded units;
cache coherence, dynamic linking/loader implementation, thread memory ordering,
profiling and broader machine execution remain substantive future instruction.
