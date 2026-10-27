from itertools import product
import struct
import unittest
from elf_plan import HEADER,PHDR,MAX_MEMORY,parse,materialize,read
from memory_models import SetCache,Mapping,nested_translate,TranslationFault


def fixture(**overrides):
    values=dict(typ=1,flags=5,offset=128,virtual=4224,physical=0,file_size=4,memory_size=8,alignment=4096)
    values.update(overrides)
    header=HEADER.pack(b'\x7fELF\x02\x01\x01'+bytes(9),2,62,1,4224,64,0,0,64,56,1,0,0,0)
    ph=PHDR.pack(*(values[k] for k in ('typ','flags','offset','virtual','physical','file_size','memory_size','alignment')))
    return header+ph+bytes(128-len(header)-len(ph))+b'ABCD'


class ElfTests(unittest.TestCase):
    def test_worked_image_zero_tail_and_permissions(self):
        raw=fixture();plan=parse(raw);image=materialize(raw,plan)
        self.assertEqual(read(image,4224,8),b'ABCD\0\0\0\0')
        self.assertEqual(read(image,4224,4,'x'),b'ABCD')
        with self.assertRaises(PermissionError):read(image,4224,1,'w')
        with self.assertRaises(MemoryError):read(image,4231,2)

    def test_sizes_alignment_permissions_and_resource_failures(self):
        for changes in [dict(file_size=9),dict(offset=130),dict(alignment=3),
                        dict(flags=7),dict(flags=8),dict(memory_size=MAX_MEMORY+1),
                        dict(virtual=(1<<64)-4096,memory_size=8192)]:
            with self.subTest(changes=changes),self.assertRaises(ValueError):parse(fixture(**changes))
        for raw in [b'',fixture()[:119],b'BAD!'+fixture()[4:]]:
            with self.assertRaises(ValueError):parse(raw)
        with self.assertRaises(ValueError):parse(fixture(),bias=4096)
        with self.assertRaises(ValueError):parse(fixture(),bias=True)

    def test_table_bounds_and_unsupported_encoding(self):
        for offset,fmt,value in [(32,'Q',10**6),(54,'H',55),(56,'H',0),(56,'H',129),(18,'H',183)]:
            raw=bytearray(fixture());struct.pack_into('<'+fmt,raw,offset,value)
            with self.assertRaises(ValueError):parse(bytes(raw))
        for offset in (4,5,6):
            raw=bytearray(fixture());raw[offset]=0
            with self.assertRaises(ValueError):parse(bytes(raw))

    def test_dynamic_bias_is_address_not_relocation_execution(self):
        raw=bytearray(fixture());struct.pack_into('<H',raw,16,3);raw=bytes(raw)
        plan=parse(raw,bias=0x10000000);image=materialize(raw,plan)
        self.assertEqual(plan.entry,0x10000000+4224)
        self.assertEqual(read(image,plan.entry,8),b'ABCD\0\0\0\0')
        with self.assertRaises(MemoryError):read(image,4224,1)

    def test_interpreter_is_recorded_not_opened_and_reparsed_plan(self):
        raw=bytearray(fixture());raw[56:58]=(2).to_bytes(2,'little')
        # Two headers followed by interpreter text and the original four bytes.
        interp=b'/not/executed\0';offset=64+112
        header=bytes(raw[:64]);text=PHDR.pack(3,4,offset,0,0,len(interp),len(interp),1)
        load_off=256;load=PHDR.pack(1,5,load_off,4096+load_off,0,4,8,4096)
        header=bytearray(header);struct.pack_into('<Q',header,24,4096+load_off)
        data=bytes(header)+text+load+interp
        data+=bytes(load_off-len(data))+b'ABCD'
        plan=parse(data);self.assertEqual(plan.interpreter,'/not/executed')
        from dataclasses import replace
        with self.assertRaises(ValueError):materialize(data,replace(plan,entry=1))


class MemoryTests(unittest.TestCase):
    def test_conflict_worked_trace_and_capacity(self):
        direct=SetCache(sets=4,ways=1,line_bytes=16)
        self.assertEqual([direct.access(a)['hit'] for a in [0,64,0,64]], [False]*4)
        associative=SetCache(sets=4,ways=2,line_bytes=16)
        self.assertEqual([associative.access(a)['hit'] for a in [0,64,0,64]],[False,False,True,True])
        sequential=SetCache(sets=4,ways=1,line_bytes=16)
        for a in range(64):sequential.access(a)
        self.assertEqual((sequential.hits,sequential.misses),(60,4))

    def test_lru_against_distinct_since_last_reference_oracle(self):
        cases=0
        for trace in product(range(4),repeat=5):
            cache=SetCache(sets=2,ways=2,line_bytes=4);history=[]
            for block in trace:
                candidates=[i for i,b in enumerate(history) if b==block]
                if not candidates:expected=False
                else:
                    since=history[candidates[-1]+1:]
                    same_set={b for b in since if b%2==block%2}
                    expected=len(same_set)<2
                self.assertEqual(cache.access(block*4)['hit'],expected)
                history.append(block)
            cases+=1
        self.assertEqual(cases,1024)

    def test_nested_translation_affine_oracle_all_offsets(self):
        guest={p:Mapping((7*p+3)%16,frozenset('rwx')) for p in range(8)}
        host={p:Mapping((11*p+9)%32,frozenset('rw')) for p in range(16)}
        for page in range(8):
            for offset in range(256):
                observed=nested_translate(page*256+offset,guest,host,permission='w')
                self.assertEqual(observed['host_physical'],((11*((7*page+3)%16)+9)%32)*256+offset)
                self.assertEqual(observed['permissions'],'rw')
        with self.assertRaisesRegex(TranslationFault,'host permission'):nested_translate(0,guest,host,permission='x')

    def test_translation_fault_stage_and_remapping(self):
        guest={1:Mapping(3,frozenset('rw'))};host={3:Mapping(9,frozenset('r'))}
        self.assertEqual(nested_translate(257,guest,host)['host_physical'],2305)
        with self.assertRaisesRegex(TranslationFault,'guest page'):nested_translate(0,guest,host)
        with self.assertRaisesRegex(TranslationFault,'guest permission'):nested_translate(257,guest,host,permission='x')
        with self.assertRaisesRegex(TranslationFault,'host permission'):nested_translate(257,guest,host,permission='w')
        with self.assertRaisesRegex(TranslationFault,'host mapping'):nested_translate(257,guest,{})
        old=nested_translate(257,guest,host)
        host[3]=Mapping(10,frozenset('r'))
        self.assertEqual(nested_translate(257,guest,host)['host_physical'],2561)
        self.assertNotEqual(old['host_physical'],2561)  # A cached old composition is stale.

    def test_bounded_contracts(self):
        for kwargs in [dict(sets=True),dict(ways=0),dict(line_bytes=3),dict(sets=128)]:
            with self.assertRaises(ValueError):SetCache(**kwargs)
        cache=SetCache()
        for a in (True,-1,1<<32):
            with self.assertRaises(ValueError):cache.access(a)
        for _ in range(10000):cache.access(0)
        with self.assertRaises(ValueError):cache.access(0)
        for frame,permissions in [(True,frozenset('r')),(256,frozenset('r')),(1,set('r')),(1,frozenset())]:
            with self.assertRaises(ValueError):Mapping(frame,permissions)


if __name__=='__main__':unittest.main(verbosity=2)
