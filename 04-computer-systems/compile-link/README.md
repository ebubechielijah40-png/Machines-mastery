# From two C files to a running process

This original unit develops separate compilation, symbol resolution, relocation,
calling interfaces and object lifetime. It is a **STRONG bounded investigation**,
not a full compiler/loader course. Read the [byte-parser C lesson](../../programming-languages-mastery/01-c/units/01-byte-parser/LESSON.md)
for pointer/length contracts, and [finite representations](../../foundations/mathematics/finite-representations/README.md)
for byte/address arithmetic first. The [source record](SOURCES.md) states exactly
which specifications were inspected and which were inaccessible.

## 1. The problem that a compiler alone cannot solve

Imagine separate people implementing a caller and a byte-processing routine.
Recompiling every dependency into one source file would couple their work and
hide interface mistakes. We want each part to compile independently, then combine
compatible definitions into one program. A declaration supplies a contract to
the compiler. It does not supply executable code to the linker.

The runnable example has three distinct artifacts:

- `sum.h` declares `sum_bytes`, `affine` and the external counter.
- `main.c` uses those declarations to compile calls and data references.
- `sum.c` supplies the definitions and storage.

For inputs `{3,5,7}`, `sum_bytes` must publish 15. Initially `output=999`; an invalid
pointer/length combination must return false without replacing it. This is a
small example of **failure atomicity**: error reporting should not quietly expose
an intermediate answer as a successful result.

This example is single-threaded. `successful_calls` is a non-atomic global
read-modify-write counter. Concurrent unsynchronized calls or reads would create
a C data race and undefined behavior; a successful O0/O2 test supplies no thread-
safety guarantee. Protect the full counter operation with a synchronization
contract or use an appropriate atomic operation before introducing concurrency.
The [synchronization unit](../../05-operating-systems/synchronization/README.md)
develops that distinction using defined atomic accesses and a separate model.

The two translation units are not two running processes. They are independently
compiled pieces later combined into one process image. A process, in contrast,
has execution state, mappings and OS-managed resources. The [OS unit](../../05-operating-systems/SELF_CONTAINED_GUIDE.md)
continues from the compiled program to that distinction.

## 2. Four transformations and their evidence

GCC documents preprocessing, compilation, assembly and linking in that order
[S-COMPILER]. Our investigation controls the boundaries:

| Operation | Input → output | What the output still lacks |
| --- | --- | --- |
| Preprocess `cc -E main.c` | Source/header directives → expanded C | Machine instructions and object format |
| Compile `cc -S main.c` | Translation unit → assembler text | Encoded machine bytes and final addresses |
| Assemble via `cc -c main.c` | Translation unit through assembly → relocatable object | Definitions/addresses owned by other units |
| Link `cc main.o sum.o` | Relocatable pieces/runtime inputs → executable | A running address space; the OS/runtime still has loading work |

A `.o` is not merely raw instruction bytes. It includes organized sections,
symbol information and records describing references that need adjustment. The
exact format is platform dependent. We inspect ELF-format output on the recorded
Linux machine; that observation is not a universal claim about Windows PE or
macOS Mach-O. The ELF specification endpoint was blocked, so no fresh formal ELF
compliance claim is made.

Our `run.py` stores the actual command, exit status, stdout and stderr for every
step. Builds use a temporary directory; no generated executable is checked in.
The observed compiler was GCC 13.3.0. A future run can differ; use its recorded
version rather than copying a version number into a new report.

## 3. Undefined symbols are unfinished references, not necessarily bugs

`nm -P main.o` showed `sum_bytes U`, `affine U` and `successful_calls U`. `U`
means undefined in that object [S-NM]. The compiler knows their declared types,
but their definitions are elsewhere. `main T ...` identifies code defined in
this object. It is therefore normal for an intermediate object to contain
undefined references.

Linking only `main.o` deliberately failed. Adding `sum.o` supplied the owned
routine/counter definitions; the compiler driver also selected runtime/library
inputs needed by `printf`. A header does not resolve that failure because the
header contains declarations, not those function definitions. A second definition
with the same strong external name would create a different link error; silently
renaming it changes which program is being built rather than fixing the original
interface argument.

**Worked trace:** the compiler emits a call site for `sum_bytes`. The object
contains a reference named by a symbol; `readelf -Wr main.o` shows relocation
entries and `objdump -dr main.o` places them beside instructions. At link time,
the definition selected for that name supplies an address. The relevant
machine field is adjusted according to the target's relocation rule. Do not
hand-edit a displacement by guessing that every relocation is simply an absolute
address: PC-relative references, instruction encodings, dynamic linkage and
addends require different rules. Our evidence exposes those records but does not
reimplement an ELF linker.

The observed x86-64 objects include `R_X86_64_PLT32` entries for calls and
`R_X86_64_PC32` entries for data/string references. The names are observations
from this compiler/target, not an inspected psABI definition. The attempted
formal ABI PDF was unavailable. A follow-up linker implementation requires that
specification before claiming to implement these encodings.

## 4. The calling interface has machine consequences

C says `affine(4,5)` computes 17, within our no-overflow precondition. How does a
caller convey 4 and 5, and how does it recover 17? Both pieces must agree on
argument representation/location, return value location, stack obligations and
which machine state a callee preserves. This agreement is a calling convention,
part of an application binary interface (ABI). A function type in one compiler
invocation cannot repair a binary built under an incompatible convention.

