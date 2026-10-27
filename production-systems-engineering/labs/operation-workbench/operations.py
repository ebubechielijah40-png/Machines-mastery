"""Controlled local operations, not a public network service or durability proof."""
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, asdict
from fractions import Fraction
import math
from pathlib import Path
import re
import sqlite3
import threading
import time


class Conflict(ValueError):
    """A retained request identity was reused for a different operation."""


class UnknownOutcome(RuntimeError):
    """The lab deliberately discards a reply after commit."""


def validate_request(request_id, delta):
    if type(request_id) is not str or re.fullmatch(r'[A-Za-z0-9_.:-]{1,64}', request_id) is None:
        raise ValueError('request identity must be 1..64 restricted ASCII characters')
    if type(delta) is not int or not -1000 <= delta <= 1000:
        raise ValueError('integer delta in [-1000,1000] required')


class OperationStore:
    def __init__(self, path):
        self.path = str(Path(path))
        db = self.connect()
        try:
            mode = db.execute('PRAGMA journal_mode=WAL').fetchone()[0]
            if mode.lower() != 'wal':
                raise RuntimeError('file-backed WAL mode required')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS counter(id INTEGER PRIMARY KEY CHECK(id=1), value INTEGER NOT NULL);
                INSERT OR IGNORE INTO counter VALUES(1,0);
                CREATE TABLE IF NOT EXISTS operations(request_id TEXT PRIMARY KEY, delta INTEGER NOT NULL, result INTEGER NOT NULL);
            ''')
        finally:
            db.close()

    def connect(self):
        db = sqlite3.connect(self.path, timeout=0.05, isolation_level=None)
        db.execute('PRAGMA synchronous=FULL')
        return db

    def apply(self, request_id, delta, fault='none', hook=None):
        validate_request(request_id, delta)
        if type(fault) is not str or fault not in {'none', 'before_commit', 'after_commit'}:
            raise ValueError('unknown controlled fault')
        db = self.connect()
        try:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT delta,result FROM operations WHERE request_id=?', (request_id,)).fetchone()
            if old is not None:
                if old[0] != delta:
                    raise Conflict('retained identity conflicts with delta')
                result, duplicate = old[1], True
            else:
                value = db.execute('SELECT value FROM counter WHERE id=1').fetchone()[0]
                result, duplicate = value + delta, False
                if not -10**12 <= result <= 10**12:
                    raise ValueError('counter bound exceeded')
                db.execute('UPDATE counter SET value=? WHERE id=1', (result,))
                db.execute('INSERT INTO operations VALUES(?,?,?)', (request_id, delta, result))
            if hook:
                hook('before_commit')
            if fault == 'before_commit':
                raise RuntimeError('injected rollback before commit')
            db.commit()
            if hook:
                hook('after_commit')
            if fault == 'after_commit':
                raise UnknownOutcome('commit happened; reply deliberately lost')
            return result, duplicate
        except BaseException:
            if db.in_transaction:
                db.rollback()
            raise
        finally:
            db.close()

    def snapshot(self):
        db = self.connect()
        try:
            db.execute('BEGIN')
            value = db.execute('SELECT value FROM counter WHERE id=1').fetchone()[0]
            rows = db.execute('SELECT request_id,delta,result FROM operations ORDER BY request_id').fetchall()
            db.commit()
            return {'counter': value, 'operations': rows}
        finally:
            db.close()


@dataclass(frozen=True)
class Observation:
    request_id: str
    issued_ns: int
    offered_ns: int
    started_ns: int
    ended_ns: int
    status: str
    result: int | None

    @property
    def latency_ns(self):
        return self.ended_ns - self.issued_ns

    @property
    def queue_ns(self):
        return self.started_ns - self.offered_ns


class BoundedService:
    """Finite experiment session: capacity counts running plus waiting work."""
    def __init__(self, store, workers=2, capacity=6, deadline_ms=30, max_observations=4096):
        if type(workers) is not int or not 1 <= workers <= 8:
            raise ValueError('1..8 workers required')
        if type(capacity) is not int or not workers <= capacity <= 64:
            raise ValueError('capacity must be workers..64')
        if type(deadline_ms) is not int or not 1 <= deadline_ms <= 10000:
            raise ValueError('integer deadline in 1..10000 ms required')
        if type(max_observations) is not int or not 1 <= max_observations <= 5000:
            raise ValueError('1..5000 observations per finite session required')
        self.store = store
        self.deadline_ns = deadline_ms * 1_000_000
        self.limit = max_observations
        self.slots = threading.BoundedSemaphore(capacity)
        self.executor = ThreadPoolExecutor(max_workers=workers)
        self.lock = threading.Lock()
        self.records = []
        self.offered = 0
        self.closed = False

    def submit(self, request_id, delta, *, issued_ns=None, delay_ms=0, fault='none'):
        validate_request(request_id, delta)
        if type(delay_ms) is not int or not 0 <= delay_ms <= 1000:
            raise ValueError('controlled delay must be integer 0..1000 ms')
        if type(fault) is not str or fault not in {'none', 'before_commit', 'after_commit'}:
            raise ValueError('unknown controlled fault')
        now = time.perf_counter_ns()
        issued = now if issued_ns is None else issued_ns
        if type(issued) is not int or not 0 <= issued <= now:
            raise ValueError('issued timestamp must be a past monotonic integer')
        with self.lock:
            if self.closed:
                raise RuntimeError('service session closed')
            if self.offered >= self.limit:
                raise ValueError('finite observation session exhausted; start a new explicit window')
            self.offered += 1
            if not self.slots.acquire(blocking=False):
                record = Observation(request_id, issued, now, now, time.perf_counter_ns(), 'overload', None)
                self.records.append(record)
                future = Future()
                future.set_result(record)
                return future
            try:
                return self.executor.submit(self._run, request_id, delta, issued, now, delay_ms, fault)
            except BaseException:
                self.slots.release()
                self.offered -= 1
                raise

    def _run(self, request_id, delta, issued, offered, delay_ms, fault):
        started = time.perf_counter_ns()
        result = None
        try:
            if started - issued >= self.deadline_ns:
                status = 'deadline'
            else:
                time.sleep(delay_ms / 1000)
                if time.perf_counter_ns() - issued >= self.deadline_ns:
                    status = 'deadline'
                else:
                    try:
                        result, duplicate = self.store.apply(request_id, delta, fault=fault)
                        status = 'duplicate' if duplicate else 'ok'
                    except UnknownOutcome:
                        status = 'unknown'
                    except Conflict:
                        status = 'conflict'
                    except sqlite3.OperationalError:
                        status = 'storage_unavailable'
                    except RuntimeError:
                        status = 'injected_failure'
                    except ValueError:
                        status = 'operation_rejected'
                    except Exception:
                        status = 'internal_error'
            record = Observation(request_id, issued, offered, started, time.perf_counter_ns(), status, result)
            with self.lock:
                self.records.append(record)
            return record
        finally:
            self.slots.release()

    def close(self):
        with self.lock:
            self.closed = True
        self.executor.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def nearest_rank(values, quantile):
    values = tuple(values)
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError('nonnegative integer observations required')
    if type(quantile) not in (float, int) or not math.isfinite(quantile) or not 0 < quantile <= 1:
        raise ValueError('quantile in (0,1] required')
    if not values:
        return None
    return sorted(values)[max(0, math.ceil(quantile * len(values)) - 1)]


def evaluate(records, deadline_ns, target=Fraction(95, 100)):
    """All eligible offered operations, including rejected ones, form the denominator."""
    records = tuple(records)
    if type(deadline_ns) is not int or deadline_ns < 1:
        raise ValueError('positive integer deadline required')
    if type(target) is not Fraction or not 0 < target < 1:
        raise ValueError('exact Fraction target in (0,1) required')
    if any(not isinstance(r, Observation) or any(type(v) is not int for v in (r.issued_ns, r.offered_ns, r.started_ns, r.ended_ns)) or not (0 <= r.issued_ns <= r.offered_ns <= r.started_ns <= r.ended_ns) for r in records):
        raise ValueError('ordered observation clocks required')
    n = len(records)
    good = sum(r.status in {'ok', 'duplicate'} and r.latency_ns <= deadline_ns for r in records)
    bad = n - good
    budget = n * (1 - target)
    ratio = Fraction(good, n) if n else None
    burn = Fraction(bad, n) / (1 - target) if n else None
    return {'eligible': n, 'good': good, 'bad': bad,
            'good_ratio': None if ratio is None else float(ratio),
            'permitted_bad_exact': str(budget), 'remaining_bad_exact': str(budget - bad),
            'burn_rate': None if burn is None else float(burn),
            'slo_met': None if ratio is None else ratio >= target,
            'latency_ms': {str(q): None if not n else nearest_rank([r.latency_ns for r in records], q) / 1e6 for q in (.5, .95, .99)},
            'queue_ms': {str(q): None if not n else nearest_rank([r.queue_ns for r in records], q) / 1e6 for q in (.5, .95, .99)},
            'statuses': {s: sum(r.status == s for r in records) for s in sorted({r.status for r in records})}}
