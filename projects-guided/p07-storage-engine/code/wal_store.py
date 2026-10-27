"""Original single-writer teaching WAL; not SQLite's format or a production DB.

A checksum-valid, structurally valid complete frame commits one ordered batch.
Recovery accepts a prefix and reports an incomplete final frame, never scans
past corruption. See ../LESSON.md and ../LIMITS.md before interpreting durability.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
import struct
from typing import BinaryIO, Iterable
import zlib

FILE_MAGIC = b"MMWAL1\n"
FRAME_MAGIC = b"TXN1"
HEADER = struct.Struct(">4sQI")  # frame magic, transaction id, payload bytes
CHECKSUM = struct.Struct(">I")
MAX_PAYLOAD = 1 << 20
Operation = tuple[str, ...]


class CorruptionError(ValueError):
    def __init__(self, offset: int, reason: str):
        self.offset = offset
        super().__init__(f"log corruption at byte {offset}: {reason}")


class TornTailError(ValueError):
    """Opening for append requires an explicit incomplete-tail repair decision."""


@dataclass(frozen=True)
class Recovery:
    data: dict[str, str]
    transactions: int
    valid_end: int
    trailing_bytes: int
    tail_reason: str | None


def _operations(ops: Iterable[Iterable[str]]) -> list[list[str]]:
    result = []
    for raw in ops:
        if not isinstance(raw, (list, tuple)):
            raise ValueError("operation must be a list or tuple")
        op = list(raw)
        if not op or op[0] not in ("put", "delete"):
            raise ValueError("operation must be put or delete")
        expected = 3 if op[0] == "put" else 2
        if len(op) != expected or not all(isinstance(x, str) for x in op):
            raise ValueError("put requires two strings; delete requires one string")
        result.append(op)
    if not result:
        raise ValueError("empty transactions are not represented")
    return result


def encode_transaction(tx_id: int, ops: Iterable[Iterable[str]]) -> bytes:
    if isinstance(tx_id, bool) or not isinstance(tx_id, int) or not 1 <= tx_id < 2**64:
        raise ValueError("transaction id must be a positive uint64")
    payload = json.dumps(_operations(ops), ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("transaction exceeds 1 MiB teaching limit")
    frame = HEADER.pack(FRAME_MAGIC, tx_id, len(payload)) + payload
    return frame + CHECKSUM.pack(zlib.crc32(frame))


def _apply(data: dict[str, str], ops: list[list[str]]) -> None:
    for op in ops:
        if op[0] == "put":
            data[op[1]] = op[2]
        else:
            data.pop(op[1], None)


def recover(path: str | Path) -> Recovery:
    """Read-only replay. Incomplete final bytes are reported, not silently removed.

    A checksum mismatch is corruption, even in the final frame: the reader cannot
    prove whether it was an interrupted write or damage to acknowledged data.
    """
    data: dict[str, str] = {}
    count = 0
    path = Path(path)
    with path.open("rb") as stream:
        size = os.fstat(stream.fileno()).st_size
        if stream.read(len(FILE_MAGIC)) != FILE_MAGIC:
            raise CorruptionError(0, "missing or unsupported file header")
        valid_end = len(FILE_MAGIC)
        reason = None
        while True:
            start = stream.tell()
            header = stream.read(HEADER.size)
            if not header:
                break
            if len(header) < HEADER.size:
                reason = "incomplete-header"
                break
            magic, tx_id, length = HEADER.unpack(header)
            if magic != FRAME_MAGIC:
                raise CorruptionError(start, "bad frame magic")
            if length > MAX_PAYLOAD:
                raise CorruptionError(start, "payload exceeds configured bound")
            body = stream.read(length)
            checksum = stream.read(CHECKSUM.size)
            if len(body) != length or len(checksum) != CHECKSUM.size:
                reason = "incomplete-body-or-checksum"
                break
            if CHECKSUM.unpack(checksum)[0] != zlib.crc32(header + body):
                raise CorruptionError(start, "checksum mismatch")
            if tx_id != count + 1:
                raise CorruptionError(start, "transaction sequence is not contiguous")
            try:
                raw = json.loads(body.decode("utf-8"))
                if not isinstance(raw, list):
                    raise ValueError("transaction payload must be a list")
                ops = _operations(raw)
            except (ValueError, UnicodeError) as error:
                raise CorruptionError(start, f"invalid payload: {error}") from error
            # Apply only after checking the entire transaction. A failed final
            # operation must not expose earlier operations in that batch.
            _apply(data, ops)
            count += 1
            valid_end = stream.tell()
    return Recovery(data, count, valid_end, size - valid_end, reason)


def _write_all(stream: BinaryIO, data: bytes) -> None:
    remaining = memoryview(data)
    while remaining:
        written = stream.write(remaining)
        if written is None or written <= 0:
            raise OSError("write made no progress")
        remaining = remaining[written:]


class WalStore:
    """Caller must provide exclusive ownership of this pathname and object.

    There are no locks. Two simultaneous writers or external file modification
    violate the contract. Memory reads reflect this object's committed state.
    """
    def __init__(self, path: str | Path, *, repair_tail: bool = False):
        self.path = Path(path)
        self._stream: BinaryIO | None = None
        self._poisoned = False
        try:
            with self.path.open("xb", buffering=0) as stream:
                _write_all(stream, FILE_MAGIC)
                os.fsync(stream.fileno())
        except FileExistsError:
            pass
        report = recover(self.path)
        if report.trailing_bytes and not repair_tail:
            raise TornTailError(
                f"{report.trailing_bytes} incomplete bytes after {report.valid_end}; "
                "inspect/copy log before choosing repair_tail=True")
        stream = self.path.open("r+b", buffering=0)
        try:
            if report.trailing_bytes:
                stream.truncate(report.valid_end)
                os.fsync(stream.fileno())
            stream.seek(0, os.SEEK_END)
        except BaseException:
            stream.close()
            raise
        self._stream = stream
        self._data = report.data
        self._count = report.transactions

    def snapshot(self) -> dict[str, str]:
        return self._data.copy()

    def commit(self, ops: Iterable[Iterable[str]]) -> int:
        if self._poisoned or self._stream is None:
            raise RuntimeError("store is closed or poisoned; close and recover")
        checked = _operations(ops)
        tx_id = self._count + 1
        encoded = encode_transaction(tx_id, checked)
        try:
            _write_all(self._stream, encoded)
            # File is unbuffered: fsync follows all completed OS-level writes.
            os.fsync(self._stream.fileno())
        except BaseException:
            # A failed sync does not mean the batch is absent from disk. Do not
            # retry in this object: recover first and reconcile with the caller.
            self._poisoned = True
            raise
        _apply(self._data, checked)
        self._count = tx_id
        return tx_id

    def close(self) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None

    def __enter__(self) -> WalStore:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
