# Attempt before opening solutions

1. List the eight full-adder inputs. For each, check a+b+c=s+2d.
2. Derive the ripple invariant after k columns. Why is the final sum modulo256?
3. Give one unsigned carry without signed overflow and one signed overflow
   without unsigned carry. Use exact eight-bit patterns.
4. Encode LDA13, ADD14, STA13 and JMP2. Decode0x6a without running Python.
5. Hand-trace the six-instruction example, including PC, carry and writes.
6. Prove multiplication's invariant and derive its exact cycle count. Which
   assumption fails if the initial counter is0?
7. Change the multiplication program's JMP target from2 to0. Predict whether it
   halts and its result for3×4. Execute only after writing a trace prediction.
8. Why can a STORE overwrite an instruction? Construct a two-cycle example in
   which a former HLT becomes NOP. Which protection is absent?
9. Implement a separate slow add8 by adding integers and reducing modulo256.
   Compare every pair. Explain why two copies of ripple-adder code are a weaker
   oracle than an independently expressed mathematical operation.
10. Design a positive/zero multiplier entry check without silently changing the
    data layout. Specify the resulting ISA/program-memory trade-off before coding.
11. Extend the ISA with SUB. Define borrow vs carry, overflow and flag lifetime.
    Write a hand case, an edge case and an exhaustive arithmetic oracle.
12. Close the reference implementation. Rebuild the CPU from the encoding table.
    Require all independent tests to pass; explain every mutation in `step`.
