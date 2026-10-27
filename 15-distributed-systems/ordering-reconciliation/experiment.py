from dataclasses import asdict
from datetime import datetime, timezone
import itertools
import json
import platform
from reconcile import Record, Replica, join_states


def view(replica):
    return {'clock': replica.clock.value, 'visible': replica.visible(),
            'state': [asdict(r) for r in replica.snapshot()]}


if __name__ == '__main__':
    a, b = Replica('A'), Replica('B')
    a.put('x', 'A-first'); b.put('x', 'B-first')
    partitioned = {'A': view(a), 'B': view(b)}
    a0, b0 = a.send(), b.send()
    a.receive(b0); b.receive(a0)
    healed = {'A': view(a), 'B': view(b)}
    a.put('x', 'A-after-receive')
    b.receive(a.send())
    causally_later = {'A': view(a), 'B': view(b)}
    stale = a.send()
    b.delete('x'); a.receive(b.send()); b.receive(stale)
    deletion = {'A': view(a), 'B': view(b)}
    events = (Record('x', 'a', 1, 'A'), Record('x', 'b', 1, 'B'),
              Record('y', 'old', 2, 'A'), Record('y', 'new', 3, 'B'))
    expected = join_states(events)
    outcomes = []
    for order in itertools.permutations(events):
        replica = Replica('C')
        for record in order + order[:2]: replica.merge((record,))
        outcomes.append(replica.snapshot() == expected)
    print(json.dumps({'executed_utc': datetime.now(timezone.utc).isoformat(),
                      'python': platform.python_version(), 'platform': platform.platform(),
                      'partitioned': partitioned, 'after_full_state_exchange': healed,
                      'after_causally_later_write': causally_later, 'after_delete_and_stale_replay': deletion,
                      'permutations': len(outcomes), 'matching_final_states': sum(outcomes),
                      'scope': 'deterministic in-memory event interleavings; eventual delivery assumed, no consensus/crash/network benchmark'}, indent=2))
