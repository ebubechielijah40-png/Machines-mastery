"""Validate reviewed requirement marks and render the STRONG readiness dashboard.

The arithmetic is automated; the qualitative marks and approval gates are not.
No file count, word count or green process automatically grants a rating.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=dict(instruction=25,implementation=20,reproduction=20,assessment=15,prerequisites=10,references=10)


def scores(domain, snapshot='current'):
    marks=domain[snapshot]
    if set(marks)!=set(WEIGHTS):
        raise ValueError('six mandated criteria required')
    out={}
    for name,values in marks.items():
        if type(values) is not list or len(values)!=4 or any(type(x) is not int or not 0<=x<=2 for x in values):
            raise ValueError('each criterion requires four reviewed integer marks0..2')
        out[name]=Fraction(100*sum(values),8)
    total=sum((out[k]*w/100 for k,w in WEIGHTS.items()),Fraction())
    return out,total


def rating(domain):
    criteria,total=scores(domain)
    if domain['mandatory_blockers']:
        return 'BLOCKED'
    gate=(total>=85 and min(criteria.values())>=70 and domain['tests_passed']
          and domain['independent_review'] and domain['scope_breadth_confirmed']
          and not domain['critical_errors'])
    return 'STRONG' if gate else 'SCAFFOLDED' if total<40 else 'PARTIAL'


def computed(domain):
    criteria,total=scores(domain)
    return dict(criterion_percentages={k:float(v) for k,v in criteria.items()},
                readiness_percent=float(total),rating=rating(domain),
                remaining_to_strong_threshold=float(max(Fraction(),85-total)),
                remaining_to_full_readiness=float(100-total))


def aggregates(data):
    domains=data['domains']
    return dict(domain_count=len(domains),strong_count=sum(rating(d)=='STRONG' for d in domains),
                strong_readiness_percent=float(sum((scores(d)[1] for d in domains),Fraction())/len(domains)),
                original_excellent_closed=sum(d['original_mandate_excellent_gate_closed'] for d in domains))


def validate(data, root=ROOT, check_computed=True):
    if data.get('weights')!=WEIGHTS:
        raise ValueError('mandated weights cannot be changed')
    ids=set()
    for d in data['domains']:
        if d['id'] in ids:raise ValueError('duplicate domain')
        ids.add(d['id'])
        frozen=json.dumps({k:d[k] for k in ('strong_scope','full_mandate_scope')},sort_keys=True).encode()
        if hashlib.sha256(frozen).hexdigest()!=d['scope_sha256']:
            raise ValueError('scope changed after baseline: '+d['id'])
        scores(d,'before');scores(d)
        if 'previous' in d:scores(d,'previous')
        if check_computed and 'computed' in d and d['computed']!=computed(d):
            raise ValueError('stale derived accounting: '+d['id'])
        for field in ('tests_passed','independent_review','scope_breadth_confirmed','original_mandate_excellent_gate_closed'):
            if type(d[field]) is not bool:raise ValueError('gate flags must be bool')
        for field in ('critical_errors','mandatory_blockers','missing_requirements'):
            if not isinstance(d[field],list):raise ValueError('gate gaps must be explicit lists')
        for paths in d['criterion_evidence'].values():
            for relative in paths:
                p=(root/relative).resolve()
                if not p.is_relative_to(root.resolve()) or not p.exists():
                    raise ValueError('missing/escaping evidence: '+relative)
        if any(not (root/p).exists() for p in d['review_basis']):
            raise ValueError('missing qualitative review record')
    if not set(data['initial_near_strong_group'])<=ids:
        raise ValueError('unknown near-STRONG candidate')
    if len(ids)!=33:raise ValueError('all33 frozen domains must remain in the denominator')
    if check_computed and 'aggregate_metrics' in data and data['aggregate_metrics']!=aggregates(data):
        raise ValueError('stale aggregate accounting')


def render(data):
    domains=data['domains']
    ranked=sorted((d for d in domains if rating(d)!='STRONG'),
                  key=lambda d:(-scores(d)[1],sum(d['estimate_active_hours']),d['learner_stage']))
    priority={d['id']:i+1 for i,d in enumerate(ranked)}
    rows=['# STRONG readiness dashboard','',
          'Readiness scores apply to fixed scopes in [strong_progress.json](registries/strong_progress.json), with24 reviewed checks and25/20/20/15/10/10 weights. Before remains the recovered4ced936 baseline. Previous is the last reviewed domain checkpoint; current is the latest reviewed evidence. To85=max(0,85-readiness) is arithmetic distance to the threshold, never a replacement for breadth, tests or qualitative gates. Scores are reviewer judgments, not measured percentages of all field knowledge.','',
          'STRONG additionally requires every criterion≥70, passed core tests, meaningful breadth, independent qualitative review and no critical errors or mandatory blockers. A score alone cannot grant it. Estimates are active development/validation hours under available tools, not elapsed-time or credit guarantees.','',
          '| Domain | Before % | Previous % | Current % | Rating | To85 % | Estimated active hours | Priority |',
          '| --- | ---: | ---: | ---: | --- | ---: | --- | --- |']
    for d in sorted(domains,key=lambda d:(0 if rating(d)=='STRONG' else priority[d['id']],d['id'])):
        current=scores(d)[1];before=scores(d,'before')[1]
        hours=d['estimate_active_hours']
        previous=scores(d,'previous' if 'previous' in d else 'before')[1]
        rows.append(f"| {d['name']} | {float(before):.2f} | {float(previous):.2f} | {float(current):.2f} | {rating(d)} | {float(max(Fraction(),85-current)):.2f} | {hours[0]}–{hours[1]} ({d['estimate_confidence']}) | {'Maintain' if rating(d)=='STRONG' else priority[d['id']]} |")
    aggregate=sum((scores(d)[1] for d in domains),Fraction())/len(domains)
    closed=sum(d['original_mandate_excellent_gate_closed'] for d in domains)
    rows+=['',f"**STRONG domains: {sum(rating(d)=='STRONG' for d in domains)}/{len(domains)}.**",
           '',f'**A. Domain STRONG readiness index: {float(aggregate):.2f}%.** Equal domain weighting; book/project scopes overlap, so this is an administrative index, not a learning measurement.',
           '',f'**B. Original EXCELLENT mandate: {closed}/{len(domains)} full domain gates closed ({100*closed/len(domains):.2f}%).** This conservative closure metric can remain0 despite substantial bounded work. No guessed overall effort-completion percentage is substituted. Full-scope ratings and gaps remain in [the original-mandate audit](FINAL_EXCELLENCE_AUDIT.md).','',
           '## Fixed first group and next learner stage','',
           'Initial closest group: '+', '.join(data['initial_near_strong_group'])+'. '+data['selection_rule'],
           '',f"Current phase: `{data['phase']}`. The continuous mandate removes the historical decision pause. Close credible near-STRONG gaps automatically, then follow the earliest unfinished learner prerequisite.",
           '', 'After this group, the earliest unfinished learner stage is scientific reasoning/experimental design in stage1; later dependencies stay in the backlog. Algorithms retain the validated foundational-release STRONG scope and receive maintenance only.',
           '', '## Criterion evidence','',
           'The JSON retains all four marks for each criterion, file paths, explicit gaps, critical blockers, test/review gates, immutable scope fingerprint, estimate confidence and changes since baseline. [The rubric and qualitative review](research/quality/2026-10-25/baseline-qualitative-review.md) explains the judgments.']
    for d in domains:
        c,total=scores(d)
        rows+=['',f"### {d['name']}",'',d['strong_scope'],'',
               '; '.join(k+' '+f'{float(v):.1f}%' for k,v in c.items())+'.',
               '', 'Remaining mandatory/scoped requirements: '+ ' '.join(d['missing_requirements']),
               '', 'Review: '+', '.join(f'[{p}]({p})' for p in d['review_basis'])+'.',
               '', 'Validation: '+(', '.join(f'[{p}]({p})' for p in d.get('validation_records',[])) or 'See criterion-level paths in JSON; no new gate inferred.')]
    return '\n'.join(rows)+'\n'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=json.loads((ROOT/'registries/strong_progress.json').read_text())
    validate(data,check_computed=args.check)
    if not args.check:
        for d in data['domains']:d['computed']=computed(d)
        data['aggregate_metrics']=aggregates(data)
        (ROOT/'registries/strong_progress.json').write_text(json.dumps(data,indent=2)+'\n')
    text=render(data);p=ROOT/'STRONG_PROGRESS_DASHBOARD.md'
    if args.check:
        if not p.exists() or p.read_text()!=text:raise SystemExit('dashboard differs from reviewed marks')
    else:p.write_text(text)
    print('Reviewed marks validated; '+str(len(data['domains']))+' domain cards; no learner mastery assigned.')


if __name__=='__main__':main()
