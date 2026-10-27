# Checkable solutions

1. In lexicographic(a,b,c) order, (sum,carry) is(0,0),(1,0),(1,0),(0,1),
(1,0),(0,1),(0,1),(1,1). Each satisfies the integer equality.

2. After k columns, low_k(a)+low_k(b)=low_k(result)+2^k carry_k.
Substitute the next column's equality and collect powers of two. k=8 yields
a+b=result+256carry, with0≤result<256.

3.11111111+00000001=00000000, carry1, signed−1+1=0.01111111+00000001=
10000000, carry0, signed127+1 exceeds127 and wraps to−128.

4.0x3d,0x2e,0x4d,0x52.0x6a is JZ10.

5. PCs after the six steps:1,2,3,4,5,6. Accumulators3,3,4,7,7,7. Carry isfalse
throughout. Writes(14,3),(15,7). Finalhaltedtrue/cycles6.

6. Base k=0 is initialization. Each ADD14 adds a, each ADD12 subtracts1 modulo256;
because1≤b≤255 the positive counter decreases without wrap untilzero. Thus p≡ka
and c=b−k by induction.2+8(b−1)+7+2=8b+3. b=0 would decrement to255; it is not
the intended zero-iteration multiplication, even though a longer modular loop
can eventually return tozero. Reject it rather than claim the proof covers it.

7. It halts with3, since each restart clears accumulated product but retains the
counter. The counter still takes four decrements, but only the final a survives.
The three nonfinal passes add the two initialization instructions:41cycles.
This is a valid terminating program with incorrect semantics, distinct from
the recorded JMP9 experiment's bounded self-loop.

8. A=0, memory0=STA1(0x41), memory1=HLT(0xf0). After firststep memory1=0;
nextfetch decodes NOP and advances. There is no executable-memory protection.

9. `return ((a+b)%256, a+b>=256)` is the oracle. Exhaustive65,536checks cover
every valid two-byte input, but not invalid boundary behavior; those need tests.

10. One option is an added entry LDAcounter/JZexit; sixteen-byte memory then
forces shortening/relocating code or expanding address width. State an exact
new layout and update branch targets. Another valid solution exposes a zero
check in the host assembler with a separate0program. Do not overwrite data to
pretend the unchanged sixteen-word layout fits extra instructions.

11. A coherent proposal: SUB sets A=(oldA−M[a])%256 and borrow=(oldA<M[a]);
other instructions preserve borrow.0−1 gives255/borrowtrue;255−1 gives254/false.
Check every pair against those formulas. If sharing the carry register, document
its SUB-specific interpretation; many real ISAs use different conventions.

12. Acceptance requires reconstructing the spec and tests, not reproducing
identical formatting. Explain invariants, flag lifetime, precise decode failure,
budget retention and unified-memory aliasing without opening the solution.
