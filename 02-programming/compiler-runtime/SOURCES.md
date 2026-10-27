# Exact primary scopes and original work

Inspected2026-10-25. The grammar, code, proof sketches, examples, finite oracles,
experiments and assessments here are original repository work. No complete book,
specification text or proprietary source is bundled. Public access does not
establish permission to redistribute a complete work. Consult original terms;
no blanket third-party license is assigned.

| Primary source / responsible publisher | Version and inspected locator | Claim boundary |
| --- | --- | --- |
| Oracle, *Java Virtual Machine Specification* | JavaSE24, [§4.9.2](https://docs.oracle.com/javase/specs/jvms/se24/html/jvms-4.html#jvms-4.9.2), selected stack/initialization constraints; [§4.10.2.1–2](https://docs.oracle.com/javase/specs/jvms/se24/html/jvms-4.html#jvms-4.10.2), worklist/merge description | Motivates structural/dataflow comparison. Flow is a different single-type machine, not Java class verification. No entire chapter reconstruction claimed. |
| Python Software Foundation, Python language reference | Live3.12 documentation identified3.12.15; [§6.7 binary arithmetic](https://docs.python.org/3.12/reference/expressions.html#binary-arithmetic-operations), selected division paragraph | Python floor division differs from Flow's original toward-zero rule. No claim that Python's full semantics are implemented. |
| Python Software Foundation, `dis` documentation | [Python3.12 `dis`](https://docs.python.org/3.12/library/dis.html), introductory implementation/version caveat, `get_instructions` and disassembly use | Host opcode inspection is CPython-specific. Actual runtime/opnames are recorded rather than promised across releases. |

Mechanism map: `_tokens`/`_Compiler` implement the declared original grammar;
`verify` implements the stated finite stack/init abstraction; `Machine` and
Snapshot define the original operational/fault contract. The counted-loop cost,
signed quotient derivation and worklist-termination argument are original
derivations with assumptions stated in README. Tests check selected instances;
they are not external validation of the implementation or a proof for all code.
