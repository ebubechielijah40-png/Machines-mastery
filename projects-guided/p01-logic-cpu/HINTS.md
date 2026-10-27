# Use hints after a written attempt

If your adder fails only near255, inspect the outgoing carry instead of extending
the stored result to nine bits. Each column consumes the previous column's carry.

If ADD14 gives18 in the3+4 program, you have confused memory addressing with an
immediate. LDI carries a literal; ADD reads M[operand].

If JZ fails after an LDA, do not consult an old flag that the ISA never defined.
It tests current A. If an invalid opcode changes PC, stage the proposed next PC
locally and commit after successful decode.

If multiplication loops unexpectedly, trace the counter separately from product.
The decrement uses memory12=255, not an immediate value255. For zero multipliers,
fix the entry condition and memory layout before claiming the positive-counter
proof extends. For the JMP0 fault, restarting code resets product but not counter.

The [separate solutions](../../01-computation/toy-cpu/SOLUTIONS.md) include proofs,
exact exercise results and a reconstruction acceptance criterion.
