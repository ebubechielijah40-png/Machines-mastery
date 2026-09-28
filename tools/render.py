#!/usr/bin/env python3
"""Render human-readable indexes from the local catalog. No network access."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = '<!-- Generated from registries/catalog.json by tools/render.py; edit the catalog. -->'


def cell(value):
    if isinstance(value, list):
        value = ', '.join(value) or 'None'
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows])


def documents(data):
    docs = {}
    resources = data['resources']
    body = ['# Resource Registry', MARKER,
            'Identity verification is not content verification, local availability or license clearance. '
            'Purpose, prerequisites and selection reasons are curriculum design choices. '
            'UNVERIFIED candidates are retained because the owner requested them; they are not approved evidence sources.',
            'See [SOURCES.md](SOURCES.md) for provenance procedures. All check dates refer to actual setup review, not continuous monitoring.']
    for r in resources:
        body += [f"## {r['id']} — {r['title']}", table(['Field', 'Record'], [
            ('Type', r['type']), ('Author/maintainer', r['author']), ('Purpose', r['purpose']),
            ('Phase', r['phases']), ('Prerequisites', r['prerequisites']),
            ('Why selected', r['why_selected']),
            ('Original source', f"[Primary source]({r['original_source']})"),
            ('License/status', r['license']), ('Verification status', r['verification']),
            ('Verification scope', r['verification_scope']), ('Checked on', r['checked_on']),
            ('Local availability', r['local_availability']), ('Notes', r['notes'])])]
    docs['RESOURCE_REGISTRY.md'] = '\n\n'.join(body)

    body = ['# Master Curriculum', MARKER,
            'This is a dependency-driven plan, not a processed reading list. All learning remains NOT STARTED. '
            'Use [PREREQUISITE_GRAPH.md](PREREQUISITE_GRAPH.md) to select a bounded unit and '
            '[RESOURCE_REGISTRY.md](RESOURCE_REGISTRY.md) to check each source before use.',
            '## Study depth',
            '- **MUST STUDY DEEPLY:** each phase’s core mechanism and required entry bridges; explain, derive, apply and test.\n'
            '- **REFERENCE:** syntax tables, API details, tool flags and catalogs once the mechanism is understood.\n'
            '- **OPTIONAL DEPTH:** advanced extensions with no current dependency; defer with a reason.\n'
            '- **HISTORICAL/CONTEXT:** background that contextualizes a mechanism without gating implementation.\n\n'
            'These are planning rules, not chapter classifications. Classify actual source units only after inspection. '
            'A difficult foundational chapter is still required.',
            '## Dependency corrections',
            'Keep the requested phase progression with small entry bridges: U00 establishes evidence logging at the start; '
            'U05 introduces only the process/descriptor concepts needed for the shell; U06 supplies proof/discrete mathematics before algorithms. '
            'Probability precedes inference and cryptography; linear algebra/calculus precede advanced regression and gradients. '
            'Physical measurement, mechanics and differential equations gate control; chemistry and cell/genetic foundations gate biological interpretation. '
            'These are design decisions preventing specific gaps, not additional survey courses. '
            'Formal scientific reasoning remains P08, but predictions and raw logs begin with the first experiment. '
            'TLS is introduced operationally in P06 and cryptographically in P10. Distributed database sections wait for P13. '
            'P15/P16 do not require completion of unrelated earlier applications; follow the graph.']
    for p in data['phases']:
        body += [f"## {p['id']} — {p['title']}",
                 '**Core scope — MUST STUDY DEEPLY:** ' + p['topics'] + '.',
                 '**Resources:** ' + ', '.join(p['resources']) + '. Verify status before selection.',
                 '**Demonstrable outcome:** ' + p['outcome'],
                 '**Project:** ' + p['project'] + ' in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). '
                 '**Subject paths:** ' + ', '.join(f'[{d}]({d}/README.md)' for d in p['directories']) + '.',
                 '**Learning state:** ' + p['state'] + '.']
    body += ['## Advanced-source selection gates',
             'Before consensus reproduction, select and inspect an original paper with its fault model; '
             'before research reproduction, select one original paper and the relevant domain prerequisites. '
             'No paper, dataset, hardware board or benchmark result has been selected by guesswork. '
             'Rust/Java and mathematical or physical bridges are learned only if the chosen implementation requires them. '
             'Chemistry/physics candidate sources need readable primary verification before study.']
    body += ['## Permanent connected tracks',
             'Prepared exemplars and scaffolded scope are distinct. Learner progress requires actual evidence. '
             'Use internal prerequisite bridges; original sources are the verification layer, not mandatory learner reading.',
             table(['Track', 'Entry gates', 'Integrated units', 'Preparation'], [
                 (f"[{t['title']}]({t['path']}/README.md)", t['required'], t['units'], t['status'])
                 for t in data['tracks']]),
             'Early language use is Shell/Python/C; x86-64 and basic RISC-V follow representation/state; '
             'C++/Rust/Zig enter systems projects; SQL joins databases, Go networking, Java runtimes, '
             'ARM64 embedded systems and SystemVerilog/VHDL digital hardware. Do not finish fourteen courses sequentially.',
             'Prepared foundation bridges descend only as far as needed. Unprepared prerequisite topics block learner '
             'progression rather than silently assuming mathematics, physics, materials or statistics.',
             'Production thinking enters every phase through code, tests, measurements, failure/recovery, '
             'observability and reviewed design decisions. See [production laboratory](production-systems-engineering/README.md).']
    docs['MASTER_CURRICULUM.md'] = '\n\n'.join(body)

    body = ['# Prerequisite Graph', MARKER,
            'These edges are curriculum planning decisions, not established knowledge or evidence of mastery. '
            'A unit ID means the bounded capability in its exit gate, not completion of an entire field. '
            'Check learner evidence in [MASTERY.md](MASTERY.md). '
            'Concurrent means compatible after each unit’s own required gates, never permission to skip prerequisites.',
            '## Required dependency graph', '```mermaid\ngraph TD\n' + '\n'.join(
                f'  {u["id"]}["{u["id"]}: {u["title"]}"]' for u in data['units']) + '\n' + '\n'.join(
                f'  {r} --> {u["id"]}' for u in data['units'] for r in u['required']) + '\n```',
            '## Entry gates and concurrency', table(['Unit', 'Required', 'Recommended', 'Concurrent', 'Resources'], [
                (u['id'] + ' — ' + u['title'], u['required'], u['recommended'], u['concurrent'], u['resources']) for u in data['units']])]
    for u in data['units']:
        body += [f"## {u['id']} — {u['title']}", f"Phase {u['phase']}. State: {u['state']}.\n\nExit evidence: {u['exit_gate']}"]
    body += ['## First unit', 'U00 is the entry protocol; U01 is the first subject unit. '
             'For current source readiness and the bounded first learning unit, '
             'see [FIRST_UNIT.md](01-computation/FIRST_UNIT.md). Internal foundations precede the existing Code reconstruction when learner evidence is absent.']
    body += ['## Internal prepared/scaffolded learning paths',
             table(['Unit', 'Artifact', 'Learner gate'], [
                 (u['id'], f"[Internal lesson or map]({u['path']})", 'Evidence required; use tools/learning_gate.py')
                 for u in data['units'] if 'path' in u]),
             'The graph is regenerated from catalog required edges. Prepared material does not satisfy a prerequisite. '
             'Check every discipline in PREREQUISITE_BRIDGE.md; scaffolded future lessons remain blocked for study.']
    docs['PREREQUISITE_GRAPH.md'] = '\n\n'.join(body)

    docs['PROJECT_REGISTRY.md'] = '\n\n'.join(['# Project Registry', MARKER,
        'Only PREPARED projects have materialized documentation. PLANNED entries are bounded future work, not implementations. '
        'All stages start at A; no completion or authorship is implied. '
        'See [project workflow](projects/README.md). J-04 groups allocator, compiled-program inspection and systems experiments; '
        'J-06 groups TCP server, HTTP server and a small networked system.',
        table(['ID / phase', 'Project', 'Status / stage', 'Original resource candidates', 'Outcome'], [
            (p['id']+' / '+p['phase'], f"[{p['title']}]({p['path']}/README.md)" if p['path'] else p['title'],
             p['status']+' / '+p['stage'],p['original_resources'],p['outcome']) for p in data['projects']]),
        'Original resource candidates must be narrowed and attributed before reproduction. '
        'No unverified author or license may be inferred from the registry. Every materialized project carries its own attribution and quality gates.'])
    docs['EXPERIMENT_REGISTRY.md'] = '\n\n'.join(['# Experiment Registry', MARKER,
        'Planned protocols are not observations. See [experiment workflow](experiments/README.md).',
        table(['ID', 'Protocol', 'Project / phase', 'Status', 'Observed result', 'Evidence'], [
            (e['id'],f"[{e['title']}]({e['path']}/README.md)",e['project']+' / '+e['phase'],
             e['status'],e['observed_result'],e['evidence']) for e in data['experiments']])])
    books = {b['resource_id']: b for b in data['books']}
    docs['BOOK_REGISTRY.md'] = '\n\n'.join(['# Book Registry', MARKER,
        'A resource can be identified online while its actual study source is absent. '
        'Only selected books are scaffolded. Prepared chapter counts describe artifacts, never learner progress.',
        table(['Resource', 'Title', 'Local intake', 'Edition of local source', 'Generated work'], [
            (r['id'],r['title'],f"[{books[r['id']]['status']}]({books[r['id']]['path']}/README.md)" if r['id'] in books else 'SOURCE NOT PRESENT — not scaffolded',
             books.get(r['id'],{}).get('edition') or 'UNVERIFIED',
             ('Prepared chapters: ' + str(sum(c['resource_id']==r['id'] for c in data['chapters']))) if r['id'] in books else 'None') for r in resources if r['type']=='book'])])
    docs['REPOSITORY_REGISTRY.md'] = '\n\n'.join(['# Repository Registry', MARKER,
        'Identity verified at the linked original repository only. No local checkouts, pinned revisions, code traces or executed upstream tests exist yet. '
        'Use [repository study workflow](repositories/README.md) before making behavior claims.',
        table(['Resource', 'Original repository', 'Owner/maintainer evidence', 'Phase', 'License status', 'Study status'], [
            (r['id'],f"[{r['title']}]({r['original_source']})",r['author'],r['phases'],r['license'],'NOT STARTED') for r in resources if r['type']=='repository'])])
    return {k: v.strip()+'\n' for k,v in docs.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail on drift; write nothing.')
    args = parser.parse_args()
    data = json.loads((ROOT/'registries/catalog.json').read_text())
    outputs = documents(data)
    stale = [name for name,text in outputs.items() if not (ROOT/name).exists() or (ROOT/name).read_text()!=text]
    if args.check:
        for name in stale:
            print('STALE: '+name)
        print(f'{len(outputs)} generated indexes checked; {len(stale)} stale.')
        return bool(stale)
    # Preflight every destination before any writes.
    for name in outputs:
        p = ROOT/name
        if p.exists() and p.stat().st_size and MARKER not in p.read_text():
            raise SystemExit(f'Refusing to overwrite unmarked document: {name}')
    for name,text in outputs.items():
        (ROOT/name).write_text(text)
    print(f'Rendered {len(outputs)} indexes; no learning state changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
