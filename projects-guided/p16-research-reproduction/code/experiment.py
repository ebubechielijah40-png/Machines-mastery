"""Original finite-trace intervention experiment; JSON to stdout only."""
import json
import platform
import sys
from logical_clocks import Event, happened_before, stamp, total_order, violations


def main():
    events=[Event('a','A'),Event('b','A'),Event('s','A','send','m','B'),
            Event('r','B','receive','m','A'),Event('c','B'),Event('u','C')]
    results=[]
    for rule in ['lamport','ignore-message','non-strict']:
        times=stamp(events,rule)
        results.append({'rule':rule,'timestamps':times,'violations':violations(events,times)})
    correct=stamp(events)
    relation=happened_before(events)
    false_causal=[(a.name,b.name) for a in events for b in events
                  if correct[a.name]<correct[b.name] and (a.name,b.name) not in relation]
    print(json.dumps({'kind':'synthetic finite-trace mechanism reconstruction; not a live-system benchmark',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'events':[e.__dict__ for e in events], 'causal_pairs':sorted(relation),
        'rule_interventions':results,'smaller_timestamp_without_causal_path':false_causal,
        'offline_total_order':total_order(events,correct)},indent=2))


if __name__=='__main__':main()
