#!/usr/bin/env python3
"""Check tracked publication paths/content without executing educational code.

This is a bounded publication hygiene check, not a guarantee that every possible
secret, legal issue or curriculum defect has been detected. Curated observations
remain versioned; local generated outputs belong in ignored directories.
"""
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import stat
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=100*1024*1024
PRIVATE_PARTS={'.git','.venv','venv','node_modules','__pycache__','.pytest_cache',
               '.mypy_cache','.ruff_cache','.tox','.nox','private','raw-private'}
GENERATED_SUFFIXES={'.pyc','.pyo','.o','.a','.so','.dll','.exe','.class','.bundle',
                    '.zip','.gz','.xz','.pem','.key','.sqlite','.sqlite3','.db'}
DELIVERY_ONLY={'RELEASE.json','SOURCE_SHA256SUMS.txt','DELIVERY_RECEIPT.md','READ_ME_FIRST.txt'}
RESERVED={'con','prn','aux','nul'}|{f'{prefix}{n}' for prefix in ('com','lpt') for n in range(1,10)}
SECRET_MARKERS=[
    ('private-key',re.compile(br'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----')),
    ('github-token',re.compile(br'\bgh[pousr]_[A-Za-z0-9]{36,}\b')),
    ('github-fine-grained-token',re.compile(br'\bgithub_pat_[A-Za-z0-9_]{80,}\b')),
]


def path_findings(names):
    findings=[];seen={}
    for name in names:
        path=PurePosixPath(name)
        if not name or path.is_absolute() or '..' in path.parts or '\\' in name or any(ord(c)<32 for c in name):
            findings.append(dict(path=name,code='unsafe-path'));continue
        key=name.casefold()
        if key in seen:findings.append(dict(path=name,code='case-collision',other=seen[key]))
        seen[key]=name
        if any(part.casefold().split('.')[0] in RESERVED or part.endswith(('.', ' ')) or
               any(c in part for c in '<>:"|?*') for part in path.parts):
            findings.append(dict(path=name,code='nonportable-path'))
        if any(part.casefold() in PRIVATE_PARTS for part in path.parts):
            findings.append(dict(path=name,code='private-or-generated-tree'))
        if path.suffix.lower() in GENERATED_SUFFIXES:
            findings.append(dict(path=name,code='private-or-generated-file'))
        basename=path.name.casefold()
        if (basename in {'.env','credentials.json','thumbs.db','desktop.ini','.ds_store'} or
                basename.startswith(('secrets.','.env.')) and basename!='.env.example'):
            findings.append(dict(path=name,code='local-configuration'))
        if len(path.parts)==1 and name.casefold() in {p.casefold() for p in DELIVERY_ONLY}:
            findings.append(dict(path=name,code='delivery-sidecar-in-repository'))
        if len(path.parts)>=4 and path.parts[0]=='books' and path.parts[2]=='source' and name!=f'books/{path.parts[1]}/source/README.md':
            findings.append(dict(path=name,code='unbundled-book-original'))
    return findings


def content_findings(name,data):
    findings=[]
    if len(data)>=MAX_BYTES:findings.append(dict(path=name,code='github-size-limit'))
    if data.startswith((b'\x7fELF',b'MZ',b'SQLite format 3\x00')):
        findings.append(dict(path=name,code='generated-binary-content'))
    for kind,pattern in SECRET_MARKERS:
        match=pattern.search(data)
        if match:
            # Never echo a possible credential in a report or CI log.
            findings.append(dict(path=name,code=kind,line=data[:match.start()].count(b'\n')+1))
    return findings


def source_findings(source):
    findings=path_findings(source)
    for name,data in source.items():findings+=content_findings(name,data)
    return findings


def audit(root=ROOT):
    root=root.resolve()
    names=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
    names=[name for name in names if name]
    findings=path_findings(names)
    ignored=subprocess.check_output(['git','ls-files','-ci','--exclude-standard','-z'],cwd=root).decode().split('\0')
    findings += [dict(path=name,code='ignored-file-tracked') for name in ignored if name]
    for name in names:
        path=root/name
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            findings.append(dict(path=name,code='symlink-or-escape'));continue
        if not path.is_file():
            findings.append(dict(path=name,code='tracked-file-missing'));continue
        if path.stat().st_size>=MAX_BYTES:
            findings.append(dict(path=name,code='github-size-limit'));continue
        findings+=content_findings(name,path.read_bytes())
    return dict(tracked_files=len(names),findings=findings,
                limits='Known credential markers, publication artifacts and path/size checks only; not exhaustive secret detection, licensing clearance or educational certification.')


def verify_zip(path,expected):
    """Require a flat, source-only archive with the exact expected byte tree."""
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)) or set(names)!=set(expected):
            raise ValueError('ZIP must contain exactly the repository files at its root')
        findings=path_findings(names)
        for info in archive.infolist():
            if stat.S_ISLNK(info.external_attr>>16) or info.file_size>=MAX_BYTES:
                raise ValueError('ZIP contains a symlink or oversized file')
            data=archive.read(info.filename)
            if data!=expected[info.filename]:raise ValueError('ZIP byte mismatch: '+info.filename)
            findings+=content_findings(info.filename,data)
        if findings:raise ValueError(json.dumps(findings))
        if archive.testzip() is not None:raise ValueError('ZIP CRC failure')
    return dict(source_files=len(expected),source_bytes=sum(map(len,expected.values())),
                zip_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path);args=parser.parse_args()
    report=audit()
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return int(bool(report['findings']))


if __name__=='__main__':raise SystemExit(main())
