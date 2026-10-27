# Python functions: local bindings, return values and defaults

The [entry build](../../02-programming/python-entry/README.md) introduces def,
parameters, calls, return and tuple unpacking using a tested byte-budget function.
A function's returned value can be used by tests/other functions; printing a result
instead supplies an I/O effect and ordinarily returns None from print.

Each call binds local parameter names to supplied objects. Rebinding that local
name does not rebind the caller's name; mutating a shared list can still affect
the caller's object. A default expression is evaluated when the function is
defined, so a mutable default list can accumulate across omitted-argument calls.
[The objects unit](units/objects-and-aliases/README.md) records an actual two-call
failure and a defaultNone design creating a fresh list inside each absent-container
call. An explicitly supplied empty list remains intentional; testing `if not
container` would replace it and violate that mutation contract.

Exercise: implement an optional destination list API, state whether it mutates a
supplied destination, and independently test two omitted calls plus an explicit
empty list. [Hints](units/objects-and-aliases/HINTS.md) and
[solutions](units/objects-and-aliases/SOLUTIONS.md) explain the alias reasoning.
Nested scopes, decorators, generators, async and full call binding remain outside
this bounded function introduction.
