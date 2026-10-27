from pathlib import Path
import subprocess,sys
base=Path(__file__).resolve().parent
commands=[[sys.executable,'-m','unittest','discover','-s',str(base/'code'),'-v']]
commands += [[sys.executable,'-m','unittest','discover','-s',str(p/'tests'),'-v'] for p in sorted((base/'problems').iterdir()) if p.is_dir()]
failed=[]
for command in commands:
 p=subprocess.run(command,text=True,capture_output=True)
 print('COMMAND',command);print(p.stdout+p.stderr,end='')
 if p.returncode or 'Ran 0 tests' in p.stdout+p.stderr:failed.append(command)
print(f'DP RELEASE: {len(commands)-len(failed)}/{len(commands)} suites passed')
raise SystemExit(bool(failed))
