import socket,threading,unittest
from unittest import mock
from http_subset import BadRequest,MAX_HEADERS,parse_request,response,serve_once

GOOD=b'GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n'

class HttpSubsetTests(unittest.TestCase):
    def test_literal_request_and_literal_response_boundary(self):
        self.assertEqual(parse_request(GOOD)[:2],('GET','/health'))
        reply=response(200,b'ready\n');header,body=reply.split(b'\r\n\r\n',1)
        self.assertEqual(body,b'ready\n');self.assertIn(b'Content-Length: 6',header)
    def test_all_truncations_reject_until_complete(self):
        for cut in range(len(GOOD)):
            with self.assertRaises(BadRequest):parse_request(GOOD[:cut])
    def test_ambiguous_message_borders_and_duplicate_host_reject(self):
        for extra in [b'Content-Length: 1\r\n',b'Content-Length: 0\r\nContent-Length: 0\r\n',
                      b'Transfer-Encoding: chunked\r\n',b'Host: localhost\r\n',b' Host: localhost\r\n',
                      b'Host : localhost\r\n',b'Expect: 100-continue\r\n']:
            with self.assertRaises(BadRequest):parse_request(GOOD[:-2]+extra+b'\r\n')
        with self.assertRaises(BadRequest):parse_request(GOOD+GOOD)
    def test_controls_bare_lf_nonascii_and_resource_limit(self):
        for raw in [GOOD.replace(b'\r\n',b'\n'),GOOD.replace(b'/health',b'/he\tal'),
                    GOOD.replace(b'localhost',b'local\xffhost'),b'X'*(MAX_HEADERS+1)]:
            with self.assertRaises(BadRequest):parse_request(raw)
    def exchange(self,request,chunk_size=1):
        client,server=socket.socketpair();client.settimeout(2)
        thread=threading.Thread(target=serve_once,args=(server,),kwargs={'recv_limit':3})
        thread.start()
        try:
            for offset in range(0,len(request),chunk_size):client.sendall(request[offset:offset+chunk_size])
            client.shutdown(socket.SHUT_WR);parts=[]
            while True:
                chunk=client.recv(64)
                if not chunk:break
                parts.append(chunk)
            return b''.join(parts)
        finally:client.close();thread.join(2);self.assertFalse(thread.is_alive())
    def test_actual_fragmented_socket_request(self):
        reply=self.exchange(GOOD)
        self.assertEqual(reply,response(200,b'ready\n'))
    def test_actual_unknown_route_and_method(self):
        self.assertTrue(self.exchange(GOOD.replace(b'/health',b'/missing'),5).startswith(b'HTTP/1.1 404'))
        self.assertTrue(self.exchange(GOOD.replace(b'GET',b'POST'),7).startswith(b'HTTP/1.1 405'))
    def test_absolute_header_deadline_not_reset_by_partial_bytes(self):
        class FakeConnection:
            def __init__(self):self.receives=0;self.answer=None;self.closed=False
            def settimeout(self,t):pass
            def recv(self,n):self.receives+=1;return b'G'
            def sendall(self,raw):self.answer=raw
            def close(self):self.closed=True
        conn=FakeConnection()
        with mock.patch('http_subset.time.monotonic',side_effect=[0,.1,1.1]):serve_once(conn)
        self.assertEqual(conn.receives,1);self.assertTrue(conn.answer.startswith(b'HTTP/1.1 400'));self.assertTrue(conn.closed)
    def test_invalid_configuration_closes_owned_socket(self):
        for limit,timeout in [(0,1),(3,0),(3,float('nan'))]:
            a,b=socket.socketpair()
            try:
                with self.assertRaises(ValueError):serve_once(a,recv_limit=limit,timeout=timeout)
                self.assertEqual(a.fileno(),-1)
            finally:a.close();b.close()
    def test_actual_eof_inside_headers_is_error(self):
        self.assertTrue(self.exchange(GOOD[:-2]).startswith(b'HTTP/1.1 400'))
    def test_receive_and_send_failures_close_owned_connection(self):
        for failure in ('recv','sendall'):
            conn=mock.Mock()
            conn.recv.return_value=GOOD
            getattr(conn,failure).side_effect=ConnectionResetError('injected local transport failure')
            with self.assertRaises(ConnectionResetError):serve_once(conn)
            conn.close.assert_called_once_with()

if __name__=='__main__':unittest.main(verbosity=2)
