"""Deterministic schedules and actual query plans, not a crash/durability test."""
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sqlite3
import tempfile
from relations import hash_join, nested_join


def snapshot_schedule():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'bank.sqlite'
        a = sqlite3.connect(path, isolation_level=None, timeout=0)
        b = sqlite3.connect(path, isolation_level=None, timeout=0)
        try:
            mode = a.execute('PRAGMA journal_mode=WAL').fetchone()[0]
            if mode.lower() != 'wal':
                raise RuntimeError('experiment requires local WAL mode')
            a.execute('CREATE TABLE account(id INTEGER PRIMARY KEY, balance INTEGER NOT NULL CHECK(balance>=0))')
            a.executemany('INSERT INTO account VALUES(?,?)', [(1, 100), (2, 100)])
            read = lambda con: list(con.execute('SELECT id,balance FROM account ORDER BY id'))
            a.execute('BEGIN')
            initial = read(a)  # The SELECT establishes this deferred read snapshot.
            b.execute('BEGIN IMMEDIATE')
            b.execute('UPDATE account SET balance=balance-10 WHERE id=1')
            b.execute('UPDATE account SET balance=balance+10 WHERE id=2')
            during = read(a)
            b.execute('COMMIT')
            after_other_commit = read(a)
            upgrade = None
            try:
                a.execute('UPDATE account SET balance=balance-1 WHERE id=1')
            except sqlite3.OperationalError as error:
                upgrade = {'type': type(error).__name__, 'message': str(error),
                           'code': getattr(error, 'sqlite_errorcode', None),
                           'name': getattr(error, 'sqlite_errorname', None)}
            finally:
                a.execute('ROLLBACK')
            fresh = read(a)
            b.execute('BEGIN IMMEDIATE')
            contention = None
            try:
                a.execute('BEGIN IMMEDIATE')
            except sqlite3.OperationalError as error:
                contention = {'code': getattr(error, 'sqlite_errorcode', None),
                              'name': getattr(error, 'sqlite_errorname', None),
                              'message': str(error)}
            finally:
                b.execute('ROLLBACK')
            # All statements below autocommit separately. This is an application
            # stale-read bug, not two overlapping serializable SQL transactions.
            a.execute('UPDATE account SET balance=100 WHERE id=1')
            stale_a = a.execute('SELECT balance FROM account WHERE id=1').fetchone()[0]
            stale_b = b.execute('SELECT balance FROM account WHERE id=1').fetchone()[0]
            a.execute('UPDATE account SET balance=? WHERE id=1', (stale_a - 10,))
            b.execute('UPDATE account SET balance=? WHERE id=1', (stale_b - 20,))
            stale_result = a.execute('SELECT balance FROM account WHERE id=1').fetchone()[0]
            a.execute('UPDATE account SET balance=100 WHERE id=1')
            a.execute('UPDATE account SET balance=balance-? WHERE id=1', (10,))
            b.execute('UPDATE account SET balance=balance-? WHERE id=1', (20,))
            atomic_result = a.execute('SELECT balance FROM account WHERE id=1').fetchone()[0]
            return {'journal_mode': mode, 'initial_snapshot': initial,
                    'during_uncommitted_transfer': during,
                    'same_snapshot_after_other_commit': after_other_commit,
                    'stale_snapshot_upgrade': upgrade, 'new_read_after_rollback': fresh,
                    'second_writer_attempt': contention,
                    'separate_statement_stale_read_result': stale_result,
                    'atomic_relative_update_result': atomic_result,
                    'scope': 'local sequential interleaving of two real connections; no crash, threads or power loss'}
        finally:
            a.close()
            b.close()


def query_plans():
    con = sqlite3.connect(':memory:')
    try:
        con.execute('CREATE TABLE reading(id INTEGER PRIMARY KEY, device INTEGER, value REAL)')
        con.executemany('INSERT INTO reading VALUES(?,?,?)', ((i, i % 100, i / 10) for i in range(1000)))
        sql = 'SELECT id,value FROM reading WHERE device=? ORDER BY id'
        result_before = list(con.execute(sql, (7,)))
        before = list(con.execute('EXPLAIN QUERY PLAN ' + sql, (7,)))
        con.execute('CREATE INDEX reading_device ON reading(device)')
        result_after = list(con.execute(sql, (7,)))
        after = list(con.execute('EXPLAIN QUERY PLAN ' + sql, (7,)))
        return {'rows': 1000, 'predicate': 'device=7', 'matching_rows': len(result_after),
                'equal_ordered_results': result_before == result_after,
                'before': before, 'after': after,
                'note': 'Plan text is version-specific diagnostic output; no elapsed-time speedup asserted.'}
    finally:
        con.close()


def join_counts():
    result = []
    for n in (10, 100, 1000):
        left = [(i, 'L') for i in range(n)]
        right = [(i, 'R') for i in range(n)]
        nested = nested_join(left, right)
        hashed = hash_join(left, right)
        result.append({'n_each_side': n, 'nested_comparisons': nested.comparisons,
                       'hash_build_rows': hashed.build_rows, 'hash_probes': hashed.probes,
                       'hash_candidate_rows': hashed.comparisons,
                       'output_rows': len(hashed.rows),
                       'equal_bags': Counter(nested.rows) == Counter(hashed.rows)})
    return result


if __name__ == '__main__':
    print(json.dumps({'executed_utc': datetime.now(timezone.utc).isoformat(),
                      'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version,
                      'platform': platform.platform(), 'snapshot': snapshot_schedule(),
                      'query_plan': query_plans(), 'join_counts': join_counts()}, indent=2))
