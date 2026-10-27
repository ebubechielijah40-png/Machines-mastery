"""Independent finite-prefix oracle, boundaries, data and error contracts."""
import itertools,unittest
from budget import choose_prefix,format_result

class BudgetTests(unittest.TestCase):
    def test_worked_example(self):
        self.assertEqual(choose_prefix([12,7,5],20),([12,7],19))
        self.assertEqual(format_result([12,7,5],20),'2 packets, 19/20 payload bytes: [12, 7]')
    def test_empty_zero_exact_and_first_too_large(self):
        self.assertEqual(choose_prefix([],0),([],0));self.assertEqual(choose_prefix([0,0,1],0),([0,0],0))
        self.assertEqual(choose_prefix([2,3],5),([2,3],5));self.assertEqual(choose_prefix([6,1],5),([],0))
    def test_no_skipping_to_a_later_fitting_packet(self):
        self.assertEqual(choose_prefix([12,11,9],20),([12],12))
    def test_finite_inputs_against_independent_prefix_definition(self):
        for n in range(6):
            for values in itertools.product(range(4),repeat=n):
                source=list(values)
                for capacity in range(10):
                    # Enumerate every prefix as a candidate, rather than simulate the loop.
                    candidates=[source[:k] for k in range(n+1) if sum(source[:k])<=capacity]
                    expected=max(candidates,key=len)
                    self.assertEqual(choose_prefix(source,capacity),(expected,sum(expected)))
    def test_returned_list_is_independent_and_input_is_unchanged(self):
        source=[2,3];accepted,used=choose_prefix(source,5);accepted.append(9)
        self.assertEqual(source,[2,3]);self.assertEqual(used,5)
    def test_validate_all_inputs_before_processing(self):
        for sizes,capacity in [([1,-1],2),([1,True],2),([1,1.0],2),([100,-1],0),([1],-1),([1],True)]:
            with self.assertRaises(ValueError):choose_prefix(sizes,capacity)
        with self.assertRaises(TypeError):choose_prefix((1,2),3)

if __name__=='__main__':unittest.main()
