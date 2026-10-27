"""Actual local child-process observations; no fabricated benchmark timings."""
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time

from minishell import Shell, run_pipeline


def observe():
    records = []
    cases = [
        ('large_pipeline', [[sys.executable, '-c',
          'import sys; sys.stdout.buffer.write(b"x"*200000)'],
          [sys.executable, '-c',
           'import sys; print(len(sys.stdin.buffer.read()))']]),
        ('literal_argument_and_exit', [[sys.executable, '-c',
          'import sys; print(sys.argv[1]); sys.exit(7)', '; $(unexecuted) *']]),
    ]
    for name, commands in cases:
        started = time.monotonic()
        result = run_pipeline(commands)
        records.append(dict(name=name, kind='actual local subprocesses',
                            argv=commands, input_bytes=0,
                            stdout=result.stdout.decode(),
                            stderr=[data.decode() for data in result.stderr],
                            returncodes=result.returncodes,
                            elapsed_seconds=time.monotonic() - started))
    before = os.getcwd()
    with tempfile.TemporaryDirectory(prefix='mm-shell-cwd-') as directory:
        child = Path(directory) / 'child'
        child.mkdir()
        shell = Shell(directory)
        shell.execute('cd child')
        command = [[sys.executable, '-c', 'import os; print(os.getcwd())']]
        result = run_pipeline(command, cwd=shell.cwd)
        records.append(dict(name='logical_cd', kind='actual local subprocess',
                            argv=command, shell_cwd=str(shell.cwd),
                            child_stdout=result.stdout.decode(),
                            parent_before=before, parent_after=os.getcwd(),
                            parent_unchanged=before == os.getcwd(),
                            child_matches_shell=result.stdout.decode().strip() == str(shell.cwd)))
    return dict(environment=dict(python=sys.version, platform=platform.platform()),
                records=records)


if __name__ == '__main__':
    print(json.dumps(observe(), indent=2))
