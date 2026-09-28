#!/usr/bin/env python3
"""Check expansion artifact contracts; scaffolds never count as completed lessons."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ['01-c','02-cpp','03-rust','04-zig','05-x86-64-assembly','06-arm64-assembly',
             '07-riscv-assembly','08-python','09-go','10-java','11-sql','12-shell-bash','13-systemverilog','14-vhdl']
EXEMPLARS = {
    'U-CEX': ['LESSON.md','SOURCES.md','MASTERY.md','problems/README.md','hints/README.md','solutions/parser.c','tests/run.py'],
    'U-RVEX': ['LESSON.md','SOURCES.md','MASTERY.md','problems/README.md','hints/README.md','solutions/model.py','solutions/program.s','tests/run.py'],
    'U-SVEX': ['LESSON.md','SOURCES.md','MASTERY.md','problems/README.md','hints/README.md','solutions/register.sv','solutions/broken_priority.sv','tests/tb.sv','tests/run.py'],
    'U-REEX': ['prompt.md','hints/README.md','oracle.py','reveal/solution.md','reveal/replica.py','tests/test_oracle.py'],
    'U-PROD': ['service.py','benchmark.py','tests/test_ledger.py','DESIGN.md','ARCHITECTURE.md','ASSUMPTIONS.md','BENCHMARKS.md','FAILURES.md','EXPERIMENTS.md','SECURITY.md','OBSERVABILITY.md','SCALABILITY.md','POSTMORTEMS.md','RESULTS.md'],
}


def validate(data, root=ROOT):
    errors=[]
    def require(relative):
        p=root/relative
        if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()) or not p.is_file() or not p.stat().st_size:
            errors.append('missing/unsafe expansion artifact '+relative)
    lessons={l['id']:l for l in data.get('lessons',[])}
    for uid,files in EXEMPLARS.items():
        if uid not in lessons:
            errors.append('missing exemplar '+uid);continue
        for name in ['README.md','PREREQUISITE_BRIDGE.md',*files]:
            require(lessons[uid]['path']+'/'+name)
    for slug in LANGUAGES:
        base=root/'programming-languages-mastery'/slug
        require(str(base.relative_to(root))+'/README.md')
        for index in range(28):
            matches=list(base.glob(f'{index:02}_*.md'))
            if len(matches)!=1:
                errors.append(f'{slug}: expected one scope file for {index:02}')
    re=root/'reverse-engineering-systems'
    for index in range(29):
        if len(list(re.glob(f'{index:02}_*.md')))!=1:
            errors.append(f'reverse engineering: missing/duplicate method {index:02}')
    plan=data.get('expansion_plan',{})
    if plan.get('problems_per_topic',0)<20 or plan.get('papers_per_domain',0)<10:
        errors.append('release quotas weakened')
    if len(plan.get('algorithm_topics',[]))<31 or len(plan.get('paper_domains',[]))<18:
        errors.append('topic/domain coverage weakened')
    for topic in plan.get('algorithm_topics',[]):
        require('algorithmic-problem-solving/topics/'+topic+'/README.md')
    for domain in plan.get('paper_domains',[]):
        require('research-paper-reconstruction/domains/'+domain+'/README.md')
    for topic in plan.get('completed_algorithm_topics',[]):
        if topic not in plan.get('algorithm_topics',[]): errors.append('unknown completed algorithm topic '+topic)
        problems=list((root/'algorithmic-problem-solving/topics'/topic/'problems').glob('*/prompt.md'))
        if len(problems)<20: errors.append(topic+': completed topic needs 20 real problems')
        for prompt in problems:
            for name in ['hints.md','solution.md']:
                require(str((prompt.parent/name).relative_to(root)))
            if not any((prompt.parent/'tests').glob('*')):
                errors.append(topic+': missing executable problem tests')
    for domain in plan.get('completed_paper_domains',[]):
        if domain not in plan.get('paper_domains',[]): errors.append('unknown completed paper domain '+domain)
        rows=[p for p in data.get('papers',[]) if p.get('domain')==domain and p.get('metadata_verified') is True]
        if len(rows)<10: errors.append(domain+': completed domain needs ten verified papers')
    for category in plan.get('machine_categories',[]):
        require('general-machine-systems/units/'+category+'/README.md')
    units={u['id']:u for u in data.get('units',[])}
    for uid in [f'U{i:02}' for i in range(22)]:
        if uid not in units: errors.append('original unit removed '+uid)
    for uid in ('U-CEX','U-RVEX','U-SVEX','U-REEX','U-PROD'):
        if not units.get(uid,{}).get('required'): errors.append('ungated exemplar '+uid)
    return errors


def main():
    data=json.loads((ROOT/'registries/catalog.json').read_text())
    errors=validate(data)
    for error in errors: print('ERROR: '+error)
    print(f'{len(errors)} expansion errors; counts check artifacts, not teaching quality or mastery.')
    return int(bool(errors))


if __name__=='__main__': raise SystemExit(main())
