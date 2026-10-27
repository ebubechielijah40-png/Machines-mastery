from pathlib import Path
import tempfile
import unittest
from unittest import mock

from bplus import BPlusIndex
from rebuild import rebuild_from_log,wal_module


class RebuildTests(unittest.TestCase):
    def test_every_log_cut_rebuilds_only_complete_transaction_states(self):
        wal=wal_module()
        frames=[wal.encode_transaction(1,[('put','0','old'),('put','29','old')]),
                wal.encode_transaction(2,[('put','0','new'),('put','29','new')]),
                wal.encode_transaction(3,[('delete','0'),('put','-2','é')])]
        image=wal.FILE_MAGIC+b''.join(frames)
        ends=[len(wal.FILE_MAGIC)+sum(len(f) for f in frames[:i]) for i in range(1,4)]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'source.wal'
            for cut in range(len(wal.FILE_MAGIC),len(image)+1):
                path.write_bytes(image[:cut]);tree,report=rebuild_from_log(path)
                if cut>=ends[2]:expected=[(-2,'é'.encode()),(29,b'new')]
                elif cut>=ends[1]:expected=[(0,b'new'),(29,b'new')]
                elif cut>=ends[0]:expected=[(0,b'old'),(29,b'old')]
                else:expected=[]
                self.assertEqual(tree.range(),expected)
                self.assertEqual(report['transactions'],sum(end<=cut for end in ends))
                self.assertEqual(path.read_bytes(),image[:cut])

    def test_rebuild_numeric_order_subset_and_corruption_contract(self):
        wal=wal_module()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'data.wal'
            with wal.WalStore(path) as store:
                store.commit([('put','10','ten'),('put','2','two'),('put','-1','negative')])
            tree,report=rebuild_from_log(path)
            self.assertEqual(tree.range(),[(-1,b'negative'),(2,b'two'),(10,b'ten')])
            self.assertEqual(report['transactions'],1)
            damaged=bytearray(path.read_bytes());damaged[-1]^=1;path.write_bytes(damaged)
            with self.assertRaises(wal.CorruptionError):rebuild_from_log(path)
        for key,value in [('01','x'),('+1','x'),('-0','x'),('word','x'),('1_0','x'),('1','x'*25),('1','é'*13)]:
            report=wal.Recovery({key:value},1,1,0,None)
            with mock.patch.object(wal,'recover',return_value=report):
                with self.assertRaises(ValueError):rebuild_from_log('not-opened')

    def test_authority_rebuild_ignores_an_accepted_stale_index(self):
        wal=wal_module()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'data.wal'
            with wal.WalStore(path) as store:
                store.commit([('put','1','before')])
                old,_=rebuild_from_log(path);stale=old.dumps()
                store.commit([('put','1','after'),('put','2','extra')])
            self.assertEqual(BPlusIndex.loads(stale).get(1),b'before')
            current,report=rebuild_from_log(path)
            self.assertEqual(current.range(),[(1,b'after'),(2,b'extra')])
            self.assertEqual(report['transactions'],2)


if __name__=='__main__':unittest.main(verbosity=2)
