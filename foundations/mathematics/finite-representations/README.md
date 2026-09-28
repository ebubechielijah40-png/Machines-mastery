# Positional notation and finite words

PREPARED; learner NOT STARTED. Unit F-BITS. Original explanation and derivation; see [foundation policy](../../README.md).

Suppose a small register has four boxes, each storing either 0 or 1. Assign right-to-left weights 1,2,4,8. The written word 1011 then represents 8+0+2+1=11. The weights double because shifting a place left must make room for both choices of the next box. Formally a width-w word represents sum(b_i * 2^i) for i from 0 to w−1; every b_i is 0 or 1 and these values are dimensionless.

There are two choices per box; multiplying w copies of 2 gives 2^w arrangements. Their unsigned values run from zero to 2^w−1. For w=4 the largest is 15, not 16. This is counting, not a statement about a chip's voltage. In hexadecimal one digit abbreviates four bits: digits 0–9 then A–F mean 10–15. Thus 0x12 is 1*16+2=18, and two octets 0x12 and 0x34 in high-first order represent 18*256+52=4660.

```text
bits:  1 0 1 1
weight 8 4 2 1  -> 11
```

Keeping only w low bits after addition means remainder on division by 2^w. At w=4, 15+1 gives remainder 0. This modular convention must be explicit; C signed overflow is not licensed by it. A signed two's-complement interpretation instead subtracts 2^w when the highest bit is 1: 1111 means 15−16=−1. Sign extension copies that leading bit into added high positions, preserving that signed value. For 12-bit immediate 0xFFF, 4095−4096=−1. Bitwise AND keeps a 1 only where both inputs have 1; OR keeps one where either does; XOR keeps one where exactly one does. A left shift by k positions multiplies an unsigned mathematical value by 2^k before any fixed-width truncation.

Wrong: a byte pattern has one intrinsic signed meaning. Correct: interpretation comes from the contract. Edge: width zero is outside this lesson's word domain. Doubling the number of bits squares capacity, not merely doubles it. Application: fields in instructions and network messages need explicit width and ordering. Transfer: a three-position lock with ten choices has 10^3 arrangements by the same counting argument.

Study [problems](problems/README.md), then [hints](hints/README.md) after an attempt. [Solutions](solutions/README.md) are separate. Complete the [experiment](experiments/README.md) and transfer before returning to the dependent unit.
