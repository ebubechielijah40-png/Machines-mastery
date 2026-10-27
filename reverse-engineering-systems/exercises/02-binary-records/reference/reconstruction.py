"""Reference after discovery: independently written bounded Python encoder/decoder."""
from dataclasses import dataclass


def crc16(data):
    if type(data) is not bytes:
        raise ValueError('bytes required')
    value = 0xffff
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ (0x1021 if value & 0x8000 else 0)) & 0xffff
    return value


@dataclass(frozen=True)
class Record:
    sequence: int
    sample: int
    enabled: bool
    payload: bytes


def encode(record):
    if not isinstance(record, Record):
        raise ValueError('Record required')
    if type(record.sequence) is not int or not 0 <= record.sequence <= 65535:
        raise ValueError('uint16 sequence required')
    if type(record.sample) is not int or not -32768 <= record.sample <= 32767:
        raise ValueError('int16 sample required')
    if type(record.enabled) is not bool or type(record.payload) is not bytes or len(record.payload) > 32:
        raise ValueError('Boolean flag and bytes payload of length 0..32 required')
    word = record.sample % 65536
    body = bytes([0x4d,0x58,1,int(record.enabled),record.sequence%256,record.sequence//256,
                  word//256,word%256,len(record.payload),0]) + record.payload
    check = crc16(body)
    return body + bytes([check//256,check%256])


def decode(packet):
    if type(packet) is not bytes or not 12 <= len(packet) <= 44:
        raise ValueError('one complete bounded byte record required')
    if packet[:3] != b'MX\x01' or packet[3] not in (0,1):
        raise ValueError('magic/version/reserved-flag violation')
    length = packet[8] + 256*packet[9]
    if length > 32 or len(packet) != 12 + length:
        raise ValueError('length/payload boundary violation')
    if crc16(packet[:-2]) != 256*packet[-2] + packet[-1]:
        raise ValueError('checksum mismatch')
    sequence = packet[4] + 256*packet[5]
    word = 256*packet[6] + packet[7]
    sample = word if word < 32768 else word - 65536
    return Record(sequence,sample,bool(packet[3]),packet[10:-2])
