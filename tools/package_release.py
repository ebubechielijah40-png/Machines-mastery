#!/usr/bin/env python3
"""Package a clean committed source tree and its development history for review.

No remote writes. Outputs stay outside the repository. The ZIP is a source
checkpoint; a passing executable report is not curriculum-completion evidence.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path,PurePosixPath
import subprocess
import tarfile
import zipfile
from check_publication import source_findings,verify_zip
ROOT=Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--report-root',type=Path,required=True)
    parser.add_argument('--continuation-base',required=True)
    parser.add_argument('--source-only',action='store_true',
                        help='Put only repository files at ZIP root; keep bundle/metadata/checksums beside it')
    args=parser.parse_args()
    # The label is a filename component, never a path or shell expression.
    if not args.label or any(c not in '0123456789-' for c in args.label):parser.error('label must contain only digits and hyphens')
    destination=args.output_dir.resolve()
    if destination==ROOT or destination.is_relative_to(ROOT):parser.error('output directory must be outside repository')
    dirty=git('status','--porcelain','--untracked-files=normal').decode()
    if dirty:parser.error('commit/review public changes first; working tree is not clean')
    commit=git('rev-parse','HEAD').decode().strip()
    branch=git('symbolic-ref','--short','HEAD').decode().strip()
    if branch in ('main','master'):parser.error('package the development/review branch')
    report_root=(ROOT/args.report_root).resolve()
    if not report_root.is_relative_to(ROOT):parser.error('report root must remain inside repository')
    report_relative=report_root.relative_to(ROOT).as_posix()
    base=git('rev-parse',args.continuation_base+'^{commit}').decode().strip()
    if subprocess.run(['git','merge-base','--is-ancestor',base,commit],cwd=ROOT).returncode:
        parser.error('continuation base must be an ancestor of this commit')
    timestamp=int(git('show','-s','--format=%ct','HEAD').decode())
    date=datetime.fromtimestamp(timestamp,timezone.utc)
    if not 1980<=date.year<=2107:parser.error('commit date outside ZIP timestamp range')
    archive_bytes=git('archive','--format=tar','HEAD')
    source={};modes={}
    with tarfile.open(fileobj=io.BytesIO(archive_bytes),mode='r:') as archive:
        for member in archive:
            if member.isdir():continue
            path=PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts or any(c in member.name for c in '\r\n\\'):
                parser.error('unsupported/unsafe archive entry: '+member.name)
            source[member.name]=archive.extractfile(member).read();modes[member.name]=member.mode
    findings=source_findings(source)
    if findings:parser.error('publication hygiene findings: '+json.dumps(findings))
    destination.mkdir(parents=True,exist_ok=True)
    bundle_name=f'Machines-mastery-development-{args.label}-zip.bundle'
    zip_name=f'Machines-mastery-development-{args.label}.zip'
    checksum_name=f'Machines-mastery-{args.label}-zip-SHA256SUMS.txt'
    for name in (bundle_name,zip_name,checksum_name,'RELEASE.json'):
        if (destination/name).exists():parser.error('output already exists: '+name)
    bundle=destination/bundle_name
    git('bundle','create',str(bundle),'refs/heads/'+branch)
    bundle_bytes=bundle.read_bytes()
    verification=json.loads(source[report_relative+'/verification-final/results.json'])
    records=verification['results'];statuses={status:sum(r['status']==status for r in records) for status in ('PASS','FAIL','BLOCKED')}
    if statuses['FAIL']:parser.error('final verified report includes a failed command')
    gate=json.loads(source[report_relative+'/content-gate.json'])
    prefix='' if args.source_only else 'machines-mastery/'
    release={'schema_version':1,'label':args.label,'commit':commit,'branch':branch,
             'source_file_count':len(source),'source_archive_prefix':prefix,
             'source_only':args.source_only,'git_bundle_in_zip':not args.source_only,
             'source_manifest':'SOURCE_SHA256SUMS.txt','git_bundle':bundle_name,
             'bundle_sha256':sha(bundle_bytes),'bundle_bytes':len(bundle_bytes),
             'baseline_commit':'7936e4344021f78f93a9e568c839da719cf2b35f',
             'continuation_base_commit':base,
             'educational_mandate':'INCOMPLETE; no whole-domain EXCELLENT classification',
             'verification_report':prefix+report_relative+'/verification-final/results.json',
             'verification_status_counts':statuses,'strict_content_gate_exit':gate['exit_code'],
             'strict_content_findings':gate['findings'],
             'limits':'Declared local contracts only. No physical/lab/hardware/live deployment or learner mastery certification. Compilers/private originals/credentials excluded.'}
    manifest=''.join(f'{sha(source[name])}  {prefix}{name}\n' for name in sorted(source))
    readme='''Machines Mastery — source and history delivery

The full source is in machines-mastery/.
Verify SOURCE_SHA256SUMS.txt from this extracted folder.
RELEASE.json identifies the exact commit and evidence boundaries.
The companion bundle preserves the complete development branch/history.
Read machines-mastery/PUSH_INSTRUCTIONS.md for your manual review-branch push.
The whole educational mandate remains incomplete; see the domain audit.
'''
    if args.source_only:
        readme='''Machines Mastery — repository-only GitHub ZIP

The ZIP contains only repository files at its root. Extract into your cloned
repository and follow PUSH_INSTRUCTIONS.md. No files need to be deleted.
The complete Git bundle, source manifest, release metadata and checksum are
separate recovery artifacts; keep them outside the repository you push.
The full educational mandate remains incomplete; see STRONG_PROGRESS_DASHBOARD.md.
'''
        payload=source
        (destination/'SOURCE_SHA256SUMS.txt').write_text(manifest)
        (destination/'READ_ME_FIRST.txt').write_text(readme)
    else:
        payload={'RELEASE.json':(json.dumps(release,indent=2)+'\n').encode(),
                 'SOURCE_SHA256SUMS.txt':manifest.encode(),'READ_ME_FIRST.txt':readme.encode(),bundle_name:bundle_bytes}
        payload.update({prefix+name:data for name,data in source.items()})
    output=destination/zip_name
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in sorted(payload):
            info=zipfile.ZipInfo(name,date.timetuple()[:6]);info.create_system=3
            mode=modes.get(name.removeprefix('machines-mastery/'),0o644)
            info.external_attr=(0o100000|mode)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,payload[name],compresslevel=9)
    if args.source_only:verify_zip(output,source)
    checksum=sha(output.read_bytes())
    (destination/checksum_name).write_text(f'{checksum}  {zip_name}\n')
    (destination/'RELEASE.json').write_text(json.dumps(release,indent=2)+'\n')
    print(json.dumps({'zip':str(output),'zip_bytes':output.stat().st_size,'zip_sha256':checksum,
                      'checksum_file':str(destination/checksum_name),'commit':commit,
                      'source_file_count':len(source),'bundle':str(bundle)},indent=2))


if __name__=='__main__':main()
