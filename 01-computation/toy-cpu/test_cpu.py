import copy
import itertools
import unittest
from cpu import CPU,DecodeError,add8,full_adder,instruction,multiplication_program


class CPUTests(unittest.TestCase):
    def test_every_full_adder_input_against_integer_arithmetic(self):
        for a,b,c in itertools.product((0,1),repeat=3):
            s,carry=full_adder(a,b,c)
            self.assertEqual(s+2*carry,a+b+c)

    def test_every_eight_bit_addition_against_independent_oracle(self):
        for a in range(256):
            for b in range(256):
                value,carry=add8(a,b)
                self.assertEqual(value,(a+b)%256)
                self.assertEqual(carry,a+b>=256)

    def test_hand_program_and_memory_addressing(self):
        program=[instruction('LDI',3),instruction('STA',14),instruction('LDI',4),instruction('ADD',14),instruction('STA',15),instruction('HLT')]+[0]*10
        cpu=CPU(program);trace=cpu.run()
        self.assertEqual([t['after']['accumulator'] for t in trace],[3,3,4,7,7,7])
        self.assertEqual(cpu.memory[15],7)
        self.assertEqual(program[15],0)
        self.assertEqual(cpu.cycles,6)

    def test_multiply_all_small_values_and_modular_overflow(self):
        for a,b in itertools.product(range(16),range(1,16)):
            cpu=CPU(multiplication_program(a,b));cpu.run()
            self.assertEqual(cpu.accumulator,a*b%256)
            self.assertEqual(cpu.memory[15],0)
        cpu=CPU(multiplication_program(255,2));cpu.run();self.assertEqual(cpu.accumulator,254)

    def test_carry_zero_branch_and_flag_lifetime(self):
        program=[instruction('LDI',1),instruction('ADD',14),instruction('JZ',4),instruction('LDI',9),instruction('HLT')]+[0]*9+[255,0]
        cpu=CPU(program);trace=cpu.run()
        self.assertEqual([x['address'] for x in trace],[0,1,2,4])
        self.assertEqual(cpu.accumulator,0);self.assertTrue(cpu.carry)

    def test_decode_failure_is_atomic(self):
        for bad in [0x01,0xf1,0x70,0x80,0xe0]:
            cpu=CPU([bad]+[0]*15);before=copy.deepcopy(cpu.__dict__)
            with self.assertRaises(DecodeError):cpu.step()
            self.assertEqual(cpu.__dict__,before)

    def test_wrap_budget_and_self_modification_are_explicit(self):
        cpu=CPU([0]*16,pc=15);cpu.step();self.assertEqual(cpu.pc,0)
        cpu=CPU([instruction('JMP',0)]+[0]*15)
        with self.assertRaises(TimeoutError):cpu.run(7)
        self.assertEqual(cpu.cycles,7)
        cpu=CPU([instruction('STA',1),instruction('HLT')]+[0]*14,accumulator=0)
        cpu.step();self.assertEqual(cpu.memory[1],instruction('NOP'))

    def test_invalid_boundary(self):
        for memory in [[],[0]*15,[0]*15+[256],[0]*15+[True]]:
            with self.assertRaises(ValueError):CPU(memory)
        for args in [('HLT',1),('X',0)]:
            with self.assertRaises(DecodeError):instruction(*args)
        cpu=CPU([instruction('HLT')]+[0]*15);cpu.run()
        with self.assertRaises(RuntimeError):cpu.step()

if __name__=='__main__':unittest.main(verbosity=2)
