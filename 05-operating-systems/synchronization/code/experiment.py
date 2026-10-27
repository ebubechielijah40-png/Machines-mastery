"""Finite model enumeration plus separately labeled actual C11 observations."""
from collections import Counter
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from interleavings import enumerate_runs
from conditions import enumerate_conditions

BASE = Path(__file__).resolve().parent


def observe():
    models = []
    for mode in ('split', 'whole_lock', 'store_lock', 'fetch_add'):
        runs = enumerate_runs(mode)
        models.append(dict(kind='exhaustive specified finite model', mode=mode,
                           completed_paths=len(runs),
                           final_value_counts=dict(Counter(run['final'] for run in runs)),
                           lost_update_example=next((run for run in runs if run['final'] == 1), None)))
    condition_models = []
    for protocol, budget in [('while', 0), ('while', 1), ('if', 1), ('split_wait', 0)]:
        runs = enumerate_conditions(protocol, budget)
        condition_models.append(dict(kind='finite predicate/wakeup model', protocol=protocol,
                                     spurious_budget=budget, completed_paths=len(runs),
                                     outcomes=dict(Counter(run['outcome'] for run in runs)),
                                     failure_example=next((run for run in runs if run['outcome'] != 'complete'), None)))
    compiler = shutil.which('cc')
    if not compiler:
        raise RuntimeError('BLOCKED: C compiler and C11 threads required')
    records = []
    with tempfile.TemporaryDirectory(prefix='mm-synchronization-') as directory:
        commands = [[compiler, '--version']]
        for index, flags in enumerate((['-O0'], ['-O2'],
                                       ['-O1', '-fsanitize=undefined', '-fno-sanitize-recover=all'])):
            executable = str(Path(directory) / f'threads-{index}')
            for source, prefix in [('threads.c', 'threads'), ('condition.c', 'condition')]:
                executable = str(Path(directory) / f'{prefix}-{index}')
                commands.extend([[compiler, '-std=c11', '-Wall', '-Wextra', '-Werror',
                                  '-pthread', *flags, str(BASE / source), '-o', executable],
                                 [executable]])
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            record = dict(command=command, exit_code=result.returncode,
                          stdout=result.stdout, stderr=result.stderr)
            records.append(record)
            if result.returncode:
                raise RuntimeError(record)
    return dict(environment=dict(python=sys.version, platform=platform.platform()),
                models=models, condition_models=condition_models, actual_c_commands=records)


if __name__ == '__main__':
    print(json.dumps(observe(), indent=2))
