from __future__ import annotations
import struct

def encode(payload: bytes) -> bytes:
    if len(payload) > 1_000_000: raise ValueError('payload too large')
    return struct.pack('!I',len(payload))+payload

class Decoder:
    def __init__(self,max_size=1_000_000): self.buf=bytearray(); self.max=max_size
    def feed(self,data:bytes):
        self.buf.extend(data); out=[]
        while len(self.buf)>=4:
            n=struct.unpack('!I',self.buf[:4])[0]
            if n>self.max: raise ValueError('frame too large')
            if len(self.buf)<4+n: break
            out.append(bytes(self.buf[4:4+n])); del self.buf[:4+n]
        return out
