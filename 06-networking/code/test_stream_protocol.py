"""Independent byte vectors, bounded storage, socket stream and EOF contracts."""
import itertools
import socket
import unittest
from framing import Decoder, ProtocolError, TruncatedFrame, encode


class StreamTests(unittest.TestCase):
    def test_fixed_wire_vector_and_empty_payload(self):
        self.assertEqual(encode(b'ABC'),b'\x00\x00\x00\x03ABC')
        d=Decoder(); self.assertEqual(d.feed(b'\0\0\0\0'),[b''])
        d.finish(); self.assertEqual(d.state,'CLOSED')

    def test_every_two_cut_partition_is_same_messages(self):
        wire=b'\0\0\0\2AB\0\0\0\0\0\0\0\1Z'
        for a in range(len(wire)+1):
            for b in range(a,len(wire)+1):
                d=Decoder(2);result=[]
                for part in [wire[:a],wire[a:b],wire[b:]]:result.extend(d.feed(part))
                d.finish(); self.assertEqual(result,[b'AB',b'',b'Z'])

    def test_all_byte_cuts_distinguish_boundary_from_truncation(self):
        wire=encode(b'abc')+encode(b'xy')
        for cut in range(len(wire)+1):
            d=Decoder(); d.feed(wire[:cut])
            if cut in [0,7,len(wire)]: d.finish(); self.assertEqual(d.state,'CLOSED')
            else:
                with self.assertRaises(TruncatedFrame):d.finish()
                self.assertEqual(d.state,'FAILED')

    def test_overflow_is_terminal_before_body_copy(self):
        d=Decoder(3)
        with self.assertRaises(ProtocolError): d.feed(b'\0\0\0\4'+b'x'*10000)
        self.assertEqual(d.state,'FAILED'); self.assertLessEqual(d.peak_pending,4)
        self.assertEqual(d.buf,bytearray())
        with self.assertRaises(ProtocolError):d.feed(encode(b'ok'))
        with self.assertRaises(ProtocolError):d.finish()

    def test_coalesced_frames_do_not_accumulate_incomplete_storage(self):
        d=Decoder(10); messages=d.feed(encode(b'x'*10)*10000)
        self.assertEqual(len(messages),10000); self.assertLessEqual(d.peak_pending,14)
        d.finish()

    def test_api_errors_do_not_consume_a_stream(self):
        for maximum in [True,-1,1_000_001,.5]:
            with self.assertRaises(ValueError):Decoder(maximum)
        d=Decoder()
        with self.assertRaises(TypeError):d.feed('text')
        self.assertEqual(d.feed(encode(b'ok')),[b'ok'])
        d.finish(); d.finish()
        with self.assertRaises(ProtocolError):d.feed(b'')

    def test_local_socket_half_close_preserves_remaining_frames(self):
        sender,receiver=socket.socketpair()
        try:
            sender.settimeout(1);receiver.settimeout(1)
            wire=encode(b'first')+encode(b'second')
            for i in range(0,len(wire),2):sender.sendall(wire[i:i+2])
            sender.shutdown(socket.SHUT_WR)
            d=Decoder();messages=[]
            while True:
                chunk=receiver.recv(3)
                if not chunk:break
                messages.extend(d.feed(chunk))
            d.finish();self.assertEqual(messages,[b'first',b'second'])
            receiver.sendall(b'ack');self.assertEqual(sender.recv(3),b'ack')
        finally:sender.close();receiver.close()

    def test_short_nonblocking_send_and_backpressure_are_handled(self):
        sender,receiver=socket.socketpair()
        try:
            sender.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096)
            sender.setblocking(False)
            remaining=memoryview(b'x'*(1<<20));total=0;blocked=False
            for attempt in range(2048):
                try:sent=sender.send(remaining)
                except BlockingIOError:blocked=True;break
                self.assertGreater(sent,0);total+=sent;remaining=remaining[sent:]
                if not remaining:break
            self.assertGreater(total,0)
            self.assertTrue(blocked,'bounded local sender should fill without reader')
            self.assertLess(total,1<<20)
            receiver.settimeout(1); received=0
            while received<total:received+=len(receiver.recv(min(total-received,8192)))
            self.assertEqual(received,total)
        finally:sender.close();receiver.close()


if __name__=='__main__':unittest.main(verbosity=2)
