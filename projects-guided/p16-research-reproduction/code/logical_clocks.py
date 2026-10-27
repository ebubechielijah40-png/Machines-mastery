"""Original finite-trace model of Lamport's logical-clock condition.

This is a mechanism reconstruction, not a mutual-exclusion/consensus service.
The trace is a topological delivery schedule of point-to-point messages.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    name: str
    process: str
    action: str = 'local'
    message: str | None = None
    peer: str | None = None


def graph(events):
    """Return generating edges: local sequence plus matching send→receive.

    A send may remain undelivered. Receives must be uniquely matched to a prior
    send with correct endpoints. No restart, ID reuse or Byzantine actor modeled.
    """
    events = tuple(events)
    names, last, sent, received, edges = set(), {}, {}, set(), set()
    for event in events:
        if not isinstance(event, Event):
            raise ValueError('trace entries must be Event objects')
        if not isinstance(event.name, str) or not event.name or event.name in names:
            raise ValueError('event names must be unique nonempty strings')
        if not isinstance(event.process, str) or not event.process:
            raise ValueError('process must be a nonempty string')
        if event.action not in {'local', 'send', 'receive'}:
            raise ValueError('action must be local, send or receive')
        if event.action == 'local':
            if event.message is not None or event.peer is not None:
                raise ValueError('local event has no message or peer')
        else:
            if not isinstance(event.message, str) or not event.message or not isinstance(event.peer, str) or not event.peer:
                raise ValueError('message action needs message ID and peer')
            if event.action == 'send':
                if event.message in sent:
                    raise ValueError('message IDs cannot be reused')
                sent[event.message] = event
            else:
                if event.message not in sent or event.message in received:
                    raise ValueError('receive needs one unmatched earlier send')
                sender = sent[event.message]
                if sender.peer != event.process or event.peer != sender.process:
                    raise ValueError('message endpoints disagree')
                received.add(event.message)
                edges.add((sender.name, event.name))
        if event.process in last:
            edges.add((last[event.process], event.name))
        names.add(event.name)
        last[event.process] = event.name
    return events, frozenset(edges)


def happened_before(events):
    """Graph-search oracle: reachability, without using any clock timestamps."""
    events, edges = graph(events)
    outgoing = {event.name: [] for event in events}
    for a, b in edges:
        outgoing[a].append(b)
    relation = set()
    for event in events:
        pending = list(outgoing[event.name])
        visited = set()
        while pending:
            node = pending.pop()
            if node not in visited:
                visited.add(node)
                relation.add((event.name, node))
                pending.extend(outgoing[node])
    return frozenset(relation)


def stamp(events, rule='lamport'):
    """Timestamp events; broken rules are named controlled interventions.

    lamport: local/send increment; receive=max(local,sent)+1.
    ignore-message: increment only; receive can precede send numerically.
    non-strict: receive=max(local,sent); send/receive can have equal clocks.
    """
    if rule not in {'lamport', 'ignore-message', 'non-strict'}:
        raise ValueError('unknown clock rule')
    events, _ = graph(events)
    clocks, messages, result = {}, {}, {}
    for event in events:
        value = clocks.get(event.process, 0)
        if event.action == 'receive' and rule != 'ignore-message':
            value = max(value, messages[event.message])
            if rule == 'lamport':
                value += 1
        else:
            value += 1
        clocks[event.process] = value
        result[event.name] = value
        if event.action == 'send':
            messages[event.message] = value
    return result


def violations(events, timestamps):
    """Compare all causal pairs, not merely final state or printed time order."""
    events = tuple(events)
    if set(timestamps) != {event.name for event in events}:
        raise ValueError('timestamps must cover exactly the trace events')
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in timestamps.values()):
        raise ValueError('timestamps must be nonnegative integers')
    return sorted((a, b) for a, b in happened_before(events) if timestamps[a] >= timestamps[b])


def total_order(events, timestamps):
    """One deterministic linear extension if timestamps satisfy the condition.

    Process-name lexicographic order breaks ties. Sorting complete offline data
    is not an online delivery protocol: missing events have no completion signal.
    """
    events = tuple(events)
    if violations(events, timestamps):
        raise ValueError('clock condition violated')
    return [e.name for e in sorted(events, key=lambda e: (timestamps[e.name], e.process, e.name))]
