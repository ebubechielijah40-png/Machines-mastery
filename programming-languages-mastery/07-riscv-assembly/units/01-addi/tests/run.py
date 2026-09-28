"""Independent assembler comparison and bounded architectural checks."""
from pathlib import Path
import itertools
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
os.environ["LD_LIBRARY_PATH"] = "/tmp/machines-tools/usr/lib/x86_64-linux-gnu" + (":" + os.environ["LD_LIBRARY_PATH"] if os.environ.get("LD_LIBRARY_PATH") else "")
B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "solutions"))
from model import encode, step, MASK


def tool(name):
    installed = shutil.which("riscv64-linux-gnu-" + name)
    candidate = Path("/tmp/machines-tools/usr/bin/riscv64-linux-gnu-" + name)
    if installed:
        return installed
    if candidate.is_file():
        return str(candidate)
    raise RuntimeError("GNU RISC-V binutils missing: " + name)


class AddiTests(unittest.TestCase):
    def test_assembler_oracle(self):
        triples = [(5, 7, imm) for imm in range(-2048, 2048)]
        triples += list(itertools.product(range(32), range(32), (-2048, -1, 0, 1, 2047)))
        with tempfile.TemporaryDirectory(prefix="mm-rv-") as temp:
            d = Path(temp)
            src = '.text\n.option norvc\n' + ''.join(f'addi x{rd}, x{rs1}, {imm}\n' for rd,rs1,imm in triples)
            (d / "all.s").write_text(src)
            subprocess.run([tool("as"), "-march=rv32i", "-mabi=ilp32", str(d/"all.s"), "-o", str(d/"all.o")], check=True)
            subprocess.run([tool("objcopy"), "-O", "binary", "-j", ".text", str(d/"all.o"), str(d/"all.bin")], check=True)
            raw = (d/"all.bin").read_bytes()
            self.assertEqual(len(raw), 4*len(triples))
            for i, operands in enumerate(triples):
                self.assertEqual(int.from_bytes(raw[4*i:4*i+4], "little"), encode(*operands))

    def test_fixed_words_and_trace(self):
        self.assertEqual(encode(5,0,7), 0x00700293)
        self.assertEqual(encode(6,5,-1), 0xfff28313)
        regs, pc = [0]*32, 0
        for operands in [(5,0,7),(6,5,-1),(0,6,9)]:
            regs, pc = step(encode(*operands), regs, pc)
        self.assertEqual((regs[0], regs[5], regs[6], pc), (0,7,6,12))

    def test_all_immediates_arithmetic(self):
        for value in (0,1,2048,0x7fffffff,0x80000000,MASK):
            for imm in range(-2048,2048):
                regs=[0]*32; regs[7]=value
                result, pc=step(encode(5,7,imm),regs,0)
                self.assertEqual(result[5], (value+imm) % (2**32))
                self.assertEqual(regs[5], 0)
                self.assertEqual(pc,4)

    def test_negative_contract(self):
        for args in [(32,0,1),(0,-1,0),(1,0,2048),(1,0,-2049),(True,0,0)]:
            with self.assertRaises(ValueError): encode(*args)
        for word in (0,0xffffffff,0x00001013,-1,2**32):
            with self.assertRaises(ValueError): step(word,[0]*32,0)
        with self.assertRaises(ValueError): step(0x13,[0]*32,2)
        self.assertEqual(step(0x13,[0]*32,0xfffffffc)[1],0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
