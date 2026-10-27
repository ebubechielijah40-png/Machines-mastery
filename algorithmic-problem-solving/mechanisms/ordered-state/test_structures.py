import random
import unittest
from structures import ChainedMap,StableHeap,SearchTree,byte_hash


class MechanismTests(unittest.TestCase):
    def test_hash_randomized_operation_histories_against_dict(self):
        for hasher in (byte_hash,lambda _:0):
            rng=random.Random(718);table=ChainedMap(hasher);oracle={}
            for _ in range(2600):
                key=rng.randrange(80).to_bytes(2,'little');operation=rng.randrange(4)
                if operation<2:
                    value=rng.choice([None,False,rng.randrange(-200,200)]);table[key]=value;oracle[key]=value
                elif operation==2:
                    if key in oracle:del table[key];del oracle[key]
                    else:
                        before=table.items()
                        with self.assertRaises(KeyError):del table[key]
                        self.assertEqual(before,table.items())
                else:
                    if key in oracle:self.assertEqual(table[key],oracle[key])
                    else:
                        with self.assertRaises(KeyError):_ = table[key]
                self.assertEqual(dict(table.items()),oracle);self.assertEqual(len(table),len(oracle));self.assertLessEqual(table.inspect()['load'],.75)

    def test_hash_collisions_resizes_and_failed_validation(self):
        table=ChainedMap(lambda _:0);n=256
        for i in range(n):table[i.to_bytes(2,'little')]=i
        self.assertEqual(table.key_comparisons,n*(n-1)//2);self.assertEqual(table.inspect()['max_chain'],n);self.assertLess(table.rehashed_entries,2*n)
        before=table.items()
        for key in ('abc',bytearray(b'abc'),1,None):
            with self.assertRaises(ValueError):table[key]=4
            self.assertEqual(before,table.items())
        table[b'']=None;self.assertIsNone(table[b'']);table[b'']=0;self.assertEqual(table[b''],0)
        self.assertEqual(byte_hash(b'ab'),ord('a')*257+ord('b'))
        bad=ChainedMap(lambda _:False)
        with self.assertRaises(ValueError):bad[b'x']=1
        self.assertEqual(len(bad),0)

    def test_heap_histories_against_sorted_independent_entries(self):
        rng=random.Random(840);heap=StableHeap();oracle=[];serial=0
        for _ in range(3500):
            if not oracle or rng.random()<.62:
                priority=rng.randrange(-6,7);payload={'serial':serial};heap.push(priority,payload);oracle.append((priority,serial,payload));serial+=1
            else:
                expected=min(oracle,key=lambda x:x[:2]);oracle.remove(expected);self.assertEqual(heap.pop(),(expected[0],expected[2]))
            self.assertEqual(len(heap),len(oracle));heap.inspect()
        while oracle:
            expected=min(oracle,key=lambda x:x[:2]);oracle.remove(expected);self.assertEqual(heap.pop(),(expected[0],expected[2]))
        with self.assertRaises(IndexError):heap.pop()

    def test_bottom_up_heap_and_tie_payloads(self):
        for n in (0,1,2,3,7,31,256,1024):
            items=[(n-i,object()) for i in range(n)];heap=StableHeap(items)
            self.assertLessEqual(heap.comparisons,2*n)
            self.assertEqual([heap.pop()[0] for _ in items],list(range(1,n+1)))
        one,two=object(),object();heap=StableHeap([(1,one),(1,two)]);self.assertIs(heap.pop()[1],one);self.assertIs(heap.pop()[1],two)
        heap=StableHeap([(2,'x')])
        with self.assertRaises(ValueError):heap.push(True,'y')
        self.assertEqual(heap.pop(),(2,'x'))

    def test_bst_histories_order_rank_select_against_sorted_map(self):
        rng=random.Random(125);tree=SearchTree();oracle={}
        for _ in range(2600):
            key=rng.randrange(-60,61);operation=rng.randrange(4)
            if operation<2:value=rng.choice([None,key*3]);tree[key]=value;oracle[key]=value
            elif operation==2:
                if key in oracle:del tree[key];del oracle[key]
                else:
                    with self.assertRaises(KeyError):del tree[key]
            else:
                if key in oracle:self.assertEqual(tree[key],oracle[key])
                else:
                    with self.assertRaises(KeyError):_ = tree[key]
            ordered=sorted(oracle.items());self.assertEqual(tree.items(),tuple(ordered));self.assertEqual(tree.inspect()['size'],len(oracle));self.assertEqual(tree.rank(key),sum(k<key for k in oracle))
            if oracle:
                index=rng.randrange(len(oracle));self.assertEqual(tree.select(index),ordered[index])

    def test_bst_two_child_splice_root_and_skew_without_recursion(self):
        for sequence in ([8,3,10,1,6,14,4,7,13],[8,3,10,12],[8,3],[8]):
            for removed in sequence:
                tree=SearchTree()
                for value in sequence:tree[value]=value*2
                del tree[removed];tree.inspect();self.assertEqual(tree.items(),tuple((k,k*2) for k in sorted(set(sequence)-{removed})))
                self.assertEqual([tree.select(i)[0] for i in range(len(tree))],sorted(set(sequence)-{removed}))
        tree=SearchTree();n=1100
        for i in range(n):tree[i]=i
        self.assertEqual(tree.key_comparisons,n*(n-1)//2);self.assertEqual(tree.inspect()['height'],n)
        for i in range(n):del tree[i]
        self.assertEqual(tree.inspect(),{'size':0,'height':0})
        with self.assertRaises(IndexError):tree.select(0)
        with self.assertRaises(ValueError):tree[False]=0
        with self.assertRaises(IndexError):tree.select(True)


if __name__=='__main__':unittest.main(verbosity=2)
