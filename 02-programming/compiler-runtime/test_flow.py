"""Finite independent arithmetic/closed-form oracles and bad bytecode."""
from fractions import Fraction
import unittest
from flow import (Instruction as I,Program,Machine,SourceError,VerificationError,
                  RuntimeFault,MIN_INT,compile_source,verify,disassemble)


def execute(source,**options):return Machine(compile_source(source),**options).run()


class FlowTests(unittest.TestCase):
    def test_precedence_and_left_association(self):
        source='print 2+3*4;print (2+3)*4;print 20-6-3;print 20/(6-3);print 3<2<1;'
        self.assertEqual(execute(source).output,(14,20,11,6,1))

    def test_exact_finite_arithmetic_oracle(self):
        cases=0
        for a in range(-7,8):
            for b in range(-7,8):
                for op in ('+','-','*','/','<','=='):
                    if op=='/' and b==0:continue
                    if op=='+':expected=a+b
                    elif op=='-':expected=a-b
                    elif op=='*':expected=a*b
                    elif op=='/':expected=int(Fraction(a,b))
                    elif op=='<':expected=int(a<b)
                    else:expected=int(a==b)
                    self.assertEqual(execute(f'print ({a}) {op} ({b});').output,(expected,))
                    cases+=1
        self.assertEqual(cases,1335)

    def test_sum_loop_against_closed_form(self):
        for n in range(31):
            result=execute(f'let i=0;let s=0;while(i<{n}){{s=s+i;i=i+1;}}print s;')
            self.assertEqual(result.output,(n*(n-1)//2,))
            self.assertEqual(result.locals,(n,n*(n-1)//2))

    def test_branch_truth_and_dead_branch(self):
        for n in range(-5,6):
            program=compile_source(f'let x={n};if(x){{x=12;}}else{{x=9;}}print x;')
            first=Machine(program).run();second=Machine(program).run()
            self.assertEqual(first,second);self.assertEqual(first.output,(12 if n else 9,))
        self.assertEqual(execute('if(0){print 1/0;}print 4;').output,(4,))

    def test_nested_flow(self):
        self.assertEqual(execute('let i=0;let s=0;while(i<6){if(i<3){s=s+2;}else{s=s+5;}i=i+1;}print s;').output,(21,))

    def test_debugger_and_immutable_history(self):
        machine=Machine(compile_source('let x=3;x=x+2;print x;'))
        initial=machine.state;stopped=machine.until(breakpoints=(2,))
        self.assertEqual((stopped.pc,stopped.locals),(2,(3,)))
        self.assertEqual(machine.until(breakpoints=(2,)),stopped)
        machine.step();self.assertEqual(machine.run().output,(5,))
        self.assertEqual((initial.stack,initial.locals),((),(None,)))
        self.assertEqual(machine.step(),machine.state)

    def test_fault_source_map_and_atomic_instruction(self):
        source='let x=8;\nprint x;\nx=x/(x-8);'
        machine=Machine(compile_source(source))
        with self.assertRaises(RuntimeFault) as caught:machine.run()
        self.assertEqual(caught.exception.offset,source.index('/'))
        self.assertEqual(caught.exception.state,machine.state)
        self.assertEqual((machine.state.locals,machine.state.output,machine.state.stack),((8,),(8,),(8,0)))
        before=machine.state
        with self.assertRaises(RuntimeFault):machine.step()
        self.assertEqual(machine.state,before)

    def test_signed_boundaries(self):
        self.assertEqual(execute('print -2147483647-1;').output,(MIN_INT,))
        for source in ('print 2147483647+1;','print (-2147483647-1)/-1;','print -(-2147483647-1);','print 100000*100000;'):
            with self.assertRaisesRegex(RuntimeFault,'overflow'):execute(source)
        with self.assertRaises(SourceError):compile_source('print 2147483648;')
        self.assertEqual(execute('print -7/3;print 7/-3;print -7/-3;').output,(-2,-2,2))

    def test_instruction_and_output_budgets(self):
        machine=Machine(compile_source('while(1){}'),budget=17)
        with self.assertRaisesRegex(RuntimeFault,'instruction budget'):machine.run()
        self.assertEqual(machine.state.steps,17)
        self.assertFalse(machine.state.halted)
        machine=Machine(compile_source('while(1){print 7;}'),output_limit=3)
        with self.assertRaisesRegex(RuntimeFault,'output budget'):machine.run()
        self.assertEqual(machine.state.output,(7,7,7))
        with self.assertRaises(RuntimeFault):execute('print 1;',output_limit=0)
        machine=Machine(compile_source('print 1;'),budget=2)
        with self.assertRaises(RuntimeFault):machine.run()
        self.assertEqual((machine.state.output,machine.state.halted),((1,),False))
        self.assertTrue(execute('',budget=1).halted)

    def test_source_errors_and_empty_program(self):
        for source in ('print @;','print 1','let while=2;','let x=x;','let x=1;let x=2;','x=2;','print missing;','if(1){let x=2;}','while(0){','print (1+);','print __import__(1);','print 1.5;'):
            with self.subTest(source=source),self.assertRaises(SourceError):compile_source(source)
        self.assertEqual(execute('#empty program\n').output,())

    def test_resource_bounds(self):
        cases=[' '*8193,'print '+'('*35+'1'+')'*35+';','print '+'0'*100+';','let '+'a'*65+'=0;',
               ''.join(f'let x{i}=0;' for i in range(65)),'print 0;'*1025]
        for source in cases:
            with self.assertRaises((SourceError,VerificationError)):compile_source(source)
        with self.assertRaises(TypeError):compile_source(b'print 1;')
        for options in ({'budget':True},{'budget':0},{'output_limit':-1}):
            with self.assertRaises(ValueError):Machine(compile_source(''),**options)

    def test_verifier_shape_stack_and_slot_mutants(self):
        bad=[Program((I('ADD'),I('HALT')),()),Program((I('CONST',1),I('HALT')),()),
             Program((I('JUMP',9),I('HALT')),()),Program((I('LOAD',0),I('PRINT'),I('HALT')),('x',)),
             Program((I('NOPE'),I('HALT')),()),Program((I('HALT',0),),()),
             Program((I('CONST',True),I('PRINT'),I('HALT')),()),Program((I('LOAD',True),I('HALT')),('x',)),
             Program((I('HALT'),),([],)),Program((I('HALT',offset=1),),()),Program([I('HALT')],()),
             Program(tuple([I('CONST',1)]*65+[I('PRINT')]*65+[I('HALT')]),())]
        for program in bad:
            with self.subTest(program=program),self.assertRaises(VerificationError):verify(program)

    def test_join_heights_and_definite_initialization(self):
        incompatible=Program((I('CONST',1),I('JZ',4),I('CONST',9),I('JUMP',4),I('HALT')),())
        with self.assertRaises(VerificationError):verify(incompatible)
        missing=Program((I('CONST',1),I('JZ',4),I('CONST',9),I('STORE',0),I('LOAD',0),I('PRINT'),I('HALT')),('x',))
        with self.assertRaisesRegex(VerificationError,'uninitialized'):verify(missing)
        both=Program((I('CONST',1),I('JZ',5),I('CONST',9),I('STORE',0),I('JUMP',7),I('CONST',7),I('STORE',0),I('LOAD',0),I('PRINT'),I('HALT')),('x',))
        self.assertEqual(Machine(both).run().output,(9,))

    def test_verification_is_not_termination_or_arithmetic_proof(self):
        infinite=Program((I('JUMP',0),I('HALT')),())
        self.assertEqual(verify(infinite)['reachable_instructions'],1)
        with self.assertRaises(RuntimeFault):Machine(infinite,budget=5).run()
        zero=compile_source('print 1/0;')
        self.assertGreater(verify(zero)['reachable_instructions'],1)
        with self.assertRaises(RuntimeFault):Machine(zero).run()

    def test_debugger_input_and_character_offsets(self):
        program=compile_source('# λ\nprint 2+3;')
        self.assertIn('h= 2 ADD',disassemble(program))
        self.assertEqual(program.code[0].offset,program.source.index('2'))
        machine=Machine(program)
        for points in ([1],(True,),(-1,),(99,)):
            with self.assertRaises(ValueError):machine.until(breakpoints=points)
        for steps in (True,-1,100001):
            with self.assertRaises(ValueError):machine.until(steps=steps)
        self.assertEqual(machine.until(steps=0),machine.state)


if __name__=='__main__':unittest.main()
