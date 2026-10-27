# Inspected primary source scopes

Inspected2026-10-23. Teaching, packet design, examples, exercises and finite cost
arguments are original. No full source chapter is reproduced.

| Source | Exact inspected scope supporting language facts | Boundary |
| --- | --- | --- |
| Rust project, The Rust Programming Language, online edition, [§4.1](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) | Ownership rules, move/clone distinction and owned buffer motivation | Not whole-book reconstruction; broad stack/heap performance simplifications are not adopted as universal measured claims |
| Rust project, [§4.2 References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html) | Shared/exclusive access, mutation conflicts and references to live values | Our exact rejection output comes from the locally recorded compiler |
| Rust project, [Rust Reference: Destructors](https://doc.rust-lang.org/reference/destructors.html) | Destructor operation and local/struct-field drop order | Not all temporary-expression drop scopes or panic/abort modes |
| Rust standard library [Vec documentation](https://doc.rust-lang.org/std/vec/struct.Vec.html) | Capacity/reallocation and buffer/handle guarantees; inspected version1.99.1 | No exact growth factor, ABI layout or optimizer-output guarantee |

Native compiler1.99.1/commit58cf8f9c3 was downloaded from the official Rust
distribution and checked against its published SHA256 metadata. Only the lab's
own sources and observed command records are distributed here, not the compiler.
The online manuals can evolve; the actual version/flags and compiler diagnostics
in evidence/observed.json are the executed scope. Source availability does not
assign a blanket license to this repository or to all external resources.
