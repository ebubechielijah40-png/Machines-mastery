"""Capture exact CLI inputs/outputs for deterministic OS teaching models."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

BASE = Path(__file__).resolve().parent


def observe():
    cases = [
        ('schedule', {'jobs': [['A', 0, 5], ['B', 1, 2], ['C', 2, 1]], 'quantum': 2}),
        ('translate', {'mappings': [[2, 7, 'r']],
                       'accesses': [[45], [45], [45, 'w'], [64]]}),
    ]
    records = []
    for mode, payload in cases:
        raw = (json.dumps(payload, separators=(',', ':')) + '\n').encode()
        command = [sys.executable, str(BASE / 'kernel_workbench.py'), mode]
        result = subprocess.run(command, input=raw, capture_output=True, timeout=5)
        record = dict(kind='executed deterministic model, not host kernel measurement',
                      command=command, input_utf8=raw.decode(),
                      input_sha256=hashlib.sha256(raw).hexdigest(),
                      exit_code=result.returncode, stdout=result.stdout.decode(),
                      stderr=result.stderr.decode())
        if result.returncode:
            raise RuntimeError(record)
        if json.loads(record['stdout'])['input_sha256'] != record['input_sha256']:
            raise AssertionError('input identity mismatch')
        records.append(record)
    return dict(environment=dict(python=sys.version, platform=platform.platform()),
                records=records)


if __name__ == '__main__':
    print(json.dumps(observe(), indent=2))
