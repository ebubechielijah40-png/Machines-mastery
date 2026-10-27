"""Actual authorized local HTTP-subset socket experiments, no network listener."""
import json,platform,socket,sys,threading
from http_subset import serve_once


def trial(request,receive_limit,send_chunk):
    client,server=socket.socketpair();client.settimeout(2);errors=[]
    def run():
        try:serve_once(server,recv_limit=receive_limit)
        except BaseException as exc:errors.append(type(exc).__name__)
    worker=threading.Thread(target=run);worker.start()
    try:
        chunks=[]
        for offset in range(0,len(request),send_chunk):
            part=request[offset:offset+send_chunk];client.sendall(part);chunks.append(len(part))
        client.shutdown(socket.SHUT_WR);answer=bytearray();receives=[]
        while True:
            part=client.recv(11)
            if not part:break
            answer.extend(part);receives.append(len(part))
    finally:client.close();worker.join(3)
    if worker.is_alive() or errors:raise RuntimeError('server thread failed: '+str(errors))
    header,body=bytes(answer).split(b'\r\n\r\n',1)
    fields=dict(line.split(b': ',1) for line in header.split(b'\r\n')[1:])
    return {'server_receive_limit':receive_limit,'client_send_chunks':chunks,'client_recv_sizes':receives,
            'status_line':header.split(b'\r\n')[0].decode('ascii'),'body_ascii':body.decode('ascii'),
            'declared_content_length':int(fields[b'Content-Length']),'actual_body_bytes':len(body)}


def main():
    good=b'GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n'
    cases={'health':good,'route_missing':good.replace(b'/health',b'/absent'),
           'method_rejected':good.replace(b'GET',b'POST'),
           'ambiguous_length':good[:-2]+b'Content-Length: 1\r\nTransfer-Encoding: chunked\r\n\r\n',
           'truncated_eof':good[:-2]}
    observations={name:trial(raw,3,2) for name,raw in cases.items()}
    observations['health_large_reads']=trial(good,256,len(good))
    print(json.dumps({'kind':'authorized local AF_UNIX HTTP subset experiment',
          'environment':{'python':sys.version,'platform':platform.platform()},
          'public_listener_created':False,'observations':observations},indent=2))

if __name__=='__main__':main()
