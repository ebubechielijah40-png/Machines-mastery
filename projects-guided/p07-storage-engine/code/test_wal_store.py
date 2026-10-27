import io
import json
from pathlib import Path
import random
import struct
import tempfile
import unittest
from unittest import mock
import zlib

from wal_store import (CHECKSUM, FILE_MAGIC, FRAME_MAGIC, HEADER, MAX_PAYLOAD,
                       CorruptionError, TornTailError, WalStore, _write_all,
                       encode_transaction, recover)


class WalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "test.wal"

    def test_empty_update_delete_unicode_and_reopen(self):
        with WalStore(self.path) as store:
            self.assertEqual(store.snapshot(), {})
            store.commit([("put", "item", "old"), ("put", "λ", "雪")])
            store.commit([("put", "item", "new"), ("delete", "missing")])
            store.commit([("delete", "item")])
            snapshot = store.snapshot()
            snapshot["λ"] = "changed externally"
            self.assertEqual(store.snapshot(), {"λ": "雪"})
        with WalStore(self.path) as store:
            self.assertEqual(store.snapshot(), {"λ": "雪"})
            self.assertEqual(store.commit([("put", "x", "1")]), 4)
        self.assertEqual(recover(self.path).transactions, 4)

    def test_every_byte_cut_preserves_prior_batch_and_atomicity(self):
        first = encode_transaction(1, [("put", "a", "10"), ("put", "b", "20")])
        second = encode_transaction(2, [("put", "a", "9"), ("put", "b", "21")])
        for cut in range(len(second)):
            with self.subTest(cut=cut):
                self.path.write_bytes(FILE_MAGIC + first + second[:cut])
                report = recover(self.path)
                self.assertEqual(report.data, {"a": "10", "b": "20"})
                self.assertEqual(report.transactions, 1)
                self.assertEqual(report.trailing_bytes, cut)
        self.path.write_bytes(FILE_MAGIC + first + second)
        self.assertEqual(recover(self.path).data, {"a": "9", "b": "21"})

    def test_incomplete_tail_requires_explicit_repair_before_append(self):
        self.path.write_bytes(FILE_MAGIC + encode_transaction(1, [("put", "a", "1")]) + b"TX")
        original = self.path.read_bytes()
        with self.assertRaises(TornTailError):
            WalStore(self.path)
        self.assertEqual(self.path.read_bytes(), original)
        with WalStore(self.path, repair_tail=True) as store:
            self.assertEqual(store.commit([("put", "b", "2")]), 2)
        report = recover(self.path)
        self.assertEqual(report.data, {"a": "1", "b": "2"})
        self.assertEqual(report.trailing_bytes, 0)

    def test_corruption_never_scans_forward_to_later_good_frames(self):
        first = encode_transaction(1, [("put", "a", "1")])
        damaged = bytearray(encode_transaction(2, [("put", "a", "2")]))
        damaged[HEADER.size + 3] ^= 1
        third = encode_transaction(3, [("put", "b", "3")])
        self.path.write_bytes(FILE_MAGIC + first + damaged + third)
        with self.assertRaisesRegex(CorruptionError, "checksum mismatch"):
            recover(self.path)
        with self.assertRaises(CorruptionError):
            WalStore(self.path, repair_tail=True)

    def test_malformed_valid_checksum_does_not_count_as_commit(self):
        payloads = [b'[["put","ok","1"],["put","bad"]]', b'{}', b'[]', b'\xff']
        for payload in payloads:
            header = HEADER.pack(FRAME_MAGIC, 1, len(payload))
            frame = header + payload + CHECKSUM.pack(zlib.crc32(header + payload))
            self.path.write_bytes(FILE_MAGIC + frame)
            with self.assertRaises(CorruptionError):
                recover(self.path)

    def test_sequence_version_size_and_magic_are_checked(self):
        for raw in (b"", b"MMWAL2\n", FILE_MAGIC + encode_transaction(2, [("delete", "x")]),
                    FILE_MAGIC + HEADER.pack(b"BAD!", 1, 0),
                    FILE_MAGIC + HEADER.pack(FRAME_MAGIC, 1, MAX_PAYLOAD + 1)):
            self.path.write_bytes(raw)
            with self.assertRaises(CorruptionError):
                recover(self.path)

    def test_input_validation_does_not_change_file(self):
        with WalStore(self.path) as store:
            before = self.path.read_bytes()
            for invalid in ([], [("wat", "x")], [("put", "x", 1)], ["put"],
                            [("put", "x", "x" * MAX_PAYLOAD)]):
                with self.assertRaises(ValueError):
                    store.commit(invalid)
                self.assertEqual(self.path.read_bytes(), before)
            self.assertEqual(store.commit([("put", "a", "1")]), 1)
        for tx in (0, -1, True, 2**64):
            with self.assertRaises(ValueError):
                encode_transaction(tx, [("delete", "x")])

    def test_sync_failure_means_unknown_outcome_and_poisoned_writer(self):
        with WalStore(self.path) as store:
            with mock.patch("wal_store.os.fsync", side_effect=OSError("injected sync failure")):
                with self.assertRaises(OSError):
                    store.commit([("put", "a", "1")])
            self.assertEqual(store.snapshot(), {})
            with self.assertRaises(RuntimeError):
                store.commit([("put", "b", "2")])
        # The kernel-visible bytes are complete despite the missing ack. This
        # observation is not evidence that a power loss would retain them.
        self.assertEqual(recover(self.path).data, {"a": "1"})

    def test_short_writes_and_no_progress(self):
        class Short(io.BytesIO):
            def write(self, data):
                return super().write(data[:2])
        stream = Short()
        _write_all(stream, b"abcdefg")
        self.assertEqual(stream.getvalue(), b"abcdefg")
        for bad in (None, 0):
            with self.assertRaises(OSError):
                _write_all(mock.Mock(write=mock.Mock(return_value=bad)), b"x")

    def test_randomized_model_matches_each_recovered_prefix(self):
        rng = random.Random(17)
        model = {}
        with WalStore(self.path) as store:
            for _ in range(100):
                batch = []
                for _ in range(rng.randrange(1, 5)):
                    key = str(rng.randrange(8))
                    if rng.randrange(3) == 0:
                        batch.append(("delete", key))
                        model.pop(key, None)
                    else:
                        value = str(rng.randrange(100))
                        batch.append(("put", key, value))
                        model[key] = value
                store.commit(batch)
                self.assertEqual(store.snapshot(), model)
                self.assertEqual(recover(self.path).data, model)


if __name__ == "__main__":
    unittest.main(verbosity=2)
