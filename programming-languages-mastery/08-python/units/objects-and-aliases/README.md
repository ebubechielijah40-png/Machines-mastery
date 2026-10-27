# Python: bindings, object graphs, mutation and lifetime

A name is a binding to an object. Assignment changes bindings; it does not by
itself copy the object. This distinction explains a large class of apparently
mysterious data contamination and is needed before the interpreter's copied
environment can be understood. Prerequisites are functions, lists, indexing and
[finite state/proof reasoning](../../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md).
No C pointer arithmetic is required. [Source map](SOURCES.md) separates Python
language rules from CPython implementation observations.

## Start with the concrete failure

```python
a = [[1], [2]]
b = a
c = a.copy()
d = copy.deepcopy(a)  # with import copy
b[0].append(9)
```

Draw the object graph before running. a and b point to the same outer list. c
points to a different outer list whose two child references initially point to
the **same inner lists** as a. d points to a separately copied structure for this
example. b[0] follows the shared outer reference, then the first child; append
changes that child list. Therefore a, b and c observe `[1,9]` in their first
position, while d still contains `[1]`. It is the path to a shared mutable object,
not similarity of variable spelling, that predicts the effect.

Identity asks whether two references designate the same object (`is`). Equality
asks whether their values compare equal (`==`), under type-defined behavior.
Two freshly created empty lists compare equal but are distinct objects. Do not
use identity to compare numeric/string values or rely on interning experiments.
The tests assert semantic relationships, never hard-coded id() addresses.

## Copying follows graph structure

A shallow copy creates a new outer collection and reuses references to children.
It isolates adding/removing/replacing that outer list's entries, but does not
isolate mutation inside a shared child. For a flat list of immutable integers,
a shallow copy is often enough; for a nested mutable structure it may not be.
This is why `dict.copy()` isolates rebinding names to immutable Fractions in
[the interpreter project](../../../../projects-guided/p10-language/README.md),
while a copied dictionary of mutable lists would not roll back inner mutations.

Deep copy recursively copies supported objects using a memo map. If two original
paths lead to one child, the copied paths can lead to one copied child, preserving
the sharing relationship instead of inventing two children. For `x=[]; x.append(x)`,
naive recursion never ends. A memo records the new container before descending,
so the copied self-reference can point back to it. The cycle test checks this.
Custom classes can define copying behavior, and resources such as files/sockets
are not generically cloned by deepcopy. Copying everything is not a substitute
for designing ownership or understanding resource lifetime.

## Rebinding and augmented assignment are different operations

For list x=[1] and y=x, `x=x+[2]` computes a new list and rebinds x; y still points
to `[1]`. For the same initial state, `x += [2]` asks the list's in-place addition
operation to extend the existing list, then binds the result to x. y sees `[1,2]`.
Do not generalize that every `+=` mutates every object: numbers are immutable,
and custom objects define their own operation behavior. Predict from operand
semantics, not from an operator character alone.

An immutable tuple fixes the identities of its immediate children, not all
objects reachable from them. `t=([1],); t[0].append(2)` succeeds because the tuple
still points to the same list. Replacing t[0] is forbidden. Immutability of an
outer container and absence of mutable reachable state are different properties.

## Function defaults and explicit resource lifetime

A default argument expression is evaluated when the function is defined. If that
object is a list, later omitted-argument calls share it. The experiment defines
an intentionally accumulating local function: after calls with'a' and'b', both
results reference `['a','b']`. [model.py](model.py) instead uses defaultNone, creates
a fresh list inside each omitted-argument call, and mutates a supplied container
only when the caller deliberately provides one. If None itself must be a valid
value, introduce a unique sentinel with a documented contract.

Deleting/rebinding a name can make an object unreachable, but other aliases or
cycles may still retain it. Python does not guarantee immediate finalization.
CPython's reference counting is an implementation choice with additional cycle
handling; it is not a portable resource-release contract. Use explicit close or
a context manager for external resources. This lab does not measure collector
scheduling or implement the collector.

## Execute, measure meaning, then transfer

From repository root:

```sh
python3 -m unittest discover -s programming-languages-mastery/08-python/units/objects-and-aliases -v
python3 programming-languages-mastery/08-python/units/objects-and-aliases/experiment.py
```

[Six passing methods](tests.txt) cover nested copies, tuple child mutation,
rebind/augmentation, independent defaults, cycle copying and equality/identity.
The question in [observed.json](observed.json) is whether changing the copy or
assignment operation changes visible state while original nested input is held
fixed. Actual CPython3.12.14 observations match the traces above. It also captures
local bytecode: both functions use BINARY_OP, with argument `+` versus `+=`.
That disassembly is an implementation observation, not a portable Python ABI or
proof that every operation has the same CPU cost. No timing/RSS claim is made.

Sharing explains these results better than imagined hidden value copies. Other
class-specific methods could give different copying/in-place behavior, so repeat
with a class whose contract you define before claiming universality. Next measure
flat versus nested copy cost with fixed shapes and separate time/memory metrics.
For engineering, document whether an API borrows, mutates, shallow-copies or
owns data; use independent immutable snapshots for cross-task state when possible.

Attempt [EXERCISES](EXERCISES.md), then [HINTS](HINTS.md) and
[SOLUTIONS](SOLUTIONS.md). This is a developed object-model unit; packaging,
async, extension ABI, runtime implementation and the rest of Python remain separate.
