# Rust: one byte buffer, explicit transfer, temporary access

This developed unit is PARTIAL within the wider Rust route. It implements a
bounded safe Rust2021 mechanism and records actual native execution. It does
not complete Rust, unsafe code, async execution, FFI or the standard library.

Before starting, complete [Python aliasing](../../../08-python/units/objects-and-aliases/README.md)
and the [C lifetime bridge](../../../../foundations/programming/c-reading/README.md).
Know values, functions, arrays, conditionals, heap storage, scope and a pointer's
meaning. The code uses no external crate, build script or network service.

## The problem before the rule

A packet arrives as a variable-length sequence of bytes. One function validates
it, another reads it, a worker computes from it, and eventually its storage must
be reclaimed. A raw address alone does not say who may free that storage or
whether another function still reads it. Consider three design choices: require
manual cleanup on every exit, trace reachable objects at runtime, or reject
incompatible ownership/access paths before execution. This lab studies the third
choice and compares it with the earlier C/C++/Python units.

Our invariant is narrower than a slogan about every Rust allocation: each
Packet owns its Vec, the Vec owns its byte allocation, and the safe public API
does not expose another mutable owner of that allocation. Rc/Arc, interior
mutability, unsafe code and deliberate leaks need additional rules; they are not
silently handled by this one diagram of ownership.

## Read the syntax in the implementation

`struct Packet { bytes: Vec<u8> }` defines a type containing an owned byte vector.
`impl Packet` groups its methods. `Self` names that type. `Result<Self, PacketError>`
has two alternatives, `Ok(value)` and `Err(reason)`; `?` propagates the error
alternative, returning from the current function. `enum PacketError` defines the
reasons. `&self` grants shared temporary access, `&mut self` grants exclusive
temporary access, and a plain `self` parameter consumes the value. A returned
`&[u8]` is a slice view, not a new vector. `usize` is used for a size/index;
`u8` is a byte. Iteration, tuples and closures appear only after these roles
have been identified.

Start at [lab.rs](lab.rs), then predict [the compile-fail cases](compile-fail/moved.rs)
before running [run.py](run.py).

## Work through an ownership trace

For `let input = vec![3,4]; let packet = Packet::new(input).unwrap();`, the vector
handle moves into the constructor and then into the successful Packet. The old
binding cannot be used as a vector owner afterward. This is not a deep copy of
the two bytes. The `consume_returns_allocation` test compares the buffer address
before and after transfer while the allocation remains live. It does not infer
an exact stack layout or inspect freed memory.

The constructor accepts lengths1..4096. On an error the already supplied Vec
is dropped; the API does not return it to the caller. The input Vec was allocated
before the call, so a length bound here does not bound caller-side allocation
or turn allocation failure into a recoverable PacketError.

Now borrow `let first = packet.view();`. No bytes are copied. A second shared view
can inspect the same bytes. While either view remains needed, safe code may not
call a method requiring `&mut packet`. The active view and a vector growth could
otherwise disagree about where the allocation lives. A view's last use can occur
before the end of its enclosing block; the successful test reads both views,
then calls `set`. The failing overlap program instead prints the view after a
push, requiring the incompatible accesses to overlap. Its rejection is actual
compiler evidence, not pseudocode output.

`set(2,8)` on two bytes returns BadIndex before mutation. Its result and unchanged
buffer are checked separately. A valid `set(0,7)` changes the owned bytes; any
later fresh view observes that state. The type system does not decide whether7
is a meaningful sensor value. Representation safety and domain truth differ.

## Clone, copy, destruction and threads

`Packet` derives Clone. Cloning this Vec duplicates its bytes; editing the clone
does not change the source. For n bytes, the copy needs O(n) time and additional
O(n) byte storage. A slice borrow needs only a view and O(1) setup, but it cannot
outlive its permitted access interval. Integer Copy values can be duplicated
without transferring an allocation; a Vec does not acquire Copy just because
its handle has a fixed size.

The drop tests deliberately distinguish two orders: local variables drop in
reverse declaration order, while fields of this Group drop in declaration order.
The trace uses Rc<RefCell<_>> only in a single thread. RefCell checks its dynamic
borrow rules at runtime; it is not a replacement for this Packet's static borrow
contract, nor is Rc a cross-thread shared counter.

`thread::spawn(move || p.into_bytes())` transfers the Packet into the closure.
The worker returns its Vec through JoinHandle. Joining recovers the result after
worker completion; a panic would be a different Result path. Send requirements
are checked by the compiler. No unprotected shared mutable packet exists in this
example, so a mutex is unnecessary for this particular transfer. A shared server
cache needs a separate design; moving one packet is not a server architecture.

## Derive cost and identify failure

The view contract permits O(1) setup because it creates no duplicate byte buffer.
Cloning n bytes must inspect/copy n bytes in this representation. A Vec push can
reallocate when capacity is insufficient, so the experiment records capacity
transitions instead of assuming that every push has the same cost. The precise
growth factor and emitted instructions are compiler/library observations, not
stable Rust ABI promises. Allocation, copying, serialization and cross-thread
scheduling are different costs and must be measured separately.

Three deliberate bad programs test different defects: use after move, mutation
while an old shared view remains live, and return of a reference into a destroyed
local String. Their checked diagnostics are E0382, E0502 and E0515 on the recorded
compiler. A compiler rejection does not prove every runtime algorithm correct;
the valid code still needs tests for length, indexing, outputs and cleanup.

## Build and investigate

```sh
rustc --version
python3 programming-languages-mastery/03-rust/units/ownership-transfer/run.py
```

Run from the repository root. RUSTC or --compiler can identify a trusted local
rustc. The driver builds the8 tests in debug and optimized modes, checks the
three expected rejection codes, and runs the ownership/capacity experiment. It
uses temporary output directories and no Cargo dependency resolution. Missing
rustc returns BLOCKED with exit2, not a passing native test.

Read [the actual experiment](EXPERIMENTS.md), attempt [the tasks](EXERCISES.md),
then consult [hints](HINTS.md) and [solutions](SOLUTIONS.md). Close the source and
rebuild a bounded owner/view/mutator/consumer with an independent boundary test.
Transfer the reasoning to C++ RAII, Python aliases and Go slices: the same byte
values can be stored under very different ownership/access policies.
