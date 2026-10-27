"""Reference local-only FASTA alignment CLI; keep closed until milestones attempted."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / '18-computational-biology' / 'code'
sys.path.insert(0, str(CODE))
from alignment import align_global, align_local
from sequence_lab import parse_fasta


def main(argv=None):
    parser = argparse.ArgumentParser(description='Align two bounded DNA FASTA records locally')
    parser.add_argument('fasta', type=Path)
    parser.add_argument('--mode', choices=['global', 'local'], default='global')
    parser.add_argument('--match', type=int, default=2)
    parser.add_argument('--mismatch', type=int, default=-3)
    parser.add_argument('--gap', type=int, default=-2)
    parser.add_argument('--max-cells', type=int, default=1_000_000)
    parser.add_argument('--max-bytes', type=int, default=65536)
    args = parser.parse_args(argv)
    try:
        if args.max_bytes < 1:
            raise ValueError('max-bytes must be positive')
        # Bounded read also handles a file growing after a size check.
        with args.fasta.open('rb') as handle:
            raw = handle.read(args.max_bytes + 1)
        if len(raw) > args.max_bytes:
            raise ValueError('FASTA exceeds max-bytes')
        records = parse_fasta(raw.decode('utf-8'))
        if len(records) != 2 or any(not seq for _, seq in records):
            raise ValueError('exactly two nonempty FASTA records are required')
        if records[0][0] == records[1][0]:
            raise ValueError('record identifiers must be distinct')
        fn = align_global if args.mode == 'global' else align_local
        r = fn(records[0][1], records[1][1], args.match, args.mismatch, args.gap,
               max_cells=args.max_cells)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    report = {'schema': 1, 'input_sha256': hashlib.sha256(raw).hexdigest(),
              'implementation_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in [Path(__file__), CODE / 'alignment.py', CODE / 'sequence_lab.py']},
              'records': [{'name': name, 'length': len(seq)} for name, seq in records],
              'mode': args.mode,
              'scoring': {'match': args.match, 'mismatch': args.mismatch, 'gap': args.gap,
                          'gap_model': 'linear, charged per gap symbol'},
              'score': r.score, 'a_aligned': r.a_aligned, 'b_aligned': r.b_aligned,
              'a_span': r.a_span, 'b_span': r.b_span,
              'cells_evaluated': r.cells_evaluated,
              'limits': ['N is a literal symbol, not a wildcard.',
                         'A deterministic optimal alignment is not evidence of ancestry or function.',
                         'Synthetic educational computation; no clinical interpretation.']}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
