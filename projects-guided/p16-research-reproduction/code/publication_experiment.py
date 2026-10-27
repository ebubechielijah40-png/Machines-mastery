"""Emit observed duplicate-attempt behavior on original synthetic records."""
from collections import Counter
import json
import platform
import sys

from task_publication import Publication, word_counts


def run():
    shards = {'s0': ['red red'], 's1': ['blue']}
    attempts = [('s0', 'first'), ('s1', 'second'), ('s0', 'backup')]
    naive = Counter()
    job = Publication(shards)
    trace = []
    external_effects = []
    for task, attempt in attempts:
        output = word_counts(shards[task])
        # This stands for an effect outside the output publication boundary.
        external_effects.append(f'notify:{task}')
        naive.update(output)
        trace.append({'task': task, 'attempt': attempt,
                      'accepted': job.publish(task, attempt, output)})
    return {
        'experiment': 'deterministic task publication, original synthetic records',
        'python': sys.version,
        'platform': platform.platform(),
        'shards': shards,
        'trace': trace,
        'sequential_oracle': word_counts([record for values in shards.values() for record in values]),
        'naive_reduce_every_attempt': dict(naive),
        'reduce_one_published_output_per_task': job.reduce(),
        'effects_outside_publication_boundary': external_effects,
        'limits': 'No processes, network, filesystem, atomic rename, GFS, timing or historical benchmark. Publication does not deduplicate external effects.'
    }


if __name__ == '__main__':
    json.dump(run(), sys.stdout, indent=2, sort_keys=True)
    print()
