# Before constructing the CPU

You need unsigned binary place value, AND/OR/XOR, indexing and Python functions.
Read the first two sections of the [local CPU lesson](../../01-computation/toy-cpu/README.md)
for those mechanisms. Python3.10+ and its standard library are sufficient; no
HDL tool, emulator download, board or network access is required.

Entry check, by hand: 0b1011 is11; 7 XOR3 is4; 255+1 reduced to eight bits is0
with carry1;0x2e has opcode2 and operand14. If these answers are unclear, list
powers of two and the four input pairs of each Boolean operation before
proceeding. Carry beyond an unsigned byte and signed overflow are different.

The reference models one abstract transition at a time. Prior knowledge of real
pipelines is unnecessary and must not be imported as an unstated timing rule.
Read [SOURCES.md](../../01-computation/toy-cpu/SOURCES.md) for the inspected author
project pages and the distinction from their sixteen-bit Hack computer.
