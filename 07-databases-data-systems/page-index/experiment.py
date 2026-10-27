"""Run controlled synthetic page-work and non-atomic snapshot experiments."""
import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import platform
import random
import sys
import tempfile
import time

from bplus import BPlusIndex, decode_node, encode_node, IMAGE_HEADER, CRC, capacities

HERE=Path(__file__).resolve().parent


def run():
    n=4096
    rng=random.Random(4081)
    shuffled=list(range(n));rng.shuffle(shuffled)
    runs=[]
    for page_size in (128,256,512,1024):
        for method,keys in [('ascending',range(n)),('shuffled',shuffled),('bulk',range(n))]:
            begin=time.perf_counter()
            if method=='bulk':t=BPlusIndex.from_sorted(((k,str(k).encode()) for k in keys),page_size)
            else:
                t=BPlusIndex(page_size)
                for k in keys:t.put(k,str(k).encode())
            elapsed=time.perf_counter()-begin
            build=t.metrics();shape=t.validate();image=t.dumps()
            with tempfile.TemporaryDirectory() as directory:
                path=Path(directory)/'pages.mm';path.write_bytes(image)
                recovered=BPlusIndex.loads(path.read_bytes())
                assert recovered.range()==[(k,str(k).encode()) for k in range(n)]
            t.reset_metrics()
            queries=[(i*41)%n for i in range(100)]+[-1,n]
            for k in queries:assert t.get(k)==(str(k).encode() if 0<=k<n else None)
            points=t.metrics()
            t.reset_metrics();selected=t.range(2000,2100)
            assert selected==[(k,str(k).encode()) for k in range(2000,2100)]
            window=t.metrics()
            t.reset_metrics();all_rows=t.range();assert len(all_rows)==n
            scan=t.metrics()
            runs.append(dict(page_size=page_size,capacities=capacities(page_size),method=method,
                             build_seconds=elapsed,build=build,shape=shape,snapshot_bytes=len(image),
                             point_queries=102,point_page_requests=points['page_decode_requests'],
                             selected_rows=len(selected),range_page_requests=window['page_decode_requests'],
                             all_row_scan_page_requests=scan['page_decode_requests']))
    t=BPlusIndex.from_sorted([(k,b'old') for k in range(30)])
    old=t.dumps();leaf_of_b=t._leaf(29).page_id
    t.put(0,b'new');t.put(29,b'new');new=t.dumps()
    mixed=bytearray(new);offset=IMAGE_HEADER.size+CRC.size+(leaf_of_b-1)*128
    mixed[offset:offset+128]=old[offset:offset+128]
    loaded=BPlusIndex.loads(bytes(mixed))
    mixed_result=dict(page_replaced=leaf_of_b,structurally_valid=loaded.validate(),
                      key0=loaded.get(0).decode(),key29=loaded.get(29).decode(),
                      interpretation='Accepted new/old state: page checksums and tree invariants do not implement batch atomicity.')
    tiny=BPlusIndex()
    trace=[]
    for key in (10,20,30,25,5,15,35):
        tiny.put(key,str(key).encode())
        trace.append({'insert':key,'root':tiny.root,'shape':tiny.validate(),
                      'pages':[dict(page_id=node.page_id,leaf=node.leaf,keys=node.keys,
                                    children=node.children,next_leaf=node.next_leaf)
                               for node in [decode_node(tiny._pages.raw[i],128,i) for i in sorted(tiny._pages.raw)]]})
    return dict(kind='actually executed synthetic byte-page experiments; no disk I/O benchmark or database transaction claim',
                environment={'python':sys.version,'platform':platform.platform()},
                parameters={'rows':n,'shuffle_seed':4081,'value':'decimal key ASCII bytes','page_sizes':[128,256,512,1024]},
                code_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'bplus.py',HERE/'experiment.py')},
                runs=runs,accepted_mixed_snapshot=mixed_result,worked_trace=trace,
                limitations=['Logical page requests do not model the OS cache, storage latency, compression or device writes.',
                             'Fixed-size cells reserve24 bytes even for a short value; there are no overflow pages.',
                             'No delete, merge, lock, WAL/checkpoint integration, fsync or atomic publication is implemented.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=run();text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
