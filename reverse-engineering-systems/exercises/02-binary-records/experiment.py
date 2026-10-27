"""Executed discovery probes, then source-reveal differential/mutation checks."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
from oracle import compile_oracle, query
BASE=Path(__file__).resolve().parent


def run():
    probes=[('baseline',0,0,False,b''),('sequence_one',1,0,False,b''),
            ('sequence_carry',256,0,False,b''),('asymmetric_sequence',0x1234,0,False,b''),
            ('sample_one',0,1,False,b''),('sample_carry',0,256,False,b''),
            ('sample_negative',0,-1,False,b''),('flag_only',0,0,True,b''),
            ('one_zero_byte',0,0,False,b'\x00'),('two_distinct_bytes',0,0,False,b'\x41\xff'),
            ('same_sum_swapped',0,0,False,b'\xff\x41'),
            ('maximum_payload',65535,-32768,True,bytes(range(32)))]
    records=[]
    with tempfile.TemporaryDirectory(prefix='mm-binary-') as directory:
        binary=Path(directory)/'oracle'
        command=compile_oracle(binary)
        for label,sequence,sample,enabled,payload in probes:
            output=query(binary,sequence,sample,enabled,payload)
            records.append(dict(label=label,input=dict(sequence=sequence,sample=sample,enabled=enabled,payload_hex=payload.hex()),output_hex=output.hex(),byte_count=len(output)))
        binary_hash=hashlib.sha256(binary.read_bytes()).hexdigest()
    compiler=shutil.which('cc')
    return dict(observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                environment=dict(platform=platform.platform(),compiler=subprocess.check_output([compiler,'--version'],text=True).splitlines()[0]),
                build_command=command,oracle_source_sha256=hashlib.sha256((BASE/'reference/oracle.c').read_bytes()).hexdigest(),
                observed_binary_sha256=binary_hash,probes=records,
                limits='Actual locally compiled oracle outputs. Source is available after the learner attempt; observations alone do not identify a unique internal implementation.')
if __name__=='__main__':print(json.dumps(run(),indent=2))
