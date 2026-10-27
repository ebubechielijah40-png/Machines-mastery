"""Compile and observe the fixed C arena; preserve exact commands and outputs."""
import json
import pathlib
import platform
import shutil
import subprocess
import tempfile

BASE = pathlib.Path(__file__).resolve().parent


def observe():
    compiler = shutil.which('cc')
    if not compiler:
        raise RuntimeError('BLOCKED: a C11 compiler is required')
    records = []
    with tempfile.TemporaryDirectory(prefix='mm-arena-observation-') as directory:
        executable = str(pathlib.Path(directory) / 'arena-experiment')
        commands = [
            [compiler, '--version'],
            [compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-O2',
             str(BASE / 'arena.c'), str(BASE / 'experiment.c'), '-o', executable],
            [executable],
        ]
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            records.append(dict(command=command, exit_code=result.returncode,
                                stdout=result.stdout, stderr=result.stderr))
            if result.returncode:
                raise RuntimeError(records[-1])
    return dict(kind='actual C interval-state observations',
                platform=platform.platform(), records=records,
                observation=json.loads(records[-1]['stdout']))


if __name__ == '__main__':
    print(json.dumps(observe(), indent=2))
