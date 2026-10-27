# Derive and build in six milestones

1. **Bit arithmetic.** Write a full-adder function from AND/OR/XOR. Enumerate all
   eight triples and check a+b+c=s+2carry. Connect eight columns; preserve the
   outgoing carry. Exit only after all65,536 byte pairs match an independent
   integer arithmetic oracle. Predict255+1 and127+1 under signed/unsigned readings.
2. **State and fetch.** Define exactly sixteen bytes, A, PC, carry, halted and a
   cycle count. Copy supplied memory. Implement NOP/HLT, PC modulo16, and rejection
   of an invalid word without a partial state change. Trace a HLT at address15:
   after the cycle PC=0, halted=true, cycles=1.
3. **Data movement.** Add LDI/LDA/STA using the encoding table. Implement the
   six-instruction3+4 program from the lesson. First predict every accumulator
   value and memory write. Exit on A trace[3,3,4,7,7,7], M[15]=7 and cycles=6.
4. **Control and arithmetic.** Add ADD/JMP/JZ. Carry changes only on ADD. JZ tests
   A directly. Decode all operands before committing any register/memory mutation.
   Test carry1 with A0, a taken branch, a nontaken branch and PC wraparound.
5. **An algorithm in machine words.** Construct repeated-addition multiplication
   with data at12–15. Prove p≡ka(mod256), c=b−k for positive initial b and derive
   8b+3 cycles. Check3×4=12 in35cycles and255×2=254 in19cycles. Reject b=0 until
   you design a correct entry check and new memory layout.
6. **Observe and reconstruct.** Inject JMP9 at address9, preserve a bounded trace,
   and distinguish nontermination from an invalid opcode. Close the reference
   and reconstruct the machine from the ISA table, including failure atomicity.
   Finally propose SUB with precise flag semantics and independent exhaustive tests.

At every milestone save a short prediction, implementation and actual result.
The complete reference is executable; learner milestones are tasks rather than
claims that an unimplemented starter is finished software.
