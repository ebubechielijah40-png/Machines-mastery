"""Bounded incremental length framing over a byte stream.

Frame: four network-order length bytes followed by that many payload bytes.
Only incomplete-frame storage is bounded by max_size+4; caller input and returned
payload lists have separate ownership/budgets. A protocol failure is terminal.
"""
from __future__ import annotations
import struct

MAX_SIZE = 1_000_000

class ProtocolError(ValueError):
    pass

class TruncatedFrame(ProtocolError):
    pass


def encode(payload: bytes) -> bytes:
    if not isinstance(payload, bytes):
        raise TypeError('payload must be immutable bytes')
    if len(payload) > MAX_SIZE:
        raise ValueError('payload too large')
    return struct.pack('!I',len(payload))+payload


class Decoder:
    def __init__(self,max_size=MAX_SIZE):
        if type(max_size) is not int or not 0 <= max_size <= MAX_SIZE:
            raise ValueError('max_size must be an integer between zero and MAX_SIZE')
        self.buf=bytearray()
        self.max=max_size
        self.expected=None
        self.state='OPEN'
        self.peak_pending=0

    def _fail(self,reason,kind=ProtocolError):
        self.state='FAILED'
        self.buf.clear()
        self.expected=None
        raise kind(reason)

    def feed(self,data:bytes):
        if self.state!='OPEN':
            raise ProtocolError('decoder is '+self.state+'; create a new connection decoder')
        if not isinstance(data,bytes):
            raise TypeError('feed requires immutable bytes')
        view=memoryview(data)
        offset=0
        out=[]
        while offset<len(view):
            target=4 if self.expected is None else 4+self.expected
            take=min(target-len(self.buf),len(view)-offset)
            self.buf.extend(view[offset:offset+take]); offset+=take
            self.peak_pending=max(self.peak_pending,len(self.buf))
            if self.expected is None and len(self.buf)==4:
                self.expected=struct.unpack('!I',self.buf)[0]
                if self.expected>self.max:
                    self._fail('declared frame exceeds configured byte budget')
            if self.expected is not None and len(self.buf)==4+self.expected:
                out.append(bytes(self.buf[4:]))
                self.buf.clear(); self.expected=None
        return out

    def finish(self):
        """Signal transport EOF. Clean boundary closes; partial frame poisons."""
        if self.state=='CLOSED':
            return
        if self.state!='OPEN':
            raise ProtocolError('decoder is '+self.state)
        if self.buf:
            self._fail('EOF inside frame: '+str(len(self.buf))+' pending bytes',TruncatedFrame)
        self.state='CLOSED'
