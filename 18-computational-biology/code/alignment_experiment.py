"""Bounded synthetic model-sensitivity, exact-null and scaling experiments.

From repository root:
  python3 18-computational-biology/code/alignment_experiment.py > results.json
No external data, network, packages or biological claims.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import platform
from pathlib import Path
import statistics
import sys
import time
import tracemalloc

from alignment import align_global, align_local


def run():
    here = Path(__file__).resolve().parent
    result = {'schema': 1,
              'environment': {'python': sys.version, 'platform': platform.platform()},
              'source_sha256': {name: hashlib.sha256((here / name).read_bytes()).hexdigest()
                                for name in ('alignment.py', 'alignment_experiment.py')},
              'scope': 'Agent-executed synthetic mechanism experiments; not a paper replication.'}
    a, b = 'ACGT', 'AGCT'
    sensitivity = []
    for gap in [-1, -2, -4]:
        r = align_global(a, b, match=2, mismatch=-3, gap=gap)
        sensitivity.append({'a': a, 'b': b, 'match': 2, 'mismatch': -3, 'gap': gap,
                            'score': r.score, 'a_aligned': r.a_aligned, 'b_aligned': r.b_aligned})
    result['gap_sensitivity'] = sensitivity
    a, b = 'TTACGTAA', 'GGACGTCC'
    result['objective_comparison'] = {}
    for mode, fn in [('global', align_global), ('local', align_local)]:
        r = fn(a, b, 2, -3, -2)
        result['objective_comparison'][mode] = {'score': r.score, 'a_aligned': r.a_aligned,
                                               'b_aligned': r.b_aligned,
                                               'a_span': r.a_span, 'b_span': r.b_span}
    # All equally weighted distinct permutations preserve symbol composition.
    # This conditional toy null is not an evolutionary or sequencing-error model.
    fixed = 'AACCGG'
    null_scores = [align_global(fixed, ''.join(p), 2, -3, -2).score
                   for p in sorted(set(itertools.permutations(fixed)))]
    observed = align_global(fixed, fixed, 2, -3, -2).score
    result['exact_toy_null'] = {'fixed': fixed, 'observed_score': observed,
                                'permutations': len(null_scores),
                                'at_least_observed': sum(s >= observed for s in null_scores),
                                'tail_fraction': sum(s >= observed for s in null_scores) / len(null_scores),
                                'score_histogram': {str(s): null_scores.count(s) for s in sorted(set(null_scores))}}
    result['scaling'] = []
    for n in [32, 64, 128, 256]:
        a, b = ('ACGT' * n)[:n], ('AGCT' * n)[:n]
        align_global(a, b)  # warmup; not timed
        samples = []
        for _ in range(5):
            start = time.perf_counter()
            r = align_global(a, b)
            samples.append(time.perf_counter() - start)
        tracemalloc.start()
        align_global(a, b)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        result['scaling'].append({'n': n, 'table_cells': (n + 1)**2,
                                  'interior_cells_evaluated': r.cells_evaluated,
                                  'elapsed_seconds': samples,
                                  'median_seconds': statistics.median(samples),
                                  'separate_tracemalloc_peak_bytes': peak})
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
