#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent/'problems'
failed=[]
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    tests=d/'tests'
    print(f"\n== {d.name} ==")
    r=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(tests),'-v'])
    if r.returncode: failed.append(d.name)
print(f"\n{20-len(failed)}/20 problem test suites passed")
if failed: print('failed:',', '.join(failed))
raise SystemExit(bool(failed))
