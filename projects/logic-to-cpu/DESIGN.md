# Design Proposal

Status: proposal, not implemented or verified.

## Scope and milestones

1. Define finite input/output contracts for selected logic primitives.
2. Compose combinational circuits and arithmetic with an explicit word width and overflow convention.
3. Introduce state with explicit initial values, clock/update semantics and reset behavior.
4. Compose registers and addressable memory with specified bounds and read/write timing.
5. Define a small instruction set and CPU transition rule; run a short hand-traced program.

Do not choose a word width, timing model or instruction encoding by pretending it came from an unread source. Record each as a local design decision or cite the inspected specification. Decide whether to use an upstream educational interface or a separately specified machine before claiming compatibility.

## Acceptance model

For each component, specify input domain, output domain, state, invariants, error behavior and observable transitions before implementation. Exhaustively check small finite domains; test larger components against an independently derived reference model and boundary cases. Preserve differences between predicted and actual behavior.

The initial scope is a digital model. Electrical noise, propagation delay, metastability and physical implementation require separately sourced models and measurements; passing a logical simulation will not verify them.

Open decisions: simulator/language, component interfaces, word width, state-update semantics and instruction set. Resolve after U01–U03 source study, not during setup.
