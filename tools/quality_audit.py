#!/usr/bin/env python3
"""Content risk inventory. Findings request review; neither counts nor headings certify quality.

Only parse code; never execute arbitrary Markdown examples or follow symlinks.
Use --report-only to record a known-incomplete baseline without claiming a pass.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'private',
            'raw-private', 'checkouts', 'source', 'build', 'dist', 'target'}
SUPPORT = {'hints', 'solutions', 'tests', 'problems', 'experiments', 'results', 'raw'}
PLACEHOLDERS = [
    r'\b(?:TODO|FIXME|TBD|lorem ipsum)\b',
    r'Identify the real system problem that makes .+ necessary',
    r'Pick one real system in the current phase',
    r'\b(?:insert|write|add) (?:your )?(?:explanation|implementation|citation) here\b',
]


def owned_files(root):
    """Skip symlinks at every level and ignored/private/source trees."""
    def walk(directory):
        for p in sorted(directory.iterdir()):
            if p.is_symlink() or p.name in EXCLUDED:
                continue
            if p.is_dir():
                yield from walk(p)
            elif p.is_file():
                yield p
    yield from walk(root)


def educational_path(relative):
    parts = relative.parts
    return (len(parts) > 1 and parts[0] not in {'tools', 'templates', 'registries',
            'research', 'notes', 'books', 'repositories'} and
            not any(part in SUPPORT for part in parts[1:-1]))


def prose(text):
    return re.sub(r'```.*?```', '', text, flags=re.S)


def destinations(text):
    """Inline links/images and reference definitions, excluding fenced code."""
    text = prose(text)
    for match in re.finditer(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)', text):
        yield match.group(1).strip('<>')
    for match in re.finditer(r'^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)', text, re.M):
        yield match.group(1).strip('<>')


def anchors(text):
    result, counts = set(), Counter()
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.M):
        slug = re.sub(r'[^\w\- ]', '', h.lower().replace('`', '')).replace(' ', '-')
        n = counts[slug]
        result.add(slug + (f'-{n}' if n else ''))
        counts[slug] += 1
    result.update(re.findall(r'\b(?:id|name)=[\"\x27]([^\"\x27]+)', text))
    return result


def evidence_exists(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return False
    parts = Path(relative).parts
    if '..' in parts or any(part in EXCLUDED for part in parts):
        return False
    p = root
    for part in parts:
        p = p/part
        if p.is_symlink():
            return False
    return p.resolve().is_relative_to(root) and p.is_file()


def audit(root):
    root = root.resolve()
    files = list(owned_files(root))
    texts, findings, paragraph_paths = {}, [], defaultdict(set)
    stats = defaultdict(lambda: {'files': 0, 'markdown': 0, 'python': 0})

    def issue(code, path, detail, severity='review'):
        findings.append({'code': code, 'path': str(path), 'severity': severity, 'detail': detail})

    for p in files:
        rel = p.relative_to(root)
        stats[rel.parts[0]]['files'] += 1
        if p.suffix not in {'.md', '.py'}:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeError, OSError) as exc:
            issue('unreadable-text', rel, str(exc), 'error')
            continue
        texts[rel] = text
        if p.suffix == '.py':
            stats[rel.parts[0]]['python'] += 1
            try:
                compile(text, str(rel), 'exec', dont_inherit=True)
            except SyntaxError as exc:
                issue('invalid-python', rel, f'line {exc.lineno}: {exc.msg}', 'error')
            continue
        stats[rel.parts[0]]['markdown'] += 1
        words = len(re.findall(r'\b\w+\b', prose(text)))
        if not text.strip():
            issue('empty-markdown', rel, 'No content.', 'error')
        elif educational_path(rel):
            if words < 100:
                issue('near-empty-instruction', rel, f'{words} prose words; inspect role before judging.')
            for pattern in PLACEHOLDERS:
                m = re.search(pattern, prose(text), re.I)
                if m:
                    issue('placeholder-instruction', rel, m.group(0))
            if not re.search(r'https?://|\b(?:sources?|references?|attribution)\b', text, re.I):
                issue('missing-reference-trail', rel, 'No explicit reference trail detected; may be inherited.')
            if not re.search(r'\b(?:exercise|practice|problem|assessment|reconstruct|assignment|challenge)', text, re.I):
                issue('missing-assessment', rel, 'No assessment detected; inspect linked assessment if any.')
            if not re.search(r'\b(?:experiment|measurement|measured|simulate|simulation|lab)\b', text, re.I):
                issue('missing-experiment', rel, 'No experiment or stated non-applicability detected.')
            for paragraph in re.split(r'\n\s*\n', prose(text)):
                normalized = re.sub(r'\s+', ' ', paragraph.strip()).lower()
                if len(normalized.split()) >= 18 and not normalized.startswith(('#', '|', '<!--')):
                    paragraph_paths[normalized].add(str(rel))
        for language, block in re.findall(r'^```([^\n]*)\n(.*?)^```', text, re.M | re.S):
            if language.strip() not in {'python', 'py'}:
                continue
            if re.search(r'^\s*#\s*(?:pseudocode|fragment|not runnable)', block, re.M | re.I):
                continue
            try:
                compile(block, str(rel)+' (example)', 'exec', dont_inherit=True)
            except SyntaxError as exc:
                issue('invalid-python-example', rel, f'block line {exc.lineno}: {exc.msg}; mark fragments explicitly.', 'error')

    for rel, text in texts.items():
        if rel.suffix != '.md':
            continue
        for destination in destinations(text):
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue
            target = (root/rel.parent/unquote(parsed.path)).resolve() if parsed.path else root/rel
            if not target.is_relative_to(root):
                issue('unsafe-link', rel, destination, 'error')
            elif not target.exists():
                issue('broken-link', rel, destination, 'error')
            elif parsed.fragment and target.is_file() and target.suffix == '.md':
                t = texts.get(target.relative_to(root))
                if t is not None and unquote(parsed.fragment) not in anchors(t):
                    issue('unresolved-anchor', rel, destination)

    duplicates = []
    for paragraph, paths in sorted(paragraph_paths.items(), key=lambda x: (-len(x[1]), x[0])):
        if len(paths) >= 4:
            duplicates.append({'sha256': hashlib.sha256(paragraph.encode()).hexdigest(),
                               'paragraph': paragraph, 'paths': sorted(paths)})
    duplicate_paths = set()
    for item in duplicates:
        duplicate_paths.update(item['paths'])
    for rel in sorted(duplicate_paths):
        issue('repeated-template', rel, 'Shares an identical >=18-word paragraph with at least three other educational files.')

    # A guided build may intentionally share one mechanism with its domain
    # lesson. Resolve only explicit public-file bindings, never guessed links.
    shared_projects = {}
    binding_name = 'registries/project_implementations.json'
    binding_file = root/binding_name
    if binding_file.is_symlink():
        issue('unsafe-project-manifest', binding_name, 'Symlink manifest is not read.', 'error')
    elif evidence_exists(root, binding_name):
        try:
            manifest = json.loads(binding_file.read_text())
            if not isinstance(manifest, dict) or not isinstance(manifest.get('projects'), list):
                raise ValueError('expected an object with a projects list')
            candidate = {}
            for binding in manifest['projects']:
                if not isinstance(binding, dict):
                    raise ValueError('project bindings must be objects')
                readme = binding.get('readme')
                if not evidence_exists(root, readme):
                    raise ValueError('project README must be an existing public file')
                parts = Path(readme).parts
                if len(parts) != 3 or parts[0] != 'projects-guided' or parts[-1] != 'README.md' or readme in candidate:
                    raise ValueError('unique projects-guided/*/README.md binding required')
                if not isinstance(binding.get('scope'), str) or not binding['scope'].strip():
                    raise ValueError('shared mechanism needs an explicit bounded scope')
                for field in ['implementation', 'tests', 'verification']:
                    paths = binding.get(field)
                    if not isinstance(paths, list) or not paths or any(not evidence_exists(root,p) for p in paths):
                        raise ValueError(f'project binding has missing/unsafe {field}')
                code_suffixes = {'.py','.c','.cpp','.rs','.go','.java','.sv','.vhd','.s','.sql'}
                if any(Path(p).suffix not in code_suffixes or Path(p).name.startswith('test') for p in binding['implementation']):
                    raise ValueError('implementation bindings must name source-code files')
                candidate[readme] = binding
            shared_projects = candidate
        except (ValueError, TypeError, AttributeError) as exc:
            issue('invalid-project-bindings', binding_name, str(exc), 'error')

    for readme in sorted((root/'projects-guided').glob('*/README.md')):
        candidates = [p for p in files if p.is_relative_to(readme.parent)]
        implementation = any(p.suffix in {'.py', '.c', '.cpp', '.rs', '.go', '.java', '.sv', '.vhd', '.s', '.sql'}
                             and not p.name.startswith('test') for p in candidates)
        tests = any(p.name.startswith('test') or 'tests' in p.relative_to(readme.parent).parts for p in candidates)
        rel = readme.relative_to(root)
        if str(rel) in shared_projects:
            implementation = tests = True  # Referenced files exist; educational quality is still a review question.
        if not implementation:
            issue('project-no-local-implementation', rel, 'No local implementation; verify any explicitly linked shared implementation.')
        if not tests:
            issue('project-no-local-tests', rel, 'No local tests; verify any explicitly linked executable tests.')

    # Citation records attest an inspection scope, not the truth of arbitrary prose.
    record_file = root/'registries/source_verification.json'
    verified_artifacts = set()
    if record_file.is_symlink():
        issue('unsafe-verification-manifest', record_file.relative_to(root), 'Symlink manifest is not read.', 'error')
    elif evidence_exists(root, 'registries/source_verification.json'):
        try:
            records = json.loads(record_file.read_text())
            if not isinstance(records, dict) or not isinstance(records.get('sources'), list):
                raise ValueError('expected an object with a sources list')
            for record in records['sources']:
                if not isinstance(record, dict):
                    raise ValueError('source records must be objects')
                if record.get('status') in {'INSPECTED', 'FULL_TEXT_INSPECTED'} and record.get('locators') and record.get('url'):
                    evidence = record.get('evidence')
                    if evidence_exists(root, evidence):
                        verified_artifacts.update(record.get('artifacts', []))
        except (ValueError, TypeError, AttributeError) as exc:
            issue('invalid-verification-records', record_file.relative_to(root), str(exc), 'error')
    for rel in sorted(texts):
        if rel.parts[0] == 'research-paper-reconstruction' and re.match(r'^\d+_', rel.name):
            if str(rel) not in verified_artifacts:
                issue('unverified-paper-dossier', rel, 'No inspected-source record maps to this dossier; source identity alone is insufficient.')

    # Completion claims must be backed by review and executable evidence, not counts.
    evidence_file = root/'registries/quality_evidence.json'
    if evidence_file.is_symlink():
        issue('unsafe-quality-manifest', evidence_file.relative_to(root), 'Symlink manifest is not read.', 'error')
    elif evidence_exists(root, 'registries/quality_evidence.json'):
        try:
            records = json.loads(evidence_file.read_text())
            if not isinstance(records, dict) or not isinstance(records.get('units'), list):
                raise ValueError('expected an object with a units list')
            for unit in records['units']:
                if not isinstance(unit, dict):
                    raise ValueError('unit records must be objects')
                classification = unit.get('classification')
                if classification not in {'STRONG', 'EXCELLENT'}:
                    continue
                for field in ['review', 'tests', 'sources', 'experiment', 'assessment']:
                    paths = unit.get(field, [])
                    if not isinstance(paths, list) or not paths or any(not evidence_exists(root,p) for p in paths):
                        code = 'unsupported-excellence-claim' if classification == 'EXCELLENT' else 'unsupported-strong-claim'
                        issue(code, unit.get('path', '?'), f'Missing {field} evidence.', 'error')
        except (ValueError, TypeError, AttributeError) as exc:
            issue('invalid-quality-evidence', evidence_file.relative_to(root), str(exc), 'error')
    for rel in [Path('COMPLETION_REPORT.md'), Path('PROGRESS.md'), Path('README.md')]:
        text = texts.get(rel, '')
        if re.search(r'(?:complete(?:d)?|self-contained|deep guides).*?(?:all 14|every domain|replace mandatory textbook)', text, re.I):
            issue('completion-claim-review', rel, 'Broad coverage claim requires qualitative evidence; this audit does not certify it.')

    catalog_file = root/'registries/catalog.json'
    if evidence_exists(root, 'registries/catalog.json'):
        try:
            catalog = json.loads(catalog_file.read_text())
            resources = {r['id']:r for r in catalog.get('resources', [])}
            for book in catalog.get('books', []):
                if book.get('status') == 'SOURCE NOT PRESENT':
                    availability = resources.get(book.get('resource_id'), {}).get('local_availability', '')
                    if 'SOURCE NOT PRESENT' not in availability and re.search(r'\bINSPECTED\b|\bSOURCE PRESENT\b', availability):
                        issue('contradictory-source-availability', 'registries/catalog.json',
                              str(book.get('resource_id'))+': book source absent but resource availability claims present/inspected.', 'error')
            for topic in catalog.get('expansion_plan', {}).get('completed_algorithm_topics', []):
                base=root/'algorithmic-problem-solving/topics'/topic/'problems'
                for prompt in base.glob('*/prompt.md'):
                    if not any(evidence_exists(root,str((prompt.parent/n).relative_to(root))) for n in ['solution.py','solution.c','solution.cpp','solution.rs']):
                        issue('completed-problem-missing-implementation', str(prompt.relative_to(root)), 'Completed topic lacks an implementation for this problem.', 'error')
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            issue('invalid-catalog-for-audit', 'registries/catalog.json', str(exc), 'error')

    return {'schema_version': 1, 'scope': str(root), 'limitations': [
        'Heuristic review findings are not factual errors or automatic domain ratings.',
        'No external URL availability or source truth validation is performed.',
        'Python compilation does not establish runtime behavior; fragments may need explicit labels.',
        'Declared shared implementation/test bindings check public file existence and scope only; quality still needs review.',
        'Non-English assessment wording and other heuristic matches need manual review.',
        'Link parser covers common inline/reference destinations, not the complete CommonMark grammar.',
        'Sources/private trees and symlinks are excluded; repository content must be trusted before running tests.'],
        'inventory': dict(sorted(stats.items())), 'findings': sorted(findings, key=lambda x: (x['path'], x['code'], x['detail'])),
        'repeated_paragraphs': duplicates, 'counts': dict(sorted(Counter(x['code'] for x in findings).items()))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json', type=Path)
    parser.add_argument('--report-only', action='store_true')
    args = parser.parse_args(argv)
    report = audit(args.root)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'counts': report['counts'], 'total_findings': len(report['findings']),
                      'mode': 'REPORT ONLY — not a quality pass' if args.report_only else 'strict risk gate',
                      'limitations': report['limitations']}, indent=2))
    return 0 if args.report_only else int(bool(report['findings']))


if __name__ == '__main__':
    raise SystemExit(main())
