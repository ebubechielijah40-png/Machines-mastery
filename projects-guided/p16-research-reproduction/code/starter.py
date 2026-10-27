"""Runnable learner baseline: repair the local-only receive rule in your copy.

This deliberately wrong algorithm is a negative control, not an unfinished
reference implementation. Hand-trace it before inspecting stamp().
"""
import json
from logical_clocks import Event, graph, violations


def draft_rule(events):
    events, _ = graph(events)
    counters, times = {}, {}
    for event in events:
        counters[event.process] = counters.get(event.process, 0) + 1
        times[event.name] = counters[event.process]
    return times


if __name__ == '__main__':
    trace = [Event('a', 'A'), Event('b', 'A'),
             Event('send', 'A', 'send', 'm', 'B'),
             Event('receive', 'B', 'receive', 'm', 'A')]
    times = draft_rule(trace)
    print(json.dumps({'baseline': 'deliberately ignores message timestamps',
                      'times': times, 'causal_violations': violations(trace, times),
                      'learner_task': 'derive a receive update that removes violations without changing the graph'}, indent=2))
