"""Read-only rebuild from the existing p07 authoritative log, never its cache.

The integration accepts a documented subset: canonical signed-int64 decimal
string keys, and UTF-8 string values fitting the24-byte leaf value field.
The snapshot is not used to skip replay; no checkpoint protocol is invented.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

from bplus import BPlusIndex, key_number, value_bytes

ROOT=Path(__file__).resolve().parents[2]
WAL_PATH=ROOT/'projects-guided/p07-storage-engine/code/wal_store.py'


def wal_module():
    name='mm_page_index_existing_wal'
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,WAL_PATH)
        module=importlib.util.module_from_spec(spec);sys.modules[name]=module
        spec.loader.exec_module(module)
    return sys.modules[name]


def rebuild_from_log(path, page_size=128, max_pages=65535):
    report=wal_module().recover(path)
    rows=[]
    for text,value in report.data.items():
        if len(text)>20:
            raise ValueError('log key is outside canonical signed-int64 subset')
        try:key=int(text)
        except ValueError:raise ValueError('log key is not a decimal integer') from None
        key_number(key)
        if str(key)!=text:
            raise ValueError('log key is not canonical decimal')
        try:encoded=value.encode('utf-8')
        except UnicodeError:raise ValueError('log value is not valid UTF-8 text') from None
        value_bytes(encoded);rows.append((key,encoded))
    tree=BPlusIndex.from_sorted(sorted(rows),page_size,max_pages)
    return tree,dict(transactions=report.transactions,valid_end=report.valid_end,
                     trailing_bytes=report.trailing_bytes,tail_reason=report.tail_reason,
                     authority='full read-only WAL replay; index can be discarded and rebuilt')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wal',type=Path,required=True)
    parser.add_argument('--page-size',type=int,default=128)
    args=parser.parse_args();tree,report=rebuild_from_log(args.wal,args.page_size)
    print(json.dumps({'source':report,'shape':tree.validate(),
                      'rows':[{'key':key,'value_hex':value.hex()} for key,value in tree.range()]},indent=2))
