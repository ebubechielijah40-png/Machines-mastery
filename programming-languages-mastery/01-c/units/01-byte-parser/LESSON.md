# A parser is an agreement plus a guarded memory operation

[EXPLANATION] Imagine a device report gives two octets, with the first carrying the high part of a nonnegative count. The count 4660 is represented by octets 18 and 52 because 18*256+52=4660. The byte ordering is our local format decision. Nothing about the host CPU chooses that meaning for us.

## Define behavior before implementation

The function receives p, a pointer to input storage; n, the number of available octets claimed by the caller; and out, a pointer to an output unsigned integer. A successful call reads exactly the first two input elements, writes their high-first value, and returns 1. If p or out is null or n is less than two, it returns 0 without changing a valid output object. Extra input is ignored. No internal state persists across calls.

The caller must provide live readable storage for the first two elements on the success path and a live, writable, correctly aligned unsigned-int object for out. Input and output must not overlap. A length check cannot prove these pointer obligations. The byte width is fixed to eight bits by a compile-time requirement, not silently assumed for every C implementation.

```text
caller-owned [high][low] -- checked extent --> base-256 interpretation
                                           --> caller-owned unsigned result
                         failure ----------> return 0, output untouched
```

## Derive the transformation

A base-256 two-place number has a high-place weight of 256 and a low-place weight of one. Let h,l be input octets, each between 0 and 255. Then v=256h+l, so 0≤v≤256*255+255=65535. C's unsigned int supports at least this range; the implementation also checks that contract at compile time. The formula uses unsigned arithmetic to keep the intended domain explicit. The maximum intermediate and result both fit.

A simple table trace for [1,2] is: test pointers/length → read h=1 and l=2 → calculate 256+2 → store 258 → return success. Change only l to 3 and the result increases by one. Change only h to 2 and it increases by 256. An empty input with n=0 follows the failure path before any read. [255,255] reaches the top of the format's range without overflow.

## Why a cast is not a parser

Incorrect sketch, not executed: `*out = *(const unsigned short *)p;`. It attempts to treat the input storage as a different object type. Alignment and permitted-access rules may be violated, unsigned short need not have the desired width, and host byte order may disagree with the format. A cast does not rearrange the bytes or establish an object's lifetime. The corrected design reads unsigned characters separately and combines their numeric values.

Another failure is reading p[1] before checking n. A subsequent error return cannot undo an invalid earlier access. A third is clearing *out before validating: it violates the promised unchanged-on-failure behavior. The invariant at the branch is “no input access or output mutation has happened.” After the successful guard, exactly two reads and one assignment suffice. Their order within the pure arithmetic expression does not matter because no mutation races with them under our contract.

## Source to machine without false stack stories

[SOURCE] The C evidence is the N1570 draft: types and storage duration in 6.2, pointer conversion in 6.3.2.3, expression/access constraints in 6.5, array subscripting in 6.5.2.1 and definitions in 6.9. These establish an abstract-language contract, not a particular stack layout.

[EXPLANATION] In `int x = 5;`, the parser recognizes declaration structure, semantic analysis associates x with int, and initialization establishes its value when that object's lifetime starts. Storage duration differs for block automatic, static and allocated objects. Alignment concerns allowable object addresses; it does not mean every variable must appear in a stack dump. A compiler may replace a computation with an equivalent one preserving required observable behavior. Inspect generated assembly to answer what this build did.

The translation route is source → compiler representation → object code and symbols → linking → executable loading → instructions on the host ISA. An AST is a structured representation of syntax, not a new runtime stack. Object disassembly shows instructions the compiler emitted, but not a complete source-level proof or a benchmark. Our inspection commands expose that boundary; CPU circuitry, caches and OS loading mechanisms are later units.

## Alternatives, limits and a proof

An explicit byte-order library helper can be appropriate if its contract and types fit. memcpy avoids some alignment/aliasing mistakes when copying representations but alone does not impose high-first format meaning. The direct arithmetic solution is short and independent of host ordering under stated byte-width assumptions. It costs constant time and constant extra storage with respect to input length because it accesses only two elements. This is an operation-count statement, not a constant-time cryptographic guarantee.

For valid pointers/extent, the guard selects success and the two reads equal h,l by the input contract. The arithmetic derivation gives exactly the intended value within range, and the single store writes it. On a specified error, early return precedes any read/write, leaving output unchanged. Inputs outside pointer-lifetime/extent/non-overlap obligations are outside the claim; tests cannot make undefined behavior safe.

## Observe and revise

Use exhaustive octet pairs plus sentinel-output error tests. A round-trip with an equally wrong encoder could conceal a shared endian mistake, so expected values are calculated independently and fixed cases are included. Compare -O0 and -O2 behavior; if they differ on valid inputs, investigate assumptions before blaming optimization. Sanitizer success is useful coverage evidence, not a proof of all memory safety. No measured runtime or throughput is supplied.
