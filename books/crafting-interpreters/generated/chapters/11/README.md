# From a moving name to a fixed binding

A program can parse correctly, run without a memory fault, and still execute the
wrong language. The problem in this unit is precise: a closure should keep using
the same lexical binding even when a later declaration adds a name to a captured
frame. Resolving a name by searching mutable dictionaries at every call can
silently change which variable is read. We will reproduce that failure, derive
a static address, then test shared mutation and recursion.

This is an original companion to Nystrom's chapter11 and selected chapter10
closure mechanics. Read [source scope](../../SOURCE_INDEX.md) and
[prerequisites](../../PREREQUISITES.md). Our runnable language starts at an AST;
it has no lexer/parser, classes, bytecode, machine code, file/network access or
native callbacks. The earlier expression-language project teaches parsing.

## Binding is a relationship

A **name** is an identifier such as`label`. A **declaration** introduces a place
for that name in a scope. A **binding** relates a particular use in the program
to the place it should access. A **value** is the current content of that place.
Binding and value can change independently: assignment changes a value while
preserving the binding; shadowing introduces a different place with the same name.

A **lexical scope** is determined by program structure and declaration order.
A **frame** is a runtime object holding values for one activation of a scope.
Two calls to the same function share one body of source/AST but create different
parameter/local frames. A **closure** is a function body paired with the frame
where that function was declared. A later call starts a new frame whose parent
is that captured frame. It does not use the caller's locals as its lexical parent.

The core invariant is: for each resolved local occurrence, the scope relation
computed from the AST must match the frame relation created at runtime. A block
adds one scope during resolution and one frame during execution. A function
body adds one scope during resolution and one call frame during invocation.
Adding an extra runtime frame only on one side breaks every deeper address.

## The failure to reproduce

The following is illustrative source notation, **not** the lab's accepted input:

```text
let label = "catalog";
{
    function read() { print label; }
    read();
    let label = "local";
    read();
}
```

The local`label`declaration follows the function's body in the enclosing block.
Its binding therefore must not capture the function's earlier name occurrence.
Both calls should produce`catalog`. Here is the complete runtime trace of the
wrong mutable-chain algorithm:

| Event | Frames or action | What changes |
| --- | --- | --- |
| Global declaration | G contains label→catalog | Global slot exists |
| Enter block | B.parent=G | New local frame |
| Declare read | Closure C=(body,B), B contains read→C | Body is saved, not run |
| First call | F1.parent=B; lookup walks F1→B→G | Finds catalog in G |
| Later declaration | Add label→local to the same B | C still points at B |
| Second call | F2.parent=B; lookup walks F2→B | Stops early and finds local |

Nothing assigned to the original global slot. The algorithm changed the lookup
**target**, so this is a binding defect rather than an ordinary changing value.
Freezing all captured values would also be wrong for languages where closures
intentionally share mutable cells. We need stable binding with mutable contents.

Our AST builder for the example is`late_declaration()`in the test file. To inspect
the repaired result directly from the repository root:

```sh
python3 -m unittest discover -s books/crafting-interpreters/generated/chapters/11/code -v
python3 books/crafting-interpreters/generated/chapters/11/code/experiment.py
```

The intentional`lookup='mutable-chain'`mode is a negative control. It reproduces
the wrong output; it is not an alternative correct implementation of this language.

## Derive the resolver

Before evaluation, walk the tree in source order with a stack of local scopes.
Each scope maps names to a two-state declaration marker:

1. **Declared, unavailable**: the binding shadows an outer binding, but its
   initializer has not yet been resolved.
2. **Defined, available**: references may resolve to that binding.

For a local`let x = initializer`, add`x→False`, resolve the initializer, then set
`x→True`. A direct read or assignment to that unavailable local is a static
error in our language. We deliberately reject assignment too; the book's main
shown check is for reading. We do not quietly guess an initial zero/None.
A second declaration in the same local scope is a static error. A nested scope
can shadow the same spelling because it introduces a new place.

For a name occurrence, search the resolver stack from inside outward. If the
matching scope has index j and the innermost index is s−1, record

\[
  d=(s-1)-j.
\]

This distance is0 for the current frame,1 for its parent, and so on. At runtime,
follow exactly d parent pointers, then access that frame's named slot. Do not
stop at an earlier frame just because a later declaration inserted the name there.

Example: a block defines`x=2`; its nested block prints x. At resolution the stack
is`[{x:True},{}]`. The occurrence has d=1. Runtime frames are G→B1→B2; printing
from B2 follows one link to B1 and gets2. Adding a function body between them adds
one resolution scope and one call frame, increasing d by one on both sides.

