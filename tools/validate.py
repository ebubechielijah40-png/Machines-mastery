#!/usr/bin/env python3
"""Check local structural/evidence contracts; cannot establish truth or mastery."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from render import documents

ROOT = Path(__file__).resolve().parents[1]
STATES = {'NOT STARTED', 'MAPPED', 'STUDIED', 'RECALLABLE', 'EXPLAINABLE',
          'APPLICABLE', 'IMPLEMENTABLE', 'DEBUGGABLE', 'EXPERIMENTALLY VERIFIED',
          'RECONSTRUCTABLE', 'TRANSFERABLE', 'PRODUCTION-APPLICABLE', 'SCALABILITY-TESTED',
          'FAILURE-TESTED', 'OPERATIONALLY-UNDERSTOOD', 'MASTERED'}
PROJECT_FILES = {'README.md', 'ORIGIN_AND_ATTRIBUTION.md', 'DESIGN.md', 'ARCHITECTURE.md',
                 'PREREQUISITES.md', 'BUILD_LOG.md', 'EXPERIMENTS.md', 'TESTS.md',
                 'RESULTS.md', 'REFERENCES.md'}
GATES = {'build', 'tests', 'behavior', 'mechanism_explanation', 'failure_cases',
         'attribution', 'license', 'experiments', 'results', 'references'}
COLLECTIONS = {
    'tracks': ('id', {'id': str, 'title': str, 'path': str, 'phase': str,
        'required': list, 'units': list, 'resources': list, 'status': str, 'state': str}),
    'lessons': ('id', {'id': str, 'unit_id': str, 'path': str, 'status': str,
        'bridge': str, 'resources': list, 'project': str, 'experiment': str}),
    'resources': ('id', {'id': str, 'title': str, 'type': str, 'author': str, 'phases': list,
        'purpose': str, 'prerequisites': str, 'why_selected': str, 'original_source': str,
        'license': str, 'verification': str, 'verification_scope': str, 'checked_on': str,
        'local_availability': str, 'notes': str}),
    'phases': ('id', {'id': str, 'title': str, 'directories': list, 'topics': str,
        'resources': list, 'outcome': str, 'project': str, 'state': str}),
    'units': ('id', {'id': str, 'title': str, 'phase': str, 'required': list,
        'recommended': list, 'concurrent': list, 'resources': list, 'exit_gate': str,
        'state': str, 'evidence': list}),
    'projects': ('id', {'id': str, 'title': str, 'phase': str, 'slug': str,
        'status': str, 'original_resources': list, 'attribution_status': str,
        'outcome': str, 'stage': str, 'evidence': list, 'quality_gates': dict}),
    'books': ('resource_id', {'resource_id': str, 'slug': str, 'path': str, 'status': str}),
    'experiments': ('id', {'id': str, 'title': str, 'phase': str, 'project': str,
        'path': str, 'status': str, 'observed_result': str, 'evidence': list,
        'resources': list, 'source_ready': bool}),
    'chapters': ('id', {'id': str, 'resource_id': str, 'path': str, 'locator': str,
        'status': str, 'source_ready': bool}),
    'claims': ('id', {'id': str, 'label': str, 'statement': str, 'resource_ids': list,
        'locator': str, 'artifact': str, 'status': str, 'assumptions': str, 'evidence': list}),
    'knowledge_edges': ('id', {'id': str, 'from': str, 'relation': str, 'to': str,
        'claim_ids': list, 'artifact': str, 'limitations': str}),
    'mastery': ('id', {'id': str, 'unit_id': str, 'state': str, 'assessed_on': str,
        'assessor': str, 'evidence': list, 'assistance': str, 'gaps': list,
        'next_review': str, 'criteria': dict}),
}


def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('expected nonempty repository-relative path')
    path = root / relative
    if '..' in Path(relative).parts or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes repository')
    if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ValueError('symlinks are not evidence paths')
    return path


def schema_errors(data):
    errors = []
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        return ['unsupported or missing catalog schema_version']
    for collection, (key, fields) in COLLECTIONS.items():
        rows = data.get(collection)
        if not isinstance(rows, list):
            errors.append(f'{collection}: expected list')
            continue
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f'{collection}[{i}]: expected object')
                continue
            for field, kind in fields.items():
                value = row.get(field)
                if type(value) is not kind or (kind is str and not value.strip()):
                    errors.append(f'{collection}[{i}].{field}: expected nonempty {kind.__name__}')
                if kind is list and isinstance(value, list) and any(not isinstance(v,str) for v in value):
                    errors.append(f'{collection}[{i}].{field}: items must be strings')
            nullable = {'projects': ['path'], 'books': ['source_path','sha256','edition','inspection_evidence']}
            for field in nullable.get(collection,[]):
                if field not in row or row[field] is not None and not isinstance(row[field],str):
                    errors.append(f'{collection}[{i}].{field}: expected string or null')
    return errors


def validate_catalog(data, root=ROOT):
    errors = schema_errors(data)
    warnings = []
    if errors:
        return errors, warnings
    indexes = {}
    for collection, (key, _) in COLLECTIONS.items():
        indexes[collection] = {}
        for row in data[collection]:
            id = row[key]
            if id in indexes[collection]:
                errors.append(f'{collection}: duplicate ID {id}')
            indexes[collection][id] = row

    def refs(values, collection, owner, required=False):
        if required and not values:
            errors.append(f'{owner}: missing {collection} references')
        for id in values:
            if id not in indexes[collection]:
                errors.append(f'{owner}: unknown {collection} reference {id}')

    def file_ref(relative, owner, directory=False):
        try:
            p = safe_path(root, relative)
            valid = p.is_dir() if directory else p.is_file() and p.stat().st_size > 0
            if not valid:
                errors.append(f'{owner}: missing or empty evidence/path {relative}')
            return p if valid else None
        except (ValueError, OSError) as exc:
            errors.append(f'{owner}: unsafe path ({exc})')
            return None

    def evidence(row, required=False):
        if required and not row['evidence']:
            errors.append(f"{row['id']}: missing evidence")
        for path in row['evidence']:
            file_ref(path, row['id'])

    for r in data['resources']:
        refs(r['phases'], 'phases', r['id'], True)
        url = urlsplit(r['original_source'])
        if url.scheme not in {'http','https'} or not url.netloc or url.username or url.password:
            errors.append(f"{r['id']}: invalid public source URL")
        if r['verification'] not in {'IDENTITY VERIFIED','PARTIALLY VERIFIED','UNVERIFIED'}:
            errors.append(f"{r['id']}: invalid verification state")
        if r['verification'] != 'IDENTITY VERIFIED':
            warnings.append(f"{r['id']}: {r['verification']} identity/metadata")
        if r['license'].startswith('UNVERIFIED'):
            warnings.append(f"{r['id']}: license unverified; no importing before review")

    for p in data['phases']:
        refs(p['resources'], 'resources', p['id'], True)
        refs([p['project']], 'projects', p['id'])
        if p['state'] not in STATES:
            errors.append(f"{p['id']}: invalid learning state")
        for d in p['directories']:
            file_ref(d+'/README.md',p['id'])

    for u in data['units']:
        refs([u['phase']], 'phases', u['id'])
        refs(u['resources'], 'resources', u['id'], True)
        for field in ['required','recommended','concurrent']:
            refs(u[field], 'units', u['id'])
            if u['id'] in u[field]:
                errors.append(f"{u['id']}: self-dependency in {field}")
        if u['state'] not in STATES:
            errors.append(f"{u['id']}: invalid learning state")
        evidence(u, u['state']!='NOT STARTED')
        if u['state']!='NOT STARTED' and not any(
                m['unit_id']==u['id'] and m['state']==u['state'] for m in data['mastery']):
            errors.append(f"{u['id']}: learning advancement requires a matching mastery review")
    visited, active = set(), set()
    def visit(id):
        if id in active:
            errors.append(f'prerequisite cycle at {id}')
            return
        if id in visited or id not in indexes['units']:
            return
        active.add(id)
        for dep in indexes['units'][id]['required']:
            visit(dep)
        active.remove(id)
        visited.add(id)
    for id in indexes['units']:
        visit(id)

    for t in data['tracks']:
        refs([t['phase']], 'phases', t['id'])
        refs(t['required'] + t['units'], 'units', t['id'], True)
        refs(t['resources'], 'resources', t['id'], True)
        file_ref(t['path'] + '/README.md', t['id'])
        if t['status'] != 'INFRASTRUCTURE' or t['state'] != 'NOT STARTED':
            errors.append(f"{t['id']}: track infrastructure is not aggregate learner mastery")
    for lesson in data['lessons']:
        refs([lesson['unit_id']], 'units', lesson['id'])
        refs([lesson['project']], 'projects', lesson['id'])
        refs([lesson['experiment']], 'experiments', lesson['id'])
        refs(lesson['resources'], 'resources', lesson['id'], True)
        file_ref(lesson['path'] + '/README.md', lesson['id'])
        file_ref(lesson['bridge'], lesson['id'])
        if lesson['status'] not in {'PREPARED', 'SCAFFOLDED', 'BLOCKED'}:
            errors.append(f"{lesson['id']}: preparation status is not a learner state")
        if not lesson['bridge'].startswith(lesson['path'] + '/'):
            errors.append(f"{lesson['id']}: bridge must belong to lesson")
    for u in data['units']:
        if 'path' in u:
            file_ref(u['path'], u['id'])

    for p in data['projects']:
        refs([p['phase']], 'phases', p['id'])
        refs(p['original_resources'], 'resources', p['id'], True)
        if p['status'] not in {'PLANNED','PREPARED','ACTIVE','BLOCKED','COMPLETE'}:
            errors.append(f"{p['id']}: invalid project status")
        if p.get('path'):
            for name in PROJECT_FILES:
                file_ref(p['path']+'/'+name,p['id'])
        elif p['status'] not in {'PLANNED','BLOCKED'}:
            errors.append(f"{p['id']}: materialized project requires path")
        if set(p['quality_gates']) != GATES:
            errors.append(f"{p['id']}: missing/unknown quality gates")
        for gate, value in p['quality_gates'].items():
            allowed = isinstance(value,str) and (value in {'PASS','FAIL','NOT RUN'} or
                value.startswith('NOT APPLICABLE: ') and len(value)>20)
            if not allowed:
                errors.append(f"{p['id']}: malformed gate {gate}")
            if p['status']=='COMPLETE' and (not allowed or value in {'FAIL','NOT RUN'}):
                errors.append(f"{p['id']}: incomplete quality gate {gate}")
        evidence(p, p['status']=='COMPLETE')
        if p['status']=='COMPLETE' and 'UNVERIFIED' in p['attribution_status']:
            errors.append(f"{p['id']}: completion blocked by unverified attribution")

    inspected_books = set()
    for b in data['books']:
        refs([b['resource_id']], 'resources', b['resource_id'])
        for name in ['README.md','source/README.md','generated/BOOK_MAP.md','generated/CONCEPT_INDEX.md',
                     'generated/PREREQUISITES.md','generated/SOURCE_INDEX.md']:
            file_ref(b['path']+'/'+name,b['resource_id'])
        if b['status']=='SOURCE NOT PRESENT':
            if b.get('source_path') or b.get('sha256') or b.get('edition') or b.get('inspection_evidence'):
                errors.append(f"{b['resource_id']}: absent source has claimed inspection metadata")
            warnings.append(f"{b['resource_id']}: SOURCE NOT PRESENT; chapter processing blocked")
        elif b['status']=='INSPECTED':
            source = file_ref(b.get('source_path'),b['resource_id'])
            inspection = file_ref(b.get('inspection_evidence'),b['resource_id'])
            if not b.get('edition'):
                errors.append(f"{b['resource_id']}: inspected source lacks edition")
            if source:
                source_folder = safe_path(root,b['path']+'/source')
                if not source.is_relative_to(source_folder) or source.name=='README.md':
                    errors.append(f"{b['resource_id']}: book source must be an original under its source directory")
                digest = hashlib.sha256()
                with source.open('rb') as handle:
                    for block in iter(lambda: handle.read(1024*1024),b''):
                        digest.update(block)
                if digest.hexdigest()!=b.get('sha256'):
                    errors.append(f"{b['resource_id']}: source fingerprint mismatch")
                elif inspection and b.get('edition'):
                    inspected_books.add(b['resource_id'])
        else:
            errors.append(f"{b['resource_id']}: invalid book status")
    for c in data['chapters']:
        portable_derived = c.get('status') == 'PORTABLE_DERIVED' and not c.get('source_ready')
        if not portable_derived and (c['resource_id'] not in inspected_books or not c['source_ready']):
            errors.append(f"{c['id']}: chapter without inspected local source")
        if portable_derived:
            warnings.append(f"{c['id']}: portable derived artifact; original source excluded, exact source verification unavailable in this archive")
        path = file_ref(c['path'],c['id'],directory=True)
        if path:
            for name in ['01_MAP.md','11_SOURCE_REFERENCES.md','13_GAPS.md']:
                file_ref(c['path']+'/'+name,c['id'])
        if 'UNVERIFIED' in c['locator']:
            errors.append(f"{c['id']}: chapter locator unverified")

    for e in data['experiments']:
        refs([e['phase']], 'phases', e['id'])
        refs([e['project']], 'projects', e['id'])
        refs(e['resources'], 'resources', e['id'], True)
        file_ref(e['path']+'/README.md',e['id'])
        if e['status'] not in {'PLANNED','BLOCKED','RUNNING','OBSERVED','ANALYZED'}:
            errors.append(f"{e['id']}: invalid experiment status")
        observed = e['status'] in {'OBSERVED','ANALYZED'}
        if observed and (e['observed_result']=='NOT YET OBSERVED' or not e['source_ready']):
            errors.append(f"{e['id']}: observation without result/source readiness")
        if not observed and e['observed_result']!='NOT YET OBSERVED':
            errors.append(f"{e['id']}: unexecuted experiment claims a result")
        evidence(e,observed)
        if observed and not any(p.startswith(e['path']+'/raw/') for p in e['evidence']):
            errors.append(f"{e['id']}: observation requires non-private raw evidence under its raw directory")

    for c in data['claims']:
        if c['label'] not in {'SOURCE','DERIVED','EXPLANATION','EXTERNAL','INFERENCE','UNCERTAIN'}:
            errors.append(f"{c['id']}: invalid epistemic label")
        refs(c['resource_ids'],'resources',c['id'],c['label']!='UNCERTAIN')
        file_ref(c['artifact'],c['id'])
        evidence(c,c['status']=='VERIFIED')
        if c['status'] not in {'VERIFIED','UNVERIFIED','CONTRADICTED'}:
            errors.append(f"{c['id']}: invalid claim status")
        if c['status']=='VERIFIED' and ('UNVERIFIED' in c['locator'] or c['label']=='UNCERTAIN'):
            errors.append(f"{c['id']}: verified claim lacks established locator/label")
    for e in data['knowledge_edges']:
        refs(e['claim_ids'],'claims',e['id'],True)
        file_ref(e['artifact'],e['id'])
        if any(indexes['claims'].get(id,{}).get('status')!='VERIFIED' for id in e['claim_ids']):
            errors.append(f"{e['id']}: knowledge edge lacks verified claim support")
    for m in data['mastery']:
        refs([m['unit_id']],'units',m['id'])
        if m['state'] not in STATES:
            errors.append(f"{m['id']}: invalid mastery state")
        evidence(m,m['state']!='NOT STARTED')
        state_criteria = {
            'DEBUGGABLE': {'debugging'}, 'RECONSTRUCTABLE': {'reconstruction'},
            'TRANSFERABLE': {'transfer'}, 'PRODUCTION-APPLICABLE': {'implementation', 'tests', 'measurement', 'security'},
            'SCALABILITY-TESTED': {'baseline', 'load', 'comparison', 'correctness'},
            'FAILURE-TESTED': {'fault_injection', 'detection', 'recovery'},
            'OPERATIONALLY-UNDERSTOOD': {'observability', 'release', 'rollback', 'incident'},
        }
        for key in state_criteria.get(m['state'], set()):
            if not isinstance(m['criteria'].get(key), str) or not m['criteria'].get(key, '').strip():
                errors.append(f"{m['id']}: missing state criterion {key}")
        if m['state'] in state_criteria and m['gaps']:
            errors.append(f"{m['id']}: unresolved core gaps block claimed capability")
        if m['state']=='MASTERED':
            needed = {'delayed_recall','transfer','mechanism','failure_analysis','implementation','experiment', 'debugging', 'reconstruction', 'applied_scope'}
            if indexes['units'].get(m['unit_id'], {}).get('applied', False):
                needed |= {'tests', 'measurement', 'optimization', 'failure_handling', 'scaling', 'security', 'operations'}
            if not needed.issubset(m['criteria']) or m['gaps']:
                errors.append(f"{m['id']}: MASTERED requires reviewed criteria and no core gaps")
            for key in needed:
                if not isinstance(m['criteria'].get(key),str) or not m['criteria'].get(key,'').strip():
                    errors.append(f"{m['id']}: missing mastery criterion {key}")
    return errors, warnings


def owned_files(root):
    excluded = {'.git','.agents','.codex','__pycache__','.venv','node_modules','build','dist',
                'target','private','raw-private','checkouts'}
    def walk(folder):
        for path in sorted(folder.iterdir()):
            if (path.is_symlink() or path.name in excluded or path.name.startswith('.env')
                    or path.name.startswith('secrets.') or path.name=='credentials.json'):
                continue
            relative = path.relative_to(root)
            if 'source' in relative.parts and relative.parts[0]=='books':
                if path.is_dir():
                    readme = path/'README.md'
                    if readme.is_file() and not readme.is_symlink():
                        yield readme
                continue
            if path.is_dir():
                yield from walk(path)
            elif path.suffix in {'.md','.py','.json','.c','.h','.s','.sv','.vhd','.sh'}:
                yield path
    return list(walk(root))


def validate_files(root, data):
    errors = []
    for path in owned_files(root):
        text = path.read_text()
        rel = str(path.relative_to(root))
        if not text.endswith('\n'):
            errors.append(f'{rel}: missing final newline')
        if any(line.rstrip()!=line for line in text.splitlines()):
            errors.append(f'{rel}: trailing whitespace')
        if path.suffix!='.md':
            continue
        # This repository uses inline Markdown links, not reference-link definitions.
        prose = re.sub(r'```.*?```','',text,flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',prose):
            target = unquote(target.strip('<>'))
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            destination = (path.parent/target.split('#',1)[0]).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'{rel}: broken or escaping internal link {target}')
    for name,text in documents(data).items():
        p = root/name
        if not p.exists() or p.read_text()!=text:
            errors.append(f'{name}: generated index drift; run python3 tools/render.py')
    for category, parent in [('projects','projects'),('experiments','experiments')]:
        registered = {r.get('path') for r in data[category]}
        for p in (root/parent).iterdir():
            if p.is_dir() and not p.is_symlink() and str(p.relative_to(root)) not in registered:
                errors.append(f'{parent}: unregistered artifact directory {p.name}')
    registered_chapters = {c['path'] for c in data['chapters']}
    for p in (root/'books').glob('*/generated/chapters/*'):
        if p.is_dir() and str(p.relative_to(root)) not in registered_chapters:
            errors.append(f'unregistered chapter directory {p.relative_to(root)}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict',action='store_true',help='Also fail on known source/license gaps.')
    args = parser.parse_args()
    try:
        data = json.loads((ROOT/'registries/catalog.json').read_text())
        errors,warnings = validate_catalog(data)
        if not schema_errors(data):
            errors += validate_files(ROOT,data)
    except (OSError, ValueError) as exc:
        print(f'ERROR: cannot validate catalog/files: {exc}')
        return 1
    for message in errors:
        print('ERROR: '+message)
    for message in warnings:
        print('WARNING: '+message)
    print(f'{len(errors)} errors; {len(warnings)} known source/license warnings.')
    print('Structural validation only: no claim truth, license clearance or learner mastery is certified.')
    return int(bool(errors or args.strict and warnings))


if __name__=='__main__':
    raise SystemExit(main())
