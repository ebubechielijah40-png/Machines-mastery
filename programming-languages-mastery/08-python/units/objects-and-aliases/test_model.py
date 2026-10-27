import copy,dis,unittest
from model import observations,append_item

class ObjectTests(unittest.TestCase):
    def test_alias_shallow_and_deep_edges(self):
        r=observations()
        for k in ['alias_same','shallow_outer_distinct','shallow_inner_same','deep_inner_distinct']:self.assertTrue(r[k])
        for k in ['a','b','shallow']:self.assertEqual(r['after_mutation'][k],[[1,9],[2]])
        self.assertEqual(r['after_mutation']['deep'],[[1],[2]])
    def test_tuple_mutable_referent(self):self.assertEqual(observations()['tuple_contains_changed_list'],[1,2])
    def test_rebinding_versus_in_place(self):
        r=observations();self.assertEqual(r['rebind_does_not_mutate_alias'],([1,2],[1]));self.assertEqual(r['augmented_list_mutates_alias'],([1,2],[1,2]))
    def test_new_default_container_per_call(self):
        self.assertEqual(append_item('a'),['a']);self.assertEqual(append_item('b'),['b'])
        existing=[];self.assertIs(append_item('x',existing),existing)
    def test_copy_of_cycle_preserves_cycle_structure(self):
        a=[];a.append(a);b=copy.deepcopy(a);self.assertIsNot(a,b);self.assertIs(b,b[0])
    def test_identity_and_equality_different_questions(self):
        a=[1];b=[1];self.assertEqual(a,b);self.assertIsNot(a,b)
if __name__=='__main__':unittest.main(verbosity=2)
