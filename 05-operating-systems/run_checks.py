"""Execute the connected systems reference suites in separate processes.

Prints an evidence record. No generated report is silently treated as a depth
rating, and expected incomplete-link failures are handled within that lab.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_checks():
    suites = [
        ('compile_link', ['-m', 'unittest', 'discover', '-s',
                          '04-computer-systems/compile-link', '-p', 'test_*.py', '-v']),
        ('os_models', ['-m', 'unittest', 'discover', '-s',
                       '05-operating-systems/code', '-p', 'test_*.py', '-v']),
        ('synchronization', ['-m', 'unittest', 'discover', '-s',
                             '05-operating-systems/synchronization/code',
                             '-p', 'test_*.py', '-v']),
        ('shell', ['-m', 'unittest', 'discover', '-s',
                   'projects-guided/p02-shell/code', '-p', 'test_*.py', '-v']),
        ('arena', ['projects-guided/p04-memory-allocator/code/run.py']),
        ('kernel_workbench', ['-m', 'unittest', 'discover', '-s',
                              'projects-guided/p05-mini-kernel-labs/code',
                              '-p', 'test_*.py', '-v']),
    ]
    records = []
    for name, arguments in suites:
        command = [sys.executable, *arguments]
        result = subprocess.run(command, cwd=ROOT, text=True,
                                capture_output=True, timeout=60)
        records.append(dict(name=name, command=command, cwd=str(ROOT),
                            exit_code=result.returncode, stdout=result.stdout,
                            stderr=result.stderr))
    return dict(kind='actual executed bounded systems checks',
                executed_at_utc=datetime.now(timezone.utc).isoformat(),
                environment=dict(python=sys.version, platform=platform.platform()),
                passed=all(record['exit_code'] == 0 for record in records),
                records=records)


if __name__ == '__main__':
    report = run_checks()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
