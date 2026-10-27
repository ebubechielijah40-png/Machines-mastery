"""Bounded local native oracle. Do not read reference/ before your saved attempt."""
from pathlib import Path
import shutil
import subprocess

BASE = Path(__file__).resolve().parent


def compile_oracle(destination, flags=('-O2',)):
    compiler = shutil.which('cc')
    if compiler is None:
        raise RuntimeError('BLOCKED: C11 compiler required')
    command = [compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', *flags,
               str(BASE/'reference/oracle.c'), '-o', str(destination)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return command


def query(executable, sequence, sample, enabled, payload):
    if type(sequence) is not int or not 0 <= sequence <= 65535:
        raise ValueError('sequence must be uint16')
    if type(sample) is not int or not -32768 <= sample <= 32767:
        raise ValueError('sample must be int16')
    if type(enabled) is not bool:
        raise ValueError('enabled must be bool')
    if type(payload) is not bytes or len(payload) > 32:
        raise ValueError('payload must be at most 32 bytes')
    result = subprocess.run([str(executable), str(sequence), str(sample), str(int(enabled)), payload.hex()],
                            capture_output=True, text=True, timeout=2)
    if result.returncode:
        raise RuntimeError('oracle rejected wrapper-validated arguments')
    return bytes.fromhex(result.stdout.strip())


if __name__ == '__main__':
    import argparse, tempfile
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sequence', type=int)
    parser.add_argument('sample', type=int)
    parser.add_argument('enabled', type=int, choices=(0,1))
    parser.add_argument('payload_hex', help='hexadecimal bytes, including empty string')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        binary = Path(directory)/'oracle'
        compile_oracle(binary)
        print(query(binary,args.sequence,args.sample,bool(args.enabled),bytes.fromhex(args.payload_hex)).hex())