Globals are a deliberate language-specific exception. We mark an unresolved local
occurrence as a **global slot** and later consult G directly. A function may be
declared before a global's initializer executes, and global redeclaration updates
that slot. Calling too early raises a runtime undefined-name error. This is not
a claim that all languages resolve globals the same way. It also means that
stable local binding does not imply immutable global values or forbidden redeclaration.

Function declarations bind their own name before their body is resolved. That
permits self-recursion. Resolving the body traverses it immediately without
executing it, including both branches of every`If`. Calling the function later
executes only the selected branch. A statically invalid unused branch is still
rejected before any top-level statement runs. The resolver tracks whether it is
inside a function so that top-level return is rejected as well.

## Capturing a cell is not copying a value

Construct a factory whose call frame contains n=0 and a nested`next`function:

```text
function make() {
    let n = 0;
    function next() { n = n + 1; return n; }
    return next;
}
let a = make();
let b = make();
print a(); print a(); print b(); print a();
```

The first factory call creates frame A, the second frame B. The two functions
capture different frames, so the output is1,2,1,3. Calls through a share A.n;
calls through b use B.n. Returning from`make`does not make the captured frame
unreachable: the returned closure still refers to it. Python's own memory manager
keeps these host objects alive; our lab does not implement a tracing collector.

If a closure copied n=0 into a fresh private slot on every call, a would return1
forever. If both factory calls reused one global n, b would interfere with a.
Both wrong implementations can pass a single one-call example. The interleaved
trace separates lifetime, sharing and instance identity in one bounded test.

## What the implementation actually contains

[The source](code/binding_lab.py) uses immutable, identity-distinct AST nodes and
a read-only address table. Nodes with the same name/text remain different uses:
`Name('x')`at distance0 must not overwrite another occurrence at distance2.
To avoid contextual address ambiguity, a shared AST object reused in two tree
positions is rejected. A program is a tuple of statements; mutable body/argument
lists, invalid names, out-of-grammar nodes and oversized/deep trees are rejected.

Runtime frames contain mutable value dictionaries. A closure retains the body
and its declaration frame. Calling evaluates the callee and arguments from left
to right, validates arity, creates a parameter frame, executes the body and catches
a private return signal. No explicit return yields None. Primitive operations
support integer addition/subtraction and type-sensitive equality. Booleans are
not integer arithmetic operands in this language even though Python subclasses
bool from int. Conditions require actual Booleans.

The static pass has no execution or output side effects. For n nodes and maximum
lexical depth h, the simple stack search costs O(nh) in the worst case; visiting
each node once does not make name lookup free. A hash-map/stack-of-declarations
resolver could improve lookup, and a slot-index compiler could remove repeated
string lookup at runtime. Our fixed-hop read costs O(d), plus dictionary access;
we do not claim a constant-time display or compiled local-slot implementation.

## Failures, engineering limits and reconstruction

The runner limits the AST to2000 nodes/depth80, parameters/arguments to32,
identifiers to64 characters, text literals to1000 characters, integer magnitudes
to4096 bits, steps to100000 and call depth to64. These teaching bounds reduce
accidental runaway work. They are not a hostile-code sandbox, memory quota,
proof of host-recursion safety for every configuration, or deployment policy.
A caught host RecursionError becomes a controlled ExecutionError and may reject
a deeply nested recursive expression before its explicit call bound.
No parser accepts user source strings. Error stops are not transactions: prior
runtime assignments/output are not rolled back.

A missing runtime global, wrong arity, nonfunction callee, invalid arithmetic,
non-Boolean condition or exhausted execution budget raises ExecutionError.
Static duplicate declarations, own-initializer access, top-level return and
malformed ASTs raise BindingError. Different types make debugging layers visible.

Build in milestones: first frames and primitive evaluation; then blocks and
functions; reproduce the mutable-chain failure; add the resolver's declare/define
states; connect fixed-hop reads **and assignments**; add semantic errors and
resource bounds; finally run the shared-mutation/recursion/oracle tests. Score
correctness by predictions and independently observable traces, not merely by
copying the reference's classes. Complete [the exercises](EXERCISES.md), keep
[hints](HINTS.md)/[solutions](SOLUTIONS.md) closed initially, then perform the
reconstruction challenge. [The experiment record](EXPERIMENTS.md) separates
actual observations from predictions and limits. The whole book remains incomplete.
