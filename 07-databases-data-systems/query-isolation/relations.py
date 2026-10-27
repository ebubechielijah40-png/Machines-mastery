"""Original bag operators for one declared, narrow relational value domain.

Tuples contain None, finite numbers or strings. Equality uses Python's equality
on those values without SQLite affinities/collations. No SQL parser is supplied.
"""
from collections import defaultdict
from dataclasses import dataclass
import math


def _rows(rows):
    rows = list(rows)
    if len(rows) > 5000:
        raise ValueError('teaching input limit is 5000 rows')
    if rows and not isinstance(rows[0], tuple):
        raise ValueError('rows must be equal-width tuples')
    width = len(rows[0]) if rows else None
    for row in rows:
        if not isinstance(row, tuple) or len(row) != width:
            raise ValueError('rows must be equal-width tuples')
        for value in row:
            if value is None or isinstance(value, str):
                continue
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError('only finite numbers, strings and None are supported')
    return rows


def _column(rows, index):
    if type(index) is not int or index < 0 or rows and index >= len(rows[0]):
        raise ValueError('invalid column index')


def _truth(value):
    if value is not None and type(value) is not bool:
        raise ValueError('predicate must return True, False or None')
    return value


def sql_equal(a, b):
    return None if a is None or b is None else a == b


def sql_not(a):
    _truth(a)
    return None if a is None else not a


def sql_and(a, b):
    _truth(a)
    _truth(b)
    if a is False or b is False:
        return False
    return None if a is None or b is None else True


def sql_or(a, b):
    _truth(a)
    _truth(b)
    if a is True or b is True:
        return True
    return None if a is None or b is None else False


def select(rows, predicate):
    return [row for row in _rows(rows) if _truth(predicate(row)) is True]


def project(rows, columns):
    rows = _rows(rows)
    columns = tuple(columns)
    if not columns:
        raise ValueError('this interface requires at least one projected column')
    for index in columns:
        _column(rows, index)
    return [tuple(row[i] for i in columns) for row in rows]


def distinct(rows):
    # None is one equivalence bucket for DISTINCT, unlike SQL = in predicates.
    return list(dict.fromkeys(_rows(rows)))


@dataclass
class JoinResult:
    rows: list
    comparisons: int = 0
    build_rows: int = 0
    probes: int = 0


def nested_join(left, right, left_key=0, right_key=0):
    left, right = _rows(left), _rows(right)
    _column(left, left_key)
    _column(right, right_key)
    result = JoinResult([])
    for a in left:
        for b in right:
            result.comparisons += 1
            if sql_equal(a[left_key], b[right_key]) is True:
                result.rows.append(a + b)
    return result


def hash_join(left, right, left_key=0, right_key=0):
    left, right = _rows(left), _rows(right)
    _column(left, left_key)
    _column(right, right_key)
    buckets = defaultdict(list)
    result = JoinResult([])
    for row in right:
        result.build_rows += 1
        if row[right_key] is not None:
            buckets[row[right_key]].append(row)
    for a in left:
        result.probes += 1
        if a[left_key] is not None:
            for b in buckets.get(a[left_key], ()):
                # A bucket contains all duplicates; selecting only one loses rows.
                result.comparisons += 1
                result.rows.append(a + b)
    return result


def grouped_numeric(rows, key=0, value=1):
    """Return key, count(*), count(value), sum(value), avg(value) per group."""
    rows = _rows(rows)
    _column(rows, key)
    _column(rows, value)
    groups = {}
    for row in rows:
        count_all, values = groups.setdefault(row[key], [0, []])
        groups[row[key]][0] = count_all + 1
        x = row[value]
        if x is not None:
            if type(x) not in (int, float):
                raise ValueError('aggregate input must be numeric or None')
            values.append(x)
    result = []
    for group, (count_all, values) in groups.items():
        total = sum(values) if values else None
        average = total / len(values) if values else None
        result.append((group, count_all, len(values), total, average))
    return result
