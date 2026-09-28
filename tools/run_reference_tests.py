from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
tests=[
 ('completion',[sys.executable,'tools/validate_completion.py'],ROOT),
 ('crypto',[sys.executable,'test_crypto_lab.py'],ROOT/'security-cryptography-mastery/code'),
 ('bio',[sys.executable,'test_sequence_lab.py'],ROOT/'18-computational-biology/code'),
 ('quantum',[sys.executable,'test_simulator.py'],ROOT/'20-quantum-computing/code'),
 ('electronics',[sys.executable,'test_rc_lab.py'],ROOT/'hardware-electronics-mastery/code'),
 ('networking',[sys.executable,'test_framing.py'],ROOT/'06-networking/code'),
 ('sqlite-index',[sys.executable,'test_lab.py'],ROOT/'production-systems-engineering/labs/sqlite-index'),
 ('ml-linear',[sys.executable,'test_linear_model.py'],ROOT/'16-machine-learning/code'),
 ('distributed',[sys.executable,'test_replication_sim.py'],ROOT/'15-distributed-systems/code'),
 ('robotics',[sys.executable,'test_pid_sim.py'],ROOT/'17-embedded-robotics/code'),
 ('data-science',[sys.executable,'test_stats_lab.py'],ROOT/'10-data-science/code'),
 ('arrays',[sys.executable,'algorithmic-problem-solving/topics/arrays/run_all_tests.py'],ROOT),
]
fail=[]
for name,cmd,cwd in tests:
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
 print(f'[{name}] exit={p.returncode}')
 if p.stdout: print(p.stdout.strip())
 if p.stderr: print(p.stderr.strip())
 if p.returncode: fail.append(name)
print(f'REFERENCE TEST GROUPS: {len(tests)-len(fail)}/{len(tests)} passed')
raise SystemExit(bool(fail))
