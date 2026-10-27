"""Pinned optional dependency gate: unavailable is BLOCKED, never fake PASS."""
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys

try:version=importlib.metadata.version('cryptography')
except importlib.metadata.PackageNotFoundError:version=None
if version!='50.0.2':
    print(json.dumps(dict(status='BLOCKED',reason='requires cryptography==50.0.2; actual='+str(version))))
    raise SystemExit(2)
root=Path(__file__).resolve().parent
result=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(root),'-p','test_protected_ledger.py','-v'],capture_output=True,text=True)
print(result.stdout,end='');print(result.stderr,end='',file=sys.stderr)
raise SystemExit(result.returncode)