The recorded `-O2` disassembly for `affine` was:

```text
lea (%rdi,%rdi,2),%rax
add %rsi,%rax
ret
```

The log also retains a preceding `endbr64` instruction; the excerpt above isolates
the arithmetic. In this execution, the first input participates through `rdi`,
the second through `rsi`, and the result through `rax`. `lea` calculates
`x+2*x` as integer address-style arithmetic without loading memory at that
computed address. Seeing the word “address” does not mean it dereferences a
pointer. `add` then contributes y. The routine can return without creating the
stack frame one might draw from an unoptimized source-level explanation.

At `-O0`, the compiler emitted a different sequence with more intermediate
storage. Both executables produced `sum=15 calls=1 affine=17`. Equal outputs
for these inputs support semantic agreement, not equality of speed, code layout
or all possible behavior. The tests compare against `x+x+x+y` over a bounded
integer grid. They avoid signed-overflow inputs, which would violate the C
function's precondition and invalidate a naive optimization comparison.

An ABI has more rules than these two registers: widths/signedness, aggregate
arguments, floating-point arguments, variadic calls, stack alignment, unwind
metadata and preserved registers matter. They are explicit remaining study,
not inferred from one leaf function.

## 5. Objects, lifetimes and the byte boundary

`sample` in `main` is an array with automatic storage duration; its lifetime
continues until that invocation of `main` leaves its block. Passing a pointer to
its first byte does not copy the bytes or extend the lifetime. `length` states
how many bytes the callee may inspect. The compiler cannot recover that bound
from a plain pointer. `output` is a separate live `uint64_t` object which the
callee writes only after completing the read/check loop.

`successful_calls` has static storage duration and external linkage. These are
different axes: duration concerns when storage exists, while linkage concerns
which declarations name the same entity across translation units. A block-local
variable can have static duration; an external declaration does not itself make
an arbitrary pointer safe. `nm`'s object-section classification is useful
implementation evidence, not a complete statement of C lifetime semantics.

A null data pointer with length zero is supported because the loop reads no
bytes; a null data pointer with nonzero length is rejected before any read.
An out-of-bounds nonnull pointer is not automatically detected. The caller
still must supply a readable region of at least `length` bytes. A pointer to a
returned function-local array would violate that rule even if its numeric address
looked familiar. An arbitrary address printed by a program is not authority to
read or write that address.

The output object must be writable and correctly aligned. Pointer arithmetic
within an array advances by its element size; a byte pointer advances one byte,
while a `uint64_t*` advances by `sizeof(uint64_t)`. Confusing those units makes
memory accounting and bounds checks wrong before any allocator is involved.
The [arena project](../../projects-guided/p04-memory-allocator/README.md) continues
this story using a concrete bounded byte region.

## 6. Tests, errors and debugging sequence

Run from repository root with Python 3.10+ and a C11 compiler. GNU `nm`, `objdump`
and `readelf` supply additional observations if present:

```sh
python3 -m unittest discover -s 04-computer-systems/compile-link -v
python3 04-computer-systems/compile-link/run.py
```

The script compiles/runs at O0 and O2, requires the deliberate missing-definition
link to fail, and runs C assertions at O1 with undefined-behavior sanitization.
A sanitizer passing safe inputs is not proof that every invalid pointer/lifetime
case is detected. Missing compiler tools are a genuine execution blocker; do not
replace their output with the expected assembly excerpt.

When a build fails, determine the stage before changing code:

1. A preprocessor error often concerns an unavailable include or malformed
   directive. Verify the exact include path and spelling.
2. A compiler diagnostic concerns syntax/types/constraints within the translated
   unit. Preserve the first diagnostic rather than guessing from its cascade.
3. An undefined-reference link failure concerns definition selection/object
   inputs or incompatible names. Inspect the object symbol tables.
4. A running program with wrong output requires tracing actual values, bounds,
   lifetime and state. It is not automatically a linker problem.
5. Only after correctness is established compare code size/performance under
   a declared workload. This investigation does not time the executable.

## 7. Controlled experiment and observed interpretation

**Question:** does compiling a caller establish a complete executable, and do
optimization levels have to preserve the same instruction sequence?
**Predictions:** caller-only compilation succeeds but linking fails; linking
both owned objects runs; O0 and O2 can differ while producing the same bounded
outputs. **Controls:** same owned sources, C11 mode, warning flags and target
machine. **Independent variables:** supplied object files, then optimization.
**Instrumentation:** exit status, symbols, relocation records, disassembly and
exact output. **Procedure:** run the script; retain every record, including failed
links. [Actual evidence](evidence/observed.json) contains those observations.

The observed link failures support missing-definition diagnosis. Successful
bounded tests do not establish a compiler proof, ABI conformance, absence of
undefined behavior for all inputs or a performance improvement. Different
compiler defaults, hardening flags and target architecture could explain a
changed listing. Next, change a definition's visibility and inspect whether a
symbol remains externally resolvable; predict before compiling.

Attempt [the exercises](EXERCISES.md), use [hints](HINTS.md) after an attempt,
then compare [solutions](SOLUTIONS.md). Reconstruct the two-unit build from
memory before progressing to OS scheduling/address spaces.
