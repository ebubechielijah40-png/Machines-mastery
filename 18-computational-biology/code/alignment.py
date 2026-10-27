"""Exact global/local alignment under an integer, linear-gap scoring model.

Original teaching implementation. Inputs may be arbitrary symbol strings except
'-', reserved for gaps; alphabet/biological validation belongs to the caller.
Python 3.10+, standard library only. See ../02_SEQUENCE_ALGORITHMS.md.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Alignment:
    score: int
    a_aligned: str
    b_aligned: str
    a_span: tuple[int, int]
    b_span: tuple[int, int]
    table: tuple[tuple[int, ...], ...]
    cells_evaluated: int


def _scoring(match: int, mismatch: int, gap: int) -> None:
    if any(type(x) is not int for x in (match, mismatch, gap)):
        raise ValueError('scores must be integers (bools are not scores)')
    if gap > 0:
        raise ValueError('this teaching model requires a nonpositive gap score')


def score_alignment(a: str, b: str, match=1, mismatch=-1, gap=-1) -> int:
    """Rescore displayed columns independently of a dynamic-programming table."""
    _scoring(match, mismatch, gap)
    if len(a) != len(b):
        raise ValueError('aligned strings must have the same length')
    total = 0
    for x, y in zip(a, b):
        if x == y == '-':
            raise ValueError('a gap-gap column consumes no input')
        total += gap if '-' in (x, y) else match if x == y else mismatch
    return total


def _align(a, b, match, mismatch, gap, local, max_cells):
    _scoring(match, mismatch, gap)
    if not isinstance(a, str) or not isinstance(b, str):
        raise ValueError('inputs must be strings')
    if '-' in a or '-' in b:
        raise ValueError("'-' is reserved for displayed gaps")
    if type(max_cells) is not int or max_cells < 1:
        raise ValueError('max_cells must be a positive integer')
    n, m = len(a), len(b)
    if (n + 1) * (m + 1) > max_cells:
        raise ValueError('alignment exceeds the configured table-cell budget')
    f = [[0] * (m + 1) for _ in range(n + 1)]
    trace = [[0] * (m + 1) for _ in range(n + 1)]
    if not local:
        for i in range(1, n + 1):
            f[i][0], trace[i][0] = i * gap, 2
        for j in range(1, m + 1):
            f[0][j], trace[0][j] = j * gap, 3
    best, endpoint = 0, (0, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            choices = (f[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch),
                       f[i - 1][j] + gap, f[i][j - 1] + gap)
            value = max(choices)
            if local and value <= 0:
                continue  # zero means restart, including an exact zero tie
            f[i][j] = value
            trace[i][j] = choices.index(value) + 1  # diag, up, left tie priority
            if local and value > best:
                best, endpoint = value, (i, j)
    if not local:
        endpoint, best = (n, m), f[n][m]
    i, j = endpoint
    aa, bb = [], []
    while trace[i][j]:
        step = trace[i][j]
        if step == 1:
            aa.append(a[i - 1]); bb.append(b[j - 1]); i -= 1; j -= 1
        elif step == 2:
            aa.append(a[i - 1]); bb.append('-'); i -= 1
        else:
            aa.append('-'); bb.append(b[j - 1]); j -= 1
    return Alignment(best, ''.join(reversed(aa)), ''.join(reversed(bb)),
                     (i, endpoint[0]), (j, endpoint[1]),
                     tuple(tuple(row) for row in f), n * m)


def align_global(a: str, b: str, match=1, mismatch=-1, gap=-1, *, max_cells=1_000_000):
    """Align all input symbols. Ties prefer diagonal, then up, then left."""
    return _align(a, b, match, mismatch, gap, False, max_cells)


def align_local(a: str, b: str, match=1, mismatch=-1, gap=-1, *, max_cells=1_000_000):
    """Best contiguous input intervals, permitting internal gaps.

    Empty alignment has score zero. Equal endpoint scores choose first row-major
    endpoint. Spans use zero-based half-open indices into the original inputs.
    """
    return _align(a, b, match, mismatch, gap, True, max_cells)
