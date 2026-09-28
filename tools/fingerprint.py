#!/usr/bin/env python3
"""Print a file's size and SHA-256; never infer edition, legitimacy or readability."""
import argparse
import hashlib
import json
from pathlib import Path


def fingerprint(path):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError('Source must be a regular non-symlink file.')
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return {'filename': path.name, 'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    print(json.dumps(fingerprint(args.path), indent=2))


if __name__ == '__main__':
    main()
