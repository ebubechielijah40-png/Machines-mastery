"""Local teaching endpoint for a deliberately strict HTTP/1.1 GET subset.

Not a conformant general HTTP server: no chunked input, persistence, proxying,
TLS, dates/cache negotiation or broad authority syntax. Tests use socketpair.
"""
import re
import socket
import math
import time

MAX_HEADERS=4096

class BadRequest(ValueError):pass


def parse_request(raw):
    if not isinstance(raw,bytes):raise TypeError('wire request must be bytes')
    if len(raw)>MAX_HEADERS:raise BadRequest('header byte limit exceeded')
    boundary=raw.find(b'\r\n\r\n')
    if boundary<0:raise BadRequest('incomplete header section')
    if boundary+4!=len(raw):raise BadRequest('bodies/pipelined bytes not supported')
    header=raw[:boundary]
    # Delimit bytes before text interpretation. Reject controls, obs-fold and
    # bare line endings rather than normalize competing interpretations.
    lines=header.split(b'\r\n')
    try:text=[line.decode('ascii') for line in lines]
    except UnicodeError as exc:raise BadRequest('ASCII header subset only') from exc
    if any(any(ord(c)<32 or ord(c)==127 for c in line) for line in text):raise BadRequest('control character in line')
    parts=text[0].split(' ')
    if len(parts)!=3 or not all(parts) or parts[2]!='HTTP/1.1':raise BadRequest('unsupported request line')
    method,target,_=parts
    if re.fullmatch(r'[A-Z]+',method) is None or not target.startswith('/'):
        raise BadRequest('unsupported method/target syntax')
    headers={}
    for line in text[1:]:
        if ':' not in line:raise BadRequest('field without colon')
        name,value=line.split(':',1)
        if re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+",name) is None:raise BadRequest('invalid field name/leading whitespace')
        name=name.lower();value=value.strip(' ')
        if name in headers:raise BadRequest('duplicate fields unsupported')
        headers[name]=value
    if headers.get('host')!='localhost':raise BadRequest('exactly one Host: localhost required')
    if 'transfer-encoding' in headers:raise BadRequest('transfer coding unsupported in this teaching subset')
    if headers.get('content-length','0')!='0':raise BadRequest('request bodies unsupported')
    if 'expect' in headers:raise BadRequest('expectation handshake unsupported')
    return method,target,headers


def response(status,body):
    reasons={200:'OK',400:'Bad Request',404:'Not Found',405:'Method Not Allowed'}
    header=(f'HTTP/1.1 {status} {reasons[status]}\r\nContent-Length: {len(body)}\r\n'
            'Content-Type: text/plain; charset=utf-8\r\nConnection: close\r\n')
    if status==405:header+='Allow: GET\r\n'
    return header.encode('ascii')+b'\r\n'+body


def serve_once(conn,*,recv_limit=256,timeout=1):
    """One local connection, bounded header collection, always close afterwards."""
    try:
        return _serve_once(conn,recv_limit=recv_limit,timeout=timeout)
    finally:
        conn.close()


def _serve_once(conn,*,recv_limit,timeout):
    if type(recv_limit) is not int or recv_limit<1 or not isinstance(timeout,(int,float)) or not math.isfinite(timeout) or timeout<=0:
        raise ValueError('positive receive limit and finite positive timeout required')
    deadline=time.monotonic()+timeout
    try:
        raw=bytearray()
        while b'\r\n\r\n' not in raw:
            remaining=MAX_HEADERS-len(raw)
            if remaining<=0:raise BadRequest('header byte budget exhausted')
            remaining_time=deadline-time.monotonic()
            if remaining_time<=0:raise TimeoutError('absolute header deadline')
            conn.settimeout(remaining_time)
            chunk=conn.recv(min(recv_limit,remaining))
            if not chunk:raise BadRequest('EOF before complete request')
            raw.extend(chunk)
        method,target,headers=parse_request(bytes(raw))
        if method!='GET':answer=response(405,b'GET required\n')
        elif target!='/health':answer=response(404,b'unknown resource\n')
        else:answer=response(200,b'ready\n')
    except (BadRequest,TimeoutError):
        answer=response(400,b'invalid or unsupported request\n')
    conn.settimeout(timeout)
    conn.sendall(answer)
    return answer
