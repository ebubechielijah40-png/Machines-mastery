# Reading the tiny C interface

PREPARED; learner NOT STARTED. Unit F-CENTRY. Original explanation and derivation; see [foundation policy](../../README.md).

We need to say what a function may read before asking whether it computes correctly. A C declaration associates a name with a type. In `unsigned int x = 5;`, x names an object initialized to 5 and the type limits permitted operations and values. The declaration alone does not promise that a compiler will reserve a visible stack slot: it may keep a value in a register or remove an unused computation.

A function is a named computation with parameters and a return value. `unsigned int twice(unsigned int x) { return x * 2u; }` receives a value and returns another; braces bound its body, a semicolon ends the return statement, and the suffix u selects an unsigned constant. A call `twice(3u)` gives a copy of 3 to parameter x. There is no loop here. `if (condition) return 0;` exits early when the condition is true. Equality is `==`; assignment is `=`. `||` means logical OR and short-circuits: if its left side is true, the right side is not evaluated.

An array stores a sequence of elements. In `unsigned char p[2] = {18, 52};`, valid indices are 0 and 1. `p[2]` is not a third available element. A pointer value designates an object; a parameter `const unsigned char *p` lets this function read through p without writing those elements through that pointer. It does not prove that p is valid or that two elements exist. The separate length n is a caller promise, not memory introspection. `size_t` is the unsigned type used for object sizes; `<stddef.h>` supplies its declaration. `NULL` represents a null pointer; compare before dereferencing it.

An output parameter `unsigned int *out` points at an existing caller-owned object. `*out = value;` changes that object, unlike assigning a local copy of a numeric argument. The caller must keep the input array and output object alive for the call. Our contract also requires non-overlap. The pointer must satisfy its type's alignment requirements; this is why casting raw bytes to a larger integer pointer is not a portable parser.

Headers declare types and interfaces, while definitions provide behavior. A compiler translates a source file to an object file; a linker connects definitions with uses. A diagnostic or failing assertion is evidence about a particular build, not universal correctness. Wrong: a non-null address proves usable memory. Correct: valid lifetime, extent, alignment and access permission are separate obligations. Transfer: a file's claimed length must be checked against available bytes just as a buffer length must correspond to a real object.

Study [problems](problems/README.md), then [hints](hints/README.md) after an attempt. [Solutions](solutions/README.md) are separate. Complete the [experiment](experiments/README.md) and transfer before returning to the dependent unit.
