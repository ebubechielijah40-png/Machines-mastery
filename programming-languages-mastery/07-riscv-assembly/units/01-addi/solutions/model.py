"""Original RV32I ADDI-only architectural teaching model."""
MASK = (1 << 32) - 1


def encode(rd, rs1, imm):
    if any(type(x) is not int for x in (rd, rs1, imm)):
        raise ValueError("integer operands required")
    if not (0 <= rd < 32 and 0 <= rs1 < 32 and -2048 <= imm <= 2047):
        raise ValueError("operand outside ADDI domain")
    return ((imm & 4095) << 20) | (rs1 << 15) | (rd << 7) | 0x13


def step(word, regs, pc):
    if type(word) is not int or not 0 <= word <= MASK:
        raise ValueError("word must be unsigned 32-bit")
    if len(regs) != 32 or any(type(v) is not int or not 0 <= v <= MASK for v in regs) or regs[0] != 0:
        raise ValueError("invalid architectural registers")
    if type(pc) is not int or not 0 <= pc <= MASK or pc % 4:
        raise ValueError("invalid aligned PC")
    if word & 0x7f != 0x13 or (word >> 12) & 7:
        raise ValueError("not an ADDI instruction")
    rd, rs1 = (word >> 7) & 31, (word >> 15) & 31
    imm = word >> 20
    if imm & 2048:
        imm -= 4096
    result = regs.copy()
    if rd:
        result[rd] = (regs[rs1] + imm) & MASK
    return result, (pc + 4) & MASK
