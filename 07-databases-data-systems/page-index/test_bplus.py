import dataclasses
import itertools
from pathlib import Path
import random
import struct
import tempfile
import unittest
import zlib

from bplus import (BPlusIndex, Node, capacities, encode_node, decode_node,
                   IMAGE_HEADER, PAGE_HEADER, LEAF_CELL, CRC, MIN_KEY, MAX_KEY)


class IndexTests(unittest.TestCase):
    def test_codec_byte_layout_and_boundaries(self):
        self.assertEqual(capacities(128), (3, 9))
        self.assertEqual(capacities(256), (7, 19))
        node = Node(7, True, (-2, 9), (b'A', b'\0B'), next_leaf=8)
        raw = encode_node(node, 128)
        self.assertEqual(len(raw), 128)
        self.assertEqual(raw[:16].hex(), '42504931010000020000000700000008')
        self.assertEqual(raw[16:25].hex(), 'fffffffffffffffe01')
        self.assertEqual(raw[25:49], b'A'+b'\0'*23)
        self.assertEqual(raw[49:58].hex(), '000000000000000902')
        self.assertEqual(decode_node(raw, 128, 7), node)
        for key in (MIN_KEY, MAX_KEY):
            n=Node(1,True,(key,),(b'x'*24,))
            self.assertEqual(decode_node(encode_node(n,128),128),n)
        with self.assertRaises(ValueError):decode_node(raw,128,8)

    def test_empty_updates_extreme_keys_and_half_open_ranges(self):
        t=BPlusIndex()
        self.assertEqual(t.validate(),dict(height_edges=0,leaf_pages=1,pages=1,rows=0))
        self.assertIsNone(t.get(0));self.assertEqual(t.range(),[])
        data={MIN_KEY:b'',-1:b'negative',0:b'zero',MAX_KEY:b'last'}
        for k,v in data.items():t.put(k,v);t.validate()
        t.put(0,b'updated');data[0]=b'updated'
        self.assertEqual(t.size,4)
        self.assertEqual(t.range(),sorted(data.items()))
        self.assertEqual(t.range(-1,MAX_KEY),[(-1,b'negative'),(0,b'updated')])
        self.assertEqual(t.range(MAX_KEY,None),[(MAX_KEY,b'last')])
        self.assertEqual(t.range(2,2),[]);self.assertEqual(t.range(3,2),[])
        self.assertIsNone(t.get(7))

    def test_all_small_permutations_against_sorted_dictionary(self):
        for permutation in itertools.permutations(range(6)):
            t=BPlusIndex();oracle={}
            for k in permutation:
                t.put(k,bytes([k]));oracle[k]=bytes([k])
                t.validate()
                self.assertEqual(t.range(),sorted(oracle.items()))
            for lo,hi in itertools.product(range(-1,8),repeat=2):
                self.assertEqual(t.range(lo,hi),[(k,v) for k,v in sorted(oracle.items()) if lo<=k<hi])

    def test_recursive_splits_orders_overwrites_and_reopen(self):
        for order in ('ascending','descending','shuffled'):
            keys=list(range(450))
            if order=='descending':keys.reverse()
            elif order=='shuffled':random.Random(910).shuffle(keys)
            t=BPlusIndex()
            for k in keys:t.put(k,str(k).encode())
            report=t.validate()
            self.assertGreaterEqual(report['height_edges'],2)
            self.assertEqual(t.range(),[(k,str(k).encode()) for k in range(450)])
            for k in range(0,450,7):t.put(k,b'new')
            reopened=BPlusIndex.loads(t.dumps())
            self.assertEqual(reopened.range(),t.range())
            for k in range(-2,452):self.assertEqual(reopened.get(k),t.get(k))
            self.assertEqual(reopened.dumps(),t.dumps())

    def test_random_operation_ranges_with_independent_oracle(self):
        rng=random.Random(72104)
        for size in (128,256,512):
            t=BPlusIndex(size);oracle={}
            for step in range(1200):
                key=rng.randrange(-300,301);value=rng.randbytes(rng.randrange(25))
                t.put(key,value);oracle[key]=value
                if step%31==0:
                    t.validate()
                    lo,hi=sorted((rng.randrange(-350,351),rng.randrange(-350,351)))
                    self.assertEqual(t.range(lo,hi),[(k,v) for k,v in sorted(oracle.items()) if lo<=k<hi])
                    self.assertEqual(BPlusIndex.loads(t.dumps()).range(),sorted(oracle.items()))
            self.assertEqual(t.size,len(oracle))

    def test_bottom_up_bulk_occupancy_for_every_small_tail(self):
        for size in (128,256,512,1024,2048,4096):
            for n in range(0,270):
                t=BPlusIndex.from_sorted(((k,b'x') for k in range(n)),size)
                self.assertEqual(t.validate()['rows'],n)
                self.assertEqual(t.range(),[(k,b'x') for k in range(n)])
                for k in (-1,n//2,n):
                    self.assertEqual(t.get(k),b'x' if 0<=k<n else None)
        for rows in ([(2,b'a'),(1,b'b')],[(1,b'a'),(1,b'b')],[None],[(1,)],[(1,b'a',0)]):
            with self.assertRaises(ValueError):BPlusIndex.from_sorted(rows)

    def test_invalid_arguments_do_not_change_index(self):
        for bad in (True,0,127,129,8192,'128',1.0):
            with self.assertRaises(ValueError):BPlusIndex(bad)
        for bad in (0,True,65536,1.0):
            with self.assertRaises(ValueError):BPlusIndex(max_pages=bad)
        t=BPlusIndex();t.put(1,b'one');before=t.dumps()
        for key in (True,1.0,None,'1',MIN_KEY-1,MAX_KEY+1,10**1000):
            with self.assertRaises(ValueError):t.put(key,b'x')
            with self.assertRaises(ValueError):t.get(key)
            if key is not None:
                with self.assertRaises(ValueError):t.range(key,None)
                with self.assertRaises(ValueError):t.range(None,key)
        for value in ('str',None,bytearray(b'x'),b'x'*25):
            with self.assertRaises(ValueError):t.put(2,value)
        self.assertEqual(t.dumps(),before)

    def test_page_budget_failure_discards_staged_split(self):
        t=BPlusIndex(max_pages=2)
        for k in (1,2,3):t.put(k,b'x')
        before=t.dumps();metrics=t.metrics()
        # Right leaf allocation fits. New root allocation fails afterwards.
        with self.assertRaisesRegex(ValueError,'page budget'):t.put(4,b'four')
        self.assertEqual(t.dumps(),before)
        self.assertEqual(t.metrics()['committed_page_images'],metrics['committed_page_images'])
        self.assertEqual(t.size,3);self.assertIsNone(t.get(4));t.validate()
        # Existing values remain replaceable at the page budget.
        t.put(2,b'new');self.assertEqual(t.get(2),b'new')

    def test_every_snapshot_prefix_and_every_single_bit_change_reject(self):
        t=BPlusIndex.from_sorted([(k,bytes([k])) for k in range(10)])
        image=t.dumps()
        for end in range(len(image)):
            with self.assertRaises(ValueError):BPlusIndex.loads(image[:end])
        for offset in range(len(image)):
            for bit in range(8):
                altered=bytearray(image);altered[offset]^=1<<bit
                with self.assertRaises(ValueError):BPlusIndex.loads(bytes(altered))
        with self.assertRaises(ValueError):BPlusIndex.loads(image+b'\0')
        with self.assertRaises(ValueError):BPlusIndex.loads(bytearray(image))
        self.assertEqual(BPlusIndex.loads(image).range(),t.range())

    def test_locally_valid_pages_can_violate_global_tree(self):
        t=BPlusIndex.from_sorted([(k,b'x') for k in range(40)])
        original=t.dumps()
        root=decode_node(t._pages.raw[t.root],128,t.root)
        left=decode_node(t._pages.raw[root.children[0]],128,root.children[0])
        leaves=[decode_node(raw,128,pid) for pid,raw in t._pages.raw.items() if decode_node(raw,128,pid).leaf]
        first=min(leaves,key=lambda n:n.keys[0]);last=max(leaves,key=lambda n:n.keys[0])
        mutations=[
            dataclasses.replace(first,next_leaf=0),
            dataclasses.replace(last,next_leaf=first.page_id),
            dataclasses.replace(root,keys=tuple(x+1 for x in root.keys)),
            dataclasses.replace(root,children=(root.children[0],)+root.children[2:]+(first.page_id,))
        ]
        offset=IMAGE_HEADER.size+CRC.size
        for node in mutations:
            image=bytearray(original);start=offset+(node.page_id-1)*128
            image[start:start+128]=encode_node(node,128)
            with self.assertRaises(ValueError):BPlusIndex.loads(bytes(image))
        # Depth mismatch and multi-page cycle have valid checksums and local shapes.
        internal=[decode_node(raw,128,pid) for pid,raw in t._pages.raw.items() if not decode_node(raw,128,pid).leaf]
        if len(internal)>1:
            child=next(x for x in internal if x.page_id!=root.page_id)
            cycle=dataclasses.replace(child,children=(root.page_id,)+child.children[1:])
            image=bytearray(original);start=offset+(child.page_id-1)*128
            image[start:start+128]=encode_node(cycle,128)
            with self.assertRaises(ValueError):BPlusIndex.loads(bytes(image))

    def test_padding_and_malicious_counts_reject_even_after_crc_repair(self):
        raw=bytearray(encode_node(Node(1,True,(2,),(b'A',)),128))
        def seal(data):
            data[-4:]=CRC.pack(zlib.crc32(data[:-4])&0xffffffff)
            return bytes(data)
        for offset,value in ((5,1),(7,255),(26,7),(100,1)):
            broken=bytearray(raw);broken[offset]=value
            with self.assertRaises(ValueError):decode_node(seal(broken),128)
        with self.assertRaises(ValueError):encode_node(Node(1,True,(2,1),(b'a',b'b')),128)
        with self.assertRaises(ValueError):encode_node(Node(1,False,(2,),children=(2,2)),128)

    def test_valid_checksum_mixed_state_does_not_imply_transaction(self):
        t=BPlusIndex.from_sorted([(k,b'old') for k in range(30)])
        old=t.dumps();old_b=BPlusIndex.loads(old)._leaf(29).page_id
        t.put(0,b'new');t.put(29,b'new');new=t.dumps()
        mixed=bytearray(new);offset=IMAGE_HEADER.size+CRC.size+(old_b-1)*128
        mixed[offset:offset+128]=old[offset:offset+128]
        accepted=BPlusIndex.loads(bytes(mixed))
        self.assertEqual((accepted.get(0),accepted.get(29)),(b'new',b'old'))
        self.assertEqual(accepted.validate()['rows'],30)

    def test_request_counters_and_file_round_trip(self):
        t=BPlusIndex.from_sorted([(k,b'x') for k in range(600)])
        height=t.validate()['height_edges'];t.reset_metrics()
        self.assertEqual(t.get(200),b'x')
        self.assertEqual(t.metrics()['page_decode_requests'],height+1)
        self.assertEqual(t.metrics()['committed_page_images'],0)
        before=t.metrics();t.validate();self.assertEqual(t.metrics(),before)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'index.mm'
            path.write_bytes(t.dumps());loaded=BPlusIndex.loads(path.read_bytes())
            self.assertEqual(loaded.range(200,211),[(k,b'x') for k in range(200,211)])


if __name__=='__main__':unittest.main(verbosity=2)
