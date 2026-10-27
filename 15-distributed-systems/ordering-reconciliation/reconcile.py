"""Original in-memory stamp-max map and explicit logical clocks.

No consensus, persistence, membership protocol, authentication or physical clock.
Valid histories require unique node IDs and no counter reuse after a restart.
"""
from dataclasses import dataclass

MAX_COUNTER = 2**63 - 1


def _counter(value):
    if type(value) is not int or not 0 <= value < MAX_COUNTER:
        raise ValueError('counter outside bounded domain')


def _text(value, limit):
    return isinstance(value, str) and 1 <= len(value) <= limit


@dataclass(frozen=True)
class Record:
    key: str
    value: str | None  # None is a retained deletion tombstone, not a missing record.
    counter: int
    origin: str

    @property
    def stamp(self):
        return self.counter, self.origin

    def validate(self):
        _counter(self.counter)
        if self.counter == 0 or not _text(self.key, 256) or not _text(self.origin, 64):
            raise ValueError('positive counter and bounded key/origin required')
        if self.value is not None and (not isinstance(self.value, str) or len(self.value) > 4096):
            raise ValueError('bounded string payload or deletion required')


@dataclass(frozen=True)
class Envelope:
    counter: int
    records: tuple


class LogicalClock:
    def __init__(self, value=0):
        _counter(value)
        self.value = value

    def event(self):
        return self.receive(0)

    def receive(self, message_stamp):
        _counter(message_stamp)
        proposed = max(self.value, message_stamp) + 1
        _counter(proposed)
        self.value = proposed
        return proposed


def join_states(*states):
    """Pure keywise maximum on valid single-payload timestamp histories.

    Reject conflicts visible in this merge, before returning any new state.
    This does not authenticate origin claims or retain every discarded event.
    """
    winners, known = {}, {}
    for state in states:
        for record in state:
            if not isinstance(record, Record):
                raise ValueError('Record instances required')
            record.validate()
            previous = known.get(record.stamp)
            if previous is not None and previous != record:
                raise ValueError('same event stamp has conflicting payload or key')
            known[record.stamp] = record
            old = winners.get(record.key)
            if old is None or record.stamp > old.stamp:
                winners[record.key] = record
    return tuple(winners[key] for key in sorted(winners))


class Replica:
    def __init__(self, node_id):
        if not _text(node_id, 64):
            raise ValueError('bounded unique node ID required')
        self.node_id = node_id
        self.clock = LogicalClock()
        self._state = ()

    def snapshot(self):
        return self._state  # Frozen records and tuple prevent external mutation.

    def visible(self):
        return {r.key: r.value for r in self._state if r.value is not None}

    def put(self, key, value):
        proposed = Record(key, value, self.clock.value + 1, self.node_id)
        proposed.validate()
        state = join_states(self._state, (proposed,))
        self.clock.event()
        self._state = state
        return proposed

    def delete(self, key):
        return self.put(key, None)

    def send(self):
        # A state exchange is also an event, even if no record changed.
        stamp=self.clock.event()
        return Envelope(stamp,self.snapshot())

    def receive(self, envelope):
        if not isinstance(envelope,Envelope) or not isinstance(envelope.records,tuple):
            raise ValueError('immutable timestamped Envelope required')
        _counter(envelope.counter)
        state=join_states(self._state,envelope.records)
        if envelope.counter < max((r.counter for r in envelope.records),default=0):
            raise ValueError('message predates its records')
        next_value=max(self.clock.value,envelope.counter)+1
        _counter(next_value)
        changed=state!=self._state
        self.clock.receive(envelope.counter)
        self._state=state
        return changed

    def merge(self, remote):
        """Local state join with record-observation ordering only.

        Use send/receive for a channel event: bare records omit the sender clock.
        """
        remote = tuple(remote)
        state = join_states(self._state, remote)
        largest = max((r.counter for r in remote), default=0)
        # Validate the next clock before mutating either clock or map.
        next_value = max(self.clock.value, largest) + 1
        _counter(next_value)
        changed = state != self._state
        self.clock.receive(largest)
        self._state = state
        return changed
