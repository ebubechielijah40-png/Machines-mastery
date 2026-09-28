#!/usr/bin/env python3
"""Report just-in-time missing evidence; never change learner state."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABLE = {'APPLICABLE', 'IMPLEMENTABLE', 'DEBUGGABLE', 'EXPERIMENTALLY VERIFIED',
           'RECONSTRUCTABLE', 'TRANSFERABLE', 'PRODUCTION-APPLICABLE', 'SCALABILITY-TESTED',
           'FAILURE-TESTED', 'OPERATIONALLY-UNDERSTOOD', 'MASTERED'}


def missing(data, unit_id):
    units = {u['id']: u for u in data['units']}
    if unit_id not in units:
        raise ValueError('unknown unit ID')
    visited, active, result = set(), set(), []
    def walk(uid):
        if uid in active:
            raise ValueError('prerequisite cycle')
        if uid in visited:
            return
        active.add(uid)
        for dep in units[uid]['required']:
            if dep not in units:
                raise ValueError('unknown prerequisite ' + dep)
            walk(dep)
            row = units[dep]
            reviews = [m for m in data['mastery'] if m['unit_id'] == dep and
                       m['state'] == row['state'] and m['evidence'] and not m['gaps']]
            if row['state'] not in CAPABLE or not row['evidence'] or not reviews:
                if dep not in result:
                    result.append(dep)
        active.remove(uid)
        visited.add(uid)
    walk(unit_id)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('unit_id')
    args=parser.parse_args()
    data=json.loads((ROOT/'registries/catalog.json').read_text())
    try:
        gaps=missing(data,args.unit_id)
    except ValueError as exc:
        parser.error(str(exc))
    units={u['id']:u for u in data['units']}
    for uid in gaps:
        print(uid + ': ' + units[uid].get('path', 'See PREREQUISITE_GRAPH.md; bounded lesson may be scaffolded'))
    print('BLOCKED: learner prerequisite evidence missing.' if gaps else
          'No missing prerequisite records; conduct the lesson diagnostic before study.')
    return int(bool(gaps))


if __name__=='__main__':
    raise SystemExit(main())
