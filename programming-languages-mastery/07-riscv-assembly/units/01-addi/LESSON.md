# Text, instruction bits and architectural effect

[EXPLANATION] A CPU cannot execute the letters in `addi x5, x0, 7` as text. An assembler translates mnemonic and operands into a word whose fields select an operation, source, destination and constant. An ISA defines the visible effect of that word. It does not prescribe the exact transistor network or number of clock cycles.

[SOURCE] The RV32I base integer specification, version 2.1 in the 20260120 collection, defines 32 integer registers of 32 bits, x0 fixed to zero, and ADDI adding a sign-extended 12-bit immediate with the low 32 bits retained. See [evidence](SOURCES.md). The fixed-zero register lets a constant be introduced without first loading a zero value from memory.

## Derive the word

The ADDI I-type layout is immediate[11:0] in bits 31:20, rs1 in 19:15, funct3=000 in 14:12, rd in 11:7, opcode=0010011 in 6:0. A bit position starts from zero at the least significant bit. A field shifted left by k occupies positions beginning at k; combining non-overlapping fields with OR preserves all of them.

```text
31              20 19    15 14 12 11     7 6          0
[ immediate:12   ][ rs1:5 ][000][ rd:5   ][0010011   ]
```

For x5,x0,7: the immediate contributes 7*2^20 = 0x00700000. rs1 contributes zero. rd contributes 5*2^7=0x00000280. Add the opcode 0x13, giving 0x00700293. This is the numeric instruction word; its four bytes in the tool's little-endian object are 93 02 70 00. Distinguish field layout within a word from byte ordering in storage. Our assembler test checks both explicitly.

For immediate −1, the 12-bit representation is 2^12−1=4095=0xFFF. Decode by subtracting 4096 when bit 11 is set. Sign extension preserves the signed value; simply treating 0xFFF as positive would add 4095 instead of subtracting one. The allowed immediate range is −2048 through 2047. A larger constant requires another sequence; silently masking an invalid source immediate is an assembler bug.

## State transition

Let r[i] be the current 32-bit register word, pc the current instruction address, and imm the decoded signed immediate. Compute v=(r[rs1]+imm) mod 2^32. If rd is not zero, set r[rd]=v. If rd is zero, discard v. In either case keep r[0]=0 and advance pc by four in this restricted straight-line sequence. A 32-bit word is a mathematical residue here; a signed interpretation of its top bit is separate.

Trace from all-zero registers and pc=0:

| Instruction | Written state | Next pc |
| --- | --- | --- |
| addi x5,x0,7 | x5=7 | 4 |
| addi x6,x5,-1 | x6=6 | 8 |
| addi x0,x6,9 | x0 remains 0 | 12 |

Changing the first immediate to zero makes the second result 0xFFFFFFFF. That wraparound is specified ISA behavior, not a license for C signed overflow. The last instruction still advances the PC although its destination is x0. There are no data-memory reads/writes in ADDI's arithmetic effect; instruction fetching is a separate part of executing a program.

## Internal model and alternatives

A minimal interpreter checks the word width and ADDI opcode/funct3, extracts fields, sign-decodes imm, computes the result and applies the writeback rule. A hardware design can implement corresponding decode, register selection, addition and write-enable logic. Sharing one adder versus having multiple adders affects implementation constraints, not this required architectural result. This bridge motivates the future HDL processor capstone; it does not claim that our interpreter is how a particular chip is built.

Invariant: all r[i] stay in [0,2^32−1], r[0]=0, and each accepted step advances this model's pc by four modulo 2^32. Initialization establishes it; masking the arithmetic result and guarding writeback preserve it. Invalid opcodes reject before mutation. For an ADDI word, the disjoint field extraction recovers precisely the chosen source/destination and signed immediate, so the transition implements the stated contract.

Wrong approaches: fail to sign-extend; write x0; confuse numeric word and byte order; assume an unknown opcode means no-op; assume four-byte PC advance for every possible RISC-V extension. Our model rejects everything outside its declared subset. Unaligned PC is also rejected, because this unit assumes fixed-width RV32I instruction alignment.

## How to verify independently

Compare hand-derived words with a real assembler, then compare state traces with hand-derived arithmetic. An encoder and decoder sharing the same wrong bit position could pass round trips, so the external assembler is a distinct encoding oracle. Exhaustively sweep all 4096 immediate values on chosen registers and check immediate boundaries across all register pairs. These checks establish bounded model behavior; they do not establish full ISA compliance or physical execution performance. Each instruction has constant model work and fixed register storage; no benchmark claim follows.
