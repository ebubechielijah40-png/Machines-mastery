"""Runnable milestone-1 inventory, deliberately without the completed aligner."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '18-computational-biology' / 'code'))
from sequence_lab import parse_fasta


def inspect(path):
    with Path(path).open('rb') as handle:
        raw = handle.read(65537)
    if len(raw) > 65536:
        raise ValueError('input exceeds starter 64 KiB limit')
    records = parse_fasta(raw.decode('utf-8'))
    return {'sha256': hashlib.sha256(raw).hexdigest(),
            'records': [{'name': name, 'length': len(seq)} for name, seq in records]}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: inspect_fasta.py FASTA_PATH')
    print(json.dumps(inspect(sys.argv[1]), indent=2, sort_keys=True))
