import binascii
import importlib.util
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from oracle import compile_oracle, query
BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('binary_reconstruction', BASE/'reference/reconstruction.py')
module = importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
Record, encode, decode, crc16 = module.Record,module.encode,module.decode,module.crc16


class BinaryRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp.name)/'oracle'
        compile_oracle(cls.binary)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_crc_fixed_value_and_independent_library(self):
        self.assertEqual(crc16(b'123456789'), 0x29b1)
        rng=random.Random(828)
        for length in range(100):
            data=bytes(rng.randrange(256) for _ in range(length))
            self.assertEqual(crc16(data), binascii.crc_hqx(data,0xffff))

    def test_ordinary_endian_signed_and_payload_edges(self):
        for sequence in (0,1,255,256,0x1234,65535):
            for sample in (-32768,-1,0,1,32767):
                for payload in (b'',b'\x00\xff',bytes(range(32))):
                    record=Record(sequence,sample,True,payload)
                    packet=query(self.binary,sequence,sample,True,payload)
                    self.assertEqual(encode(record),packet)
                    self.assertEqual(decode(packet),record)
        packet=encode(Record(0x1234,-2,False,b''))
        self.assertEqual(packet[4:8],b'\x34\x12\xff\xfe')

    def test_native_python_random_differential(self):
        rng=random.Random(72411)
        for _ in range(200):
            record=Record(rng.randrange(65536),rng.randrange(-32768,32768),bool(rng.randrange(2)),bytes(rng.randrange(256) for _ in range(rng.randrange(33))))
            native=query(self.binary,record.sequence,record.sample,record.enabled,record.payload)
            self.assertEqual(native,encode(record));self.assertEqual(decode(native),record)

    def test_every_truncation_and_trailing_byte(self):
        packet=encode(Record(256,-1,True,bytes(range(32))))
        for cut in range(len(packet)):
            with self.assertRaises(ValueError):decode(packet[:cut])
        for suffix in (b'\x00',packet):
            with self.assertRaises(ValueError):decode(packet+suffix)

    def test_every_single_bit_mutation_rejected(self):
        packet=encode(Record(257,-123,True,b'payload'))
        for index in range(len(packet)):
            for bit in range(8):
                changed=bytearray(packet);changed[index]^=1<<bit
                with self.assertRaises(ValueError):decode(bytes(changed))

    def test_recomputed_crc_does_not_make_semantics_valid(self):
        packet=bytearray(encode(Record(0,0,False,b'')))
        for index,value in ((0,0),(2,2),(3,2),(8,33),(9,1)):
            changed=bytearray(packet);changed[index]=value
            check=crc16(bytes(changed[:-2]));changed[-2:]=bytes([check//256,check%256])
            with self.assertRaises(ValueError):decode(bytes(changed))
        # A forged valid payload is accepted: checksum is not authentication.
        forged=encode(Record(0,1,False,b''))
        self.assertEqual(decode(forged).sample,1)

    def test_schema_validation(self):
        for record in (Record(True,0,False,b''),Record(0,32768,False,b''),Record(0,0,1,b''),Record(0,0,False,b'a'*33),Record(0,0,False,bytearray())):
            with self.assertRaises(ValueError):encode(record)
        for packet in ('MX',bytearray(12),None,b''):
            with self.assertRaises(ValueError):decode(packet)

    def test_native_rejection_and_sanitized_build(self):
        for args in [('65536','0','0',''),('0','-32769','0',''),('0','0','2',''),('0','0','0','zz'),('0','0','0','0')]:
            self.assertEqual(subprocess.run([str(self.binary),*args],capture_output=True,timeout=2).returncode,2)
        binary=Path(self.temp.name)/'sanitized'
        compile_oracle(binary,('-O1','-fsanitize=undefined','-fno-sanitize-recover=all'))
        self.assertEqual(query(binary,65535,-32768,True,bytes(range(32))),encode(Record(65535,-32768,True,bytes(range(32)))))


if __name__=='__main__':unittest.main(verbosity=2)
