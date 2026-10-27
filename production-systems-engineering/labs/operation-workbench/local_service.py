"""Serial loopback release rehearsal; trusted local clients only.

The mutant intentionally returns a current counter for a duplicate response.
Neither release is an authenticated internet service. HTTP parsing is delegated
to Python's basic http.server. This server never binds a public interface.
"""
import argparse
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import sqlite3
from operations import Conflict,OperationStore,validate_request


def strict_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('duplicate JSON field')
        out[k]=v
    return out


def serve(path,release):
    store=OperationStore(path)
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup();self.connection.settimeout(1)
        def log_message(self,*args):pass
        def reply(self,status,payload):
            raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode('ascii')
            self.send_response(status);self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            self.close_connection=True
        def do_GET(self):
            if self.path!='/ready':return self.reply(404,{'error':'route'})
            try:
                state=store.snapshot()
                self.reply(200,dict(release=release,counter=state['counter'],operations=len(state['operations'])))
            except sqlite3.Error:self.reply(503,{'error':'storage'})
        def do_POST(self):
            if self.path!='/op':return self.reply(404,{'error':'route'})
            try:
                lengths=self.headers.get_all('Content-Length',[])
                if len(lengths)!=1 or self.headers.get('Transfer-Encoding') is not None:
                    raise ValueError('one explicit body length required')
                text=lengths[0]
                if not text.isascii() or not text.isdecimal() or len(text)>3 or not 1<=int(text)<=512:
                    raise ValueError('body length must lie in1..512')
                raw=self.rfile.read(int(text))
                if len(raw)!=int(text):raise ValueError('truncated body')
                obj=json.loads(raw,object_pairs_hook=strict_object)
                if type(obj) is not dict or set(obj)!={'request_id','delta'}:raise ValueError('exact operation schema required')
                validate_request(obj['request_id'],obj['delta'])
                result,duplicate=store.apply(obj['request_id'],obj['delta'])
                if release=='mutant-current-response' and duplicate:
                    result=store.snapshot()['counter']
                self.reply(200,dict(result=result,duplicate=duplicate,release=release))
            except Conflict:self.reply(409,{'error':'identity_conflict'})
            except (ValueError,UnicodeError):self.reply(400,{'error':'schema'})
            except sqlite3.Error:self.reply(503,{'error':'storage'})
    with HTTPServer(('127.0.0.1',0),Handler) as server:
        print(json.dumps(dict(port=server.server_port,release=release)),flush=True)
        server.serve_forever(poll_interval=.05)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path');parser.add_argument('--release',choices=['stable-v1','mutant-current-response'],default='stable-v1')
    args=parser.parse_args();serve(args.path,args.release)
