from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'code'))
from stats_lab import (bootstrap_mean_ci, bootstrap_means,
                       exact_bernoulli_percentile_coverage, exact_bootstrap_means)


if __name__ == '__main__':
    exact = Counter(exact_bootstrap_means([0, 1]))
    approximate = Counter(bootstrap_means([0, 1], reps=10000, seed=7))
    print(json.dumps({'executed_utc': datetime.now(timezone.utc).isoformat(),
                      'python': platform.python_version(), 'platform': platform.platform(),
                      'conditional_sample': [0, 1],
                      'exact_ordered_resample_counts': sorted(exact.items()),
                      'monte_carlo': {'reps': 10000, 'seed': 7, 'counts': sorted(approximate.items())},
                      'zero_sample_ci': bootstrap_mean_ci([0]*5, 1000, seed=2),
                      'ideal_percentile_coverage': [exact_bernoulli_percentile_coverage(n, p)
                                                    for n, p in [(5, .1), (20, .1), (100, .1), (20, .5)]],
                      'scope': 'finite-distribution exact computations plus conditional Monte Carlo; no physical sample or paper benchmark'}, indent=2))
