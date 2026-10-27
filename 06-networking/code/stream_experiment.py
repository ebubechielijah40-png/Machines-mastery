"""Actual local kernel observations; no claim about IP packets or Internet TCP."""
import json,platform,socket,sys
from collections import Counter
from framing import Decoder,encode


def main():
    wire=encode(b'alpha')+encode(b'')+encode(b'beta'*20)
    observations=[]
    for receive_limit in [1,3,7,64]:
        a,b=socket.socketpair()
        try:
            a.settimeout(1);b.settimeout(1)
            sends=[]
            for offset in range(0,len(wire),5):
                chunk=wire[offset:offset+5];a.sendall(chunk);sends.append(len(chunk))
            a.shutdown(socket.SHUT_WR)
            d=Decoder(100); payloads=[];reads=[]
            while True:
                chunk=b.recv(receive_limit)
                if not chunk:break
                reads.append(len(chunk));payloads.extend(d.feed(chunk))
            d.finish()
            observations.append({'receive_limit':receive_limit,'application_send_chunks':sends,
                'recv_sizes':reads,'decoded_lengths':[len(x) for x in payloads],
                'payloads_equal_expected':payloads==[b'alpha',b'',b'beta'*20],
                'peak_incomplete_storage':d.peak_pending,'state_after_eof':d.state})
        finally:a.close();b.close()
    a,b=socket.socketpair()
    try:
        a.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096);a.setblocking(False)
        remaining=memoryview(b'x'*(1<<20));sent=[];blocked=False
        for _ in range(2048):
            try:n=a.send(remaining)
            except BlockingIOError:blocked=True;break
            sent.append(n);remaining=remaining[n:]
            if not remaining:break
        pressure={'requested_send_buffer':4096,'kernel_reported_send_buffer':a.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF),
                  'send_returns':sent,'bytes_accepted_before_reader':sum(sent),'blocking_error_observed':blocked,
                  'remaining_application_bytes':len(remaining)}
    finally:a.close();b.close()
    print(json.dumps({'kind':'authorized local AF_UNIX SOCK_STREAM observation',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'framing':observations,'backpressure':pressure},indent=2))


if __name__=='__main__':main()
