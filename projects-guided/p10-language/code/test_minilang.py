from fractions import Fraction
import itertools
import unittest
from minilang import evaluate,parse,tokenize,LanguageError,MAX_DEPTH

class LanguageTests(unittest.TestCase):
    def test_precedence_associativity_and_exact_rationals(self):
        self.assertEqual(evaluate('2+3*4; (2+3)*4; 8/4/2; 7-3-1; 1/3+1/6;'),[14,20,1,3,Fraction(1,2)])
        self.assertEqual(parse('1+2*3;')[0],('expr',('+',('number',1),('*',('number',2),('number',3)))))
    def test_generated_parenthesized_expressions_independent_arithmetic(self):
        operations={'+':lambda a,b:a+b,'-':lambda a,b:a-b,'*':lambda a,b:a*b,'/':lambda a,b:a/b}
        for a,b,c in itertools.product(range(-2,3),repeat=3):
            for left,right in itertools.product(operations,repeat=2):
                try:expected=operations[right](operations[left](Fraction(a),Fraction(b)),Fraction(c))
                except ZeroDivisionError:continue
                self.assertEqual(evaluate(f'(({a}){left}({b})){right}({c});'),[expected])
    def test_bindings_and_unary(self):
        env={};self.assertEqual(evaluate('let x = 2; let x=x+3; --x; -(-1+2);',env),[5,-1]);self.assertEqual(env['x'],5)
        self.assertEqual(evaluate('x/2;',env),[Fraction(5,2)])
    def test_failed_program_is_atomic(self):
        for source in ['let x=9; 1/0;','let x=9; missing;','let x=9; 1+;']:
            env={'x':Fraction(2)}
            with self.assertRaises(LanguageError):evaluate(source,env)
            self.assertEqual(env,{'x':2})
    def test_comments_and_token_offsets(self):
        self.assertEqual(evaluate('# comment\n let total=12; # another\n total;'),[12])
        self.assertEqual([(t.kind,t.offset) for t in tokenize(' 12 + x;')],[('int',1),('+',4),('name',6),(';',7),('eof',8)])
    def test_invalid_syntax_and_host_code_rejected(self):
        for source in ['1','let=2;','1 2;','2**3;','x=1;','"text";','__import__("os");','[1];','1;;']:
            with self.subTest(source=source),self.assertRaises(LanguageError):evaluate(source)
    def test_bounded_resources(self):
        for source in ['('*100+'1'+')'*100+';', '1'*1300+';', '1;'*5000, '+'.join(['1']*100)+';']:
            with self.assertRaises(LanguageError):evaluate(source)
        env={'x':Fraction(1<<4096)}
        with self.assertRaises(LanguageError):evaluate('x;',env)
    def test_empty_program_and_input_contract(self):
        env={'a':1};self.assertEqual(evaluate('',env),[]);self.assertEqual(env,{'a':1})
        for source,environment in [(None,{}),('1;',[]),('1;',{'x':True})]:
            with self.assertRaises(LanguageError):evaluate(source,environment)
if __name__=='__main__':unittest.main(verbosity=2)
