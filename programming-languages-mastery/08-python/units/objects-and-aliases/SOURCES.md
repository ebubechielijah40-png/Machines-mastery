# Verified Python sources and limits

Inspected 2026-10-23, Python3.12 documentation (currently rendered as3.12.15).
Local execution used CPython3.12.14, recorded separately. Source excerpts/code
are not copied into this unit; all examples and experiments are original.

| Primary PSF document | Scope actually inspected | Use |
|---|---|---|
| [Data model](https://docs.python.org/3.12/reference/datamodel.html) | §3.1 identity/type/value, mutability, references, garbage collection and explicit resource release | Binding/object and lifetime boundaries; no entire-runtime reconstruction claimed. |
| [copy](https://docs.python.org/3.12/library/copy.html) | Shallow/deep distinction, memo, custom hooks and unsupported resource types | Nested sharing/cycle reasoning and limits of generic copying. |
| [Control-flow tutorial](https://docs.python.org/3.12/tutorial/controlflow.html#default-argument-values) | §4.9.1 definition-time default evaluation | Shared mutable defaults and fresh per-call alternative. |
| [dis](https://docs.python.org/3.12/library/dis.html) | Introduction and get_instructions API/implementation warning | Capture of local bytecode, with no VM/release portability claim. |

Documentation text is PSF License Version2; its examples additionally carry
0BSD as stated by the inspected pages. No source files or substantial passages
are bundled. Runtime bytecode/output is independently observed repository evidence.
Performance, collector timing, C-extension ABI and alternative Python VMs were
not measured or verified in this unit.
