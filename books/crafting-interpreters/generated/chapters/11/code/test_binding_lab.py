import unittest
from binding_lab import *


def late_declaration():
    return (Let('label', Literal('catalog')), Block((
        Function('read', (), (Print(Name('label')),)),
        Expression(Call(Name('read'))), Let('label', Literal('local')),
        Expression(Call(Name('read'))))))


def counters():
    return (Function('make', (), (
        Let('n', Literal(0)),
        Function('next', (), (
            Expression(Assign('n', Add(Name('n'), Literal(1)))), Return(Name('n')))),
        Return(Name('next')))),
        Let('a', Call(Name('make'))), Let('b', Call(Name('make'))),
        Print(Call(Name('a'))), Print(Call(Name('a'))), Print(Call(Name('b'))), Print(Call(Name('a'))))


class BindingTests(unittest.TestCase):
    def test_late_declaration_counterexample(self):
        program = compile_program(late_declaration())
        self.assertEqual(program.run()['output'], ['catalog', 'catalog'])
        self.assertEqual(program.run(lookup='mutable-chain')['output'], ['catalog', 'local'])

    def test_closure_shared_mutation_and_distinct_factory_frames(self):
        program = compile_program(counters())
        self.assertEqual(program.run()['output'], [1, 2, 1, 3])
        self.assertEqual(program.run()['output'], [1, 2, 1, 3])  # Fresh globals on each run.

    def test_static_addresses_distinguish_occurrences(self):
        near, far = Name('x'), Name('x')
        program = compile_program((Block((Let('x', Literal(2)), Print(near),
                                         Block((Print(far),)))),))
        self.assertEqual(program.addresses[near], 0)
        self.assertEqual(program.addresses[far], 1)
        self.assertEqual(program.run()['output'], [2, 2])
        with self.assertRaises(TypeError):
            program.addresses[near] = 3

    def test_assignment_keeps_outer_target_after_late_shadow(self):
        program = compile_program((Let('x', Literal(0)), Block((
            Function('set', (), (Expression(Assign('x', Literal(8))),)),
            Let('x', Literal(99)), Expression(Call(Name('set'))), Print(Name('x')))),
            Print(Name('x'))))
        self.assertEqual(program.run()['output'], [99, 8])
        self.assertEqual(program.run(lookup='mutable-chain')['output'], [8, 0])

    def test_lexical_parent_not_caller(self):
        program = compile_program((Let('x', Literal(4)),
            Function('read', (), (Return(Name('x')),)),
            Function('caller', ('x',), (Return(Call(Name('read'))),)),
            Print(Call(Name('caller'), (Literal(100),)))))
        self.assertEqual(program.run()['output'], [4])

    def test_function_self_reference_recursion(self):
        count = Function('count', ('n',), (
            If(Equal(Name('n'), Literal(0)), Return(Literal(0)),
               Return(Add(Literal(1), Call(Name('count'), (Subtract(Name('n'), Literal(1)),))))),))
        self.assertEqual(compile_program((count, Print(Call(Name('count'), (Literal(7),))))).run()['output'], [7])

    def test_globals_looked_up_at_runtime(self):
        program = compile_program((Function('later', (), (Return(Name('x')),)),
                                   Let('x', Literal(2)), Print(Call(Name('later'))),
                                   Let('x', Literal(5)), Print(Call(Name('later')))))
        self.assertEqual(program.run()['output'], [2, 5])
        with self.assertRaises(ExecutionError):
            compile_program((Print(Name('missing')),)).run()

    def test_static_errors_include_unexecuted_branch(self):
        cases = [(Return(Literal(1)),),
                 (Block((Let('x', Name('x')),)),),
                 (Block((Let('x', Assign('x', Literal(1))),)),),
                 (Block((Let('x', Literal(1)), Let('x', Literal(2)))),),
                 (Function('f', ('x', 'x'), (Return(Name('x')),)),),
                 (If(Literal(False), Block((Let('x', Name('x')),)), Block(())),)]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(BindingError):
                compile_program(case)

    def test_arity_types_and_resource_bounds(self):
        for case in [(Print(Add(Literal(True), Literal(2))),),
                     (If(Literal(1), Block(()), Block(())),),
                     (Expression(Call(Literal(2))),),
                     (Function('f', ('x',), ()), Expression(Call(Name('f'))))]:
            with self.subTest(case=case), self.assertRaises(ExecutionError):
                compile_program(case).run()
        infinite = compile_program((Function('f', (), (Return(Call(Name('f'))),)), Expression(Call(Name('f')))))
        with self.assertRaisesRegex(ExecutionError, 'call depth'):
            infinite.run(call_limit=10)
        with self.assertRaisesRegex(ExecutionError, 'step budget'):
            compile_program(counters()).run(steps=3)
        for kwargs in ({'steps':True}, {'call_limit':0}, {'lookup':'unknown'}):
            with self.assertRaises(ExecutionError):compile_program(()).run(**kwargs)

    def test_nested_recursive_expressions_reject_with_controlled_error(self):
        body = Call(Name('f'))
        for _ in range(50):body = Add(Literal(0), body)
        program = compile_program((Function('f', (), (Return(body),)), Expression(Call(Name('f')))))
        with self.assertRaises(ExecutionError):program.run()

    def test_ast_occurrence_and_shape_validation(self):
        reused = Name('x')
        bad = [(Print(reused), Print(reused)), (Literal(1),), (Print(Literal(object())),),
               (Let('bad-name', Literal(1)),), (Block([]),), (Print(Literal(1 << 4096)),)]
        for case in bad:
            with self.subTest(case=case), self.assertRaises(BindingError):compile_program(case)
        node = Literal(1)
        for _ in range(82):node = Add(node, Literal(0))
        with self.assertRaises(BindingError):compile_program((Print(node),))

    def test_exhaustive_small_shadowing_address_oracle(self):
        # Directly know which frame's unique marker is nearest; no runtime search oracle.
        for outer in range(5):
            for inner in range(5):
                tree = (Block((Let('x', Literal(outer)), Block((Let('x', Literal(inner)),
                          Print(Name('x')))), Print(Name('x')))),)
                self.assertEqual(compile_program(tree).run()['output'], [inner, outer])


if __name__ == '__main__':
    unittest.main(verbosity=2)
