"""Run the independent oracle suite and the twenty released worked contracts."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
commands=[[sys.executable,'-m','unittest','discover','-s',str(root/'code'),'-v']]
commands += [[sys.executable,str(p)] for p in sorted(root.glob('problems/*/tests/test_solution.py'))]
fail=[]
for command in commands:
    result=subprocess.run(command)
    if result.returncode:fail.append(command)
print(f'graph validation groups: {len(commands)-len(fail)}/{len(commands)} passed; one shared independent oracle suite plus twenty worked contracts')
raise SystemExit(bool(fail))
