from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
required=[
'START_HERE.md','SELF_CONTAINED_STUDY.md','STUDY_ROUTE.md','CAPABILITY_MAP.md','LIMITS_AND_REALITY.md',
'coursebooks/README.md','security-cryptography-mastery/HANDBOOK.md','18-computational-biology/DEEP_HANDBOOK.md',
'20-quantum-computing/HANDBOOK.md','projects-guided/README.md','COMPLETION_REPORT.md']
errors=[]
for r in required:
 p=ROOT/r
 if not p.is_file() or p.stat().st_size<200: errors.append(f'missing/shallow {r}')
for d in ['foundations/mathematics','foundations/physics','foundations/statistics','foundations/chemistry-materials']:
 if not (ROOT/d/'DEEP_GUIDE.md').is_file(): errors.append('missing '+d+'/DEEP_GUIDE.md')
langs=list((ROOT/'programming-languages-mastery').glob('[0-9][0-9]-*'))
for d in langs:
 if not (d/'DEEP_GUIDE.md').is_file(): errors.append('missing '+str(d.relative_to(ROOT))+'/DEEP_GUIDE.md')
# executable reference tests
cmds=[
 [sys.executable,'test_crypto_lab.py'],
 [sys.executable,'test_sequence_lab.py'],
 [sys.executable,'test_simulator.py']]
cwds=[ROOT/'security-cryptography-mastery/code', ROOT/'18-computational-biology/code', ROOT/'20-quantum-computing/code']
for cmd,cwd in zip(cmds,cwds):
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
 if p.returncode: errors.append(f'test failed {cwd}: {p.stdout} {p.stderr}')
 else: print(p.stdout.strip())
print(f'{len(errors)} completion errors')
for e in errors: print('ERROR:',e)
raise SystemExit(bool(errors))
