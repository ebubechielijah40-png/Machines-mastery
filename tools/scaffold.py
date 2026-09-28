#!/usr/bin/env python3
"""Prepare one book or registered project. Never write source contents or learning results."""
import argparse
import json
import re
import tempfile
from pathlib import Path

from validate import ROOT, safe_path


def save_catalog(root, data):
    with tempfile.NamedTemporaryFile(mode='w',dir=root/'registries',prefix='.catalog-',
                                     suffix='.tmp',delete=False) as handle:
        json.dump(data,handle,indent=2,ensure_ascii=False)
        handle.write('\n')
        temp = Path(handle.name)
    temp.replace(root/'registries/catalog.json')


def scaffold(root, kind, id, slug=None, project_id=None):
    data = json.loads((root/'registries/catalog.json').read_text())
    if kind=='project':
        rows = [p for p in data['projects'] if p['id']==id]
        if len(rows)!=1:
            raise ValueError('Expected one registered project ID.')
        record = rows[0]
        if record['status']!='PLANNED' or record.get('path'):
            raise ValueError('Only unmaterialized PLANNED projects can be scaffolded.')
        slug = record['slug']
        relative = 'projects/'+slug
        templates = json.loads((root/'templates/project-documents.json').read_text())
        texts = {name: f"# {record['title']} — {name[:-3].replace('_',' ').title()}\n\n"
                 f"Project {id} / {record['phase']}. PREPARED; Stage A — NOT STARTED.\n\n"
                 f"{prompt}\n\nIntended outcome: {record['outcome']}\n\n"
                 f"Candidate original resource IDs: {', '.join(record['original_resources'])}. "
                 'Inspect and verify exact attribution before reproduction.\n'
                 for name,prompt in templates.items()}
        record.update(path=relative,status='PREPARED')
    elif kind=='book':
        rows = [r for r in data['resources'] if r['id']==id and r['type']=='book']
        if len(rows)!=1 or any(b['resource_id']==id for b in data['books']):
            raise ValueError('Expected a registered book without an existing intake.')
        resource = rows[0]
        relative = 'books/'+str(slug)
        common = f"Resource {id}: {resource['title']}.\n\nSOURCE NOT PRESENT. "
        prompts = {
            'README.md':'Place a legally available source under source/; inspect it before mapping. No chapter processed.',
            'source/README.md':'Local originals are ignored by Git. Do not store credentials or purchase receipts. Preserve the source unchanged.',
            'generated/BOOK_MAP.md':'NOT MAPPED. After inspection, map exact chapters/sections, dependencies, depth classes and project/experiment relevance. Do not substitute internet summaries.',
            'generated/CONCEPT_INDEX.md':'No source-derived concepts indexed. Add actual locators, claim IDs and artifact links after inspection.',
            'generated/PREREQUISITES.md':'Book-specific requirements: UNVERIFIED — source required. Use the curriculum entry gates provisionally; learner evidence remains absent.',
            'generated/SOURCE_INDEX.md':'Actual edition, path, fingerprint and readability: UNVERIFIED — source required. Record title-page evidence and locator convention before changing status.'}
        texts = {name: f'# {name[:-3].split("/")[-1].replace("_"," ").title()}\n\n{common}{prompt}\n'
                 for name,prompt in prompts.items()}
        data['books'].append(dict(resource_id=id,slug=slug,path=relative,status='SOURCE NOT PRESENT',
                                 source_path=None,sha256=None,edition=None,inspection_evidence=None))
    elif kind=='experiment':
        if not re.fullmatch(r'E-[0-9]+',id) or any(e['id']==id for e in data['experiments']):
            raise ValueError('Expected a new experiment ID such as E-002.')
        matches = [p for p in data['projects'] if p['id']==project_id]
        if len(matches)!=1:
            raise ValueError('Expected one registered parent project.')
        project = matches[0]
        relative = 'experiments/'+id+'-'+str(slug)
        template = (root/'templates/experiment.md').read_text()
        texts = {'README.md': template.replace('# Experiment Protocol Template',
            f'# {id} — {slug}\n\nProject {project_id} / {project["phase"]}. PLANNED; source-ready: false.',1)}
        data['experiments'].append(dict(id=id,title=str(slug).replace('-',' ').title(),
            phase=project['phase'],project=project_id,path=relative,status='PLANNED',
            observed_result='NOT YET OBSERVED',evidence=[],
            resources=project['original_resources'][:],source_ready=False))
    else:
        raise ValueError('Unknown scaffold kind.')
    if not slug or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
        raise ValueError('Slug must use lowercase letters/digits separated by hyphens.')
    destination = safe_path(root,relative)
    if destination.exists():
        raise ValueError('Destination already exists; refusing to overwrite.')
    # Preflight every path; no content is written before these checks.
    for name in texts:
        safe_path(root,relative+'/'+name)
    destination.mkdir()
    for name,text in texts.items():
        path = destination/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x') as handle:
            handle.write(text)
    save_catalog(root,data)
    return relative


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='kind',required=True)
    project = sub.add_parser('project')
    project.add_argument('id')
    book = sub.add_parser('book')
    book.add_argument('id')
    book.add_argument('slug')
    experiment = sub.add_parser('experiment')
    experiment.add_argument('id')
    experiment.add_argument('slug')
    experiment.add_argument('--project',required=True)
    args = parser.parse_args()
    try:
        path = scaffold(ROOT,args.kind,args.id,getattr(args,'slug',None),getattr(args,'project',None))
    except (ValueError,OSError) as exc:
        raise SystemExit(f'Refused/failed: {exc}')
    print(f'Prepared {path}; no source processed, implementation created or learning state advanced.')
    print('Review files, then run python3 tools/render.py and python3 tools/validate.py.')


if __name__=='__main__':
    main()
