# C++: one resource, object lifetime, copying and moving

Prerequisites: [representations and proofs](../../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
C-style functions, pointers and arrays from the [C reading bridge](../../../../foundations/programming/c-reading/README.md).
The C++ syntax slice below introduces the references, constructors and exceptions
used by this particular build. The
[compile/link route](../../../../04-computer-systems/compile-link/README.md) connects
source-level ownership to object files and symbols. This is a bounded C++17
mechanism unit, not completion of the entire C++ language or ABI route.

## Read the C++ syntax used by this build

A `class` groups state fields and operations for an object. Its members are
private until a `public:` section exposes an interface; a `struct` begins public.
The trailing semicolon closes a class definition. `Buffer a(2)` constructs an
object named a by selecting a constructor named `Buffer`; a constructor has no
written return type. Its `: size_(size), ...` list initializes member fields
before the body. Actual field initialization follows declaration order, so do
not infer a different lifetime order merely by rearranging the written list.

`~Buffer()` is its destructor, invoked when a completed object's lifetime ends.
`a.at(0)` calls a member on a; inside that member, fields refer to that object.
`this` is its pointer and `*this` the object. `std::size_t` is the standard
unsigned size type; `nullptr` is the null-pointer literal. `new int[n]{}`
creates a dynamically allocated zero-initialized integer array, paired here
with `delete[]`, not scalar `delete`. A missing release on a path is a program
obligation, not an automatic property of using C++.

An `int&` is a reference to an existing integer, so assigning through the return
of `at` changes that stored element. `const Buffer&` permits observing an existing
Buffer without copying it or modifying it through that reference. `Buffer&&`
marks a different overload used for an eligible expiring/moved expression;
it does not itself move storage. The selected constructor must implement transfer.
`Buffer b=a` calls this class's copy constructor; `Buffer c=std::move(b)` selects
its move constructor. Both are derived from the ownership invariant below.

`throw std::out_of_range(...)` reports an exception rather than returning an
integer sentinel. A surrounding `try`/matching `catch` handles it. Completed
automatic objects between throw and handler are destroyed during unwinding;
the experiment checks a concrete nested cleanup order. `noexcept` declares
an operation that must not let an exception escape; violating it terminates the
program. It is not a guarantee that arbitrary work outside that operation's
body, such as constructing a by-value argument, cannot fail.

Before continuing, point to constructor, destructor, reference result, copy,
move and catch in [the actual source](resource.cpp). These syntax definitions
support this bounded mechanism; templates, overload resolution in general and
the full C++ object model remain further study.

## Why tie a resource to an object?

A raw allocation creates two obligations: know who may access its storage and
release it exactly once after the last permitted use. Writing a delete on only
the ordinary return path misses an exception/early return. RAII makes a completed
object's destructor responsible for release when its lifetime ends. The same
idea applies to file handles and locks, but this lab owns an integer array so the
state is inspectable. Destruction ends an object's resource obligation; it does
not make outstanding references to released storage safe.

[resource.cpp](resource.cpp) defines Buffer with state `(size_,data_,id_)`.
Invariant: a nonempty Buffer uniquely owns one allocation of size_ initialized
integers; an empty Buffer has size0 and null data. id_ traces the allocation,
not a stable memory address or language identity. No raw owning pointer escapes.
Bounds-checked at(i) rejects i≥size. Audit is fixed-capacity nonallocating test
instrumentation, not a production allocator or complete heap-leak detector.

## Derive each operation from the invariant

Construction allocates and zero-initializes storage before a usable Buffer exists.
A failed `new[]` does not produce a completed Buffer requiring its own destructor.
Destruction uses matching `delete[]`, decrements the live counter and records its
resource ID. It is noexcept; cleanup must not introduce another propagating error.
Nested completed local objects in this example clean up during ordinary scope exit
or the controlled exception. The actual trace verifies reverse release order.

A default pointer-value copy would make two independent owners of the same
allocation, so both destructors could release it. Our copy constructor allocates
an independent array and copies integer elements. With a.at(0)=7, `Buffer b=a`
and b.at(0)=9 leave a's7 unchanged. Copy time is O(n), storage O(n). This is value
copying by an explicit class contract, unlike Python assignment binding aliases.

The move constructor transfers pointer/size/ID and sets the source to empty.
It allocates nothing and performs a constant number of scalar operations. The
source remains safely destructible and bounds checking rejects access to its now
empty data. `std::move(b)` makes b eligible for a move overload; the Buffer
constructor performs the transfer. Applying std::move to a raw pointer would not
magically enforce unique ownership or null the original pointer.

Assignment receives a Buffer **by value**, then swaps all three state fields.
Copying an lvalue constructs the parameter before the existing target changes;
if allocation fails there, the target is unchanged. Moving an rvalue constructs
the parameter by transfer. Swap is nonthrowing. After swapping, the parameter's
destructor releases the target's previous resource. This derives copy-and-swap's
strong assignment behavior here; no injected allocation-failure test has been run.
The function's noexcept body does not promise that copying its argument cannot
throw before entry. Self-copy is safe; self-move in this particular implementation
moves into the parameter then swaps the resource back. That is a class-specific
contract, not a universal claim about all moved-from library objects.

## Execute and explain actual evidence

From repository root:

```sh
python3 programming-languages-mastery/02-cpp/units/resource-lifetime/run.py
```

The runner builds isolated temporary executables with g++ and C++17, warnings as
errors, then runs assertions at O0, O2 and O1 with undefined-behavior sanitizer.
[observed.json](observed.json) retains g++13.3.0, environment, exact flags, build/run
exit0 and actual stdout for all three configurations. It reports independent
copy values, empty moved source, self-assignment, reverse exception cleanup and
live allocation counter0. UBSan produced no diagnostics on these executed paths;
this is not proof of all possible C++ memory safety or a separate leak check.
Assertions must remain enabled; compiling with NDEBUG would remove these gates.

Question: does exception exit preserve the same ownership invariant as normal
exit? Controlled input is a runtime_error after constructing one then two. The
measured release log is two then one and live count returns0. The hypothesis is
supported for this local path. Alternative missing paths include constructor
allocation failure, unrelated exception types and external mutable aliases. Add
an allocator failpoint as the next experiment; do not claim its result in advance.

## Engineering transfer

A borrow from at() remains valid only while the owning allocation remains alive;
a later assignment can destroy that allocation and dangle the reference. Bounds
checks cannot detect that use-after-lifetime. Buffer is not synchronized across
threads. Repeated copies can be expensive; moves avoid data duplication but do
not solve shared ownership. For application code prefer standard owners such as
vector/unique_ptr and compose their invariants; manually implementing an owner
here exposes the mechanism that those abstractions provide.

Attempt [EXERCISES](EXERCISES.md) before [HINTS](HINTS.md) and
[SOLUTIONS](SOLUTIONS.md). [SOURCES](SOURCES.md) precisely limits the inspected
standard-draft evidence and selected compiler validation.
