"""Original deterministic task-output publication model inspired by DG04 §3.3.

An in-memory logical task has one accepted output despite multiple attempts.
There is no filesystem, network, durable master, worker storage or side-effect
transaction here. This model isolates publication; it is not MapReduce itself.
"""
from collections import Counter


def word_counts(records):
    """Whitespace-separated, case-sensitive strings; no linguistic tokenization."""
    result = Counter()
    for record in records:
        if not isinstance(record, str):
            raise ValueError('records must be strings')
        result.update(record.split())
    return dict(result)


def _output(pairs):
    """Snapshot and canonicalize integer counts; caller mutations cannot leak in."""
    try:
        items = list(pairs.items())
    except AttributeError as exc:
        raise ValueError('output must map words to nonnegative integer counts') from exc
    for key, value in items:
        if not isinstance(key, str) or not key or any(ch.isspace() for ch in key):
            raise ValueError('keys must be nonempty whitespace-free strings')
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError('counts must be nonnegative integers')
    return tuple(sorted(items))


class Publication:
    """First completion per task wins; replay of the same attempt must be equal.

    Tasks are logical shard identities. Attempts identify executions. Map
    functions must be deterministic for winner independence. Calling publish
    cannot undo external effects already performed by the attempted function.
    """

    def __init__(self, tasks):
        tasks = tuple(tasks)
        if (not tasks or any(not isinstance(t, str) or not t for t in tasks)
                or len(set(tasks)) != len(tasks)):
            raise ValueError('tasks must be unique nonempty strings')
        self._tasks = frozenset(tasks)
        self._attempts = {}
        self._accepted = {}

    def publish(self, task, attempt, counts):
        if task not in self._tasks:
            raise ValueError('unknown logical task')
        if not isinstance(attempt, str) or not attempt:
            raise ValueError('attempt must be a nonempty string')
        output = _output(counts)
        identity = (task, output)
        if attempt in self._attempts:
            if self._attempts[attempt] != identity:
                raise ValueError('an attempt ID cannot change task or output')
            return False
        self._attempts[attempt] = identity
        if task in self._accepted:
            return False
        self._accepted[task] = output
        return True

    def reduce(self):
        """One contribution per logical task, only once all tasks are published."""
        if set(self._accepted) != self._tasks:
            raise RuntimeError('some logical tasks have no published output')
        totals = Counter()
        for output in self._accepted.values():
            totals.update(dict(output))
        return dict(sorted(totals.items()))

    @property
    def accepted(self):
        """Owned snapshot for observation, not a handle to internal task state."""
        return {task: dict(output) for task, output in self._accepted.items()}
