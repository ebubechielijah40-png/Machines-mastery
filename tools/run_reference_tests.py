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
 ('ml-autodiff',[sys.executable,'test_autodiff.py'],ROOT/'16-machine-learning/code'),
 ('ml-attention',[sys.executable,'-m','unittest','discover','-s','16-machine-learning/labs','-v'],ROOT),
 ('numerical-foundations',[sys.executable,'-m','unittest','discover','-s','foundations/mathematics/change-error-and-evidence','-v'],ROOT),
 ('storage-recovery',[sys.executable,'-m','unittest','discover','-s','projects-guided/p07-storage-engine/code','-v'],ROOT),
 ('bio-alignment',[sys.executable,'-m','unittest','discover','-s','18-computational-biology/code','-p','test_alignment.py','-v'],ROOT),
 ('bio-workbench',[sys.executable,'-m','unittest','discover','-s','projects-guided/p14-bioinformatics/tests','-v'],ROOT),
 ('math-core',[sys.executable,'-m','unittest','discover','-s','foundations/mathematics/core','-v'],ROOT),
 ('finite-inference',[sys.executable,'-m','unittest','discover','-s','foundations/statistics/probability-inference','-v'],ROOT),
 ('python-entry',[sys.executable,'-m','unittest','discover','-s','02-programming/python-entry','-v'],ROOT),
 ('toy-cpu',[sys.executable,'-m','unittest','discover','-s','01-computation/toy-cpu','-v'],ROOT),
 ('os-models',[sys.executable,'-m','unittest','discover','-s','05-operating-systems/code','-v'],ROOT),
 ('synchronization',[sys.executable,'-m','unittest','discover','-s','05-operating-systems/synchronization/code','-v'],ROOT),
 ('shell-lifecycle',[sys.executable,'-m','unittest','discover','-s','projects-guided/p02-shell/code','-v'],ROOT),
 ('kernel-workbench',[sys.executable,'-m','unittest','discover','-s','projects-guided/p05-mini-kernel-labs/code','-v'],ROOT),
 ('stream-protocol',[sys.executable,'-m','unittest','discover','-s','06-networking/code','-p','test_stream_protocol.py','-v'],ROOT),
 ('http-subset',[sys.executable,'-m','unittest','discover','-s','projects-guided/p06-http-server/code','-v'],ROOT),
 ('relational-isolation',[sys.executable,'-m','unittest','discover','-s','07-databases-data-systems/query-isolation','-v'],ROOT),
 ('finite-information',[sys.executable,'-m','unittest','discover','-s','08-information-science/finite-information','-v'],ROOT),
 ('scientific-measurement',[sys.executable,'-m','unittest','discover','-s','projects-guided/p08-scientific-pipeline/code','-v'],ROOT),
 ('authenticated-provenance',[sys.executable,'-m','unittest','discover','-s','security-cryptography-mastery/provenance','-p','test_pipeline.py','-v'],ROOT),
 ('privacy-count',[sys.executable,'-m','unittest','discover','-s','13-privacy/count-release','-v'],ROOT),
 ('graphs',[sys.executable,'algorithmic-problem-solving/topics/graphs/run_all_tests.py'],ROOT),
 ('expression-language',[sys.executable,'-m','unittest','discover','-s','projects-guided/p10-language/code','-v'],ROOT),
 ('python-aliases',[sys.executable,'-m','unittest','discover','-s','programming-languages-mastery/08-python/units/objects-and-aliases','-v'],ROOT),
 ('bash-arguments',[sys.executable,'-m','unittest','discover','-s','programming-languages-mastery/12-shell-bash/units/argument-boundaries','-v'],ROOT),
 ('sql-null-joins',[sys.executable,'-m','unittest','discover','-s','programming-languages-mastery/11-sql/units/null-and-joins','-v'],ROOT),
 ('replica-reconciliation',[sys.executable,'-m','unittest','discover','-s','15-distributed-systems/ordering-reconciliation','-v'],ROOT),
 ('replica-workbench',[sys.executable,'-m','unittest','discover','-s','projects-guided/p11-distributed-kv/code','-v'],ROOT),
 ('trained-model-tokenizers',[sys.executable,'-m','unittest','discover','-s','16-machine-learning/training','-v'],ROOT),
 ('retrieval-tools',[sys.executable,'-m','unittest','discover','-s','16-machine-learning/retrieval-agents','-v'],ROOT),
 ('motor-control',[sys.executable,'-m','unittest','discover','-s','17-embedded-robotics/control-path','-v'],ROOT),
 ('population-phylogeny',[sys.executable,'-m','unittest','discover','-s','18-computational-biology/population-phylogeny','-v'],ROOT),
 ('quantum-noise',[sys.executable,'-m','unittest','discover','-s','20-quantum-computing/noise-correction','-v'],ROOT),
 ('bio-stack',[sys.executable,'-m','unittest','discover','-s','projects-guided/computational-biology-stack','-v'],ROOT),
 ('quantum-stack',[sys.executable,'-m','unittest','discover','-s','projects-guided/quantum-machine-stack','-v'],ROOT),
 ('research-mechanisms',[sys.executable,'-m','unittest','discover','-s','projects-guided/p16-research-reproduction/code','-v'],ROOT),
]
tests += [
 ('page-index',[sys.executable,'-m','unittest','discover','-s','07-databases-data-systems/page-index','-v'],ROOT),
 ('model-families',[sys.executable,'-m','unittest','discover','-s','16-machine-learning/model-families','-v'],ROOT),
 ('elastic-evidence',[sys.executable,'-m','unittest','discover','-s','foundations/chemistry-materials/elastic-evidence','-v'],ROOT),
 ('device-logic',[sys.executable,'-m','unittest','discover','-s','hardware-electronics-mastery/device-logic','-v'],ROOT),
 ('ordered-structures',[sys.executable,'-m','unittest','discover','-s','algorithmic-problem-solving/mechanisms/ordered-state','-v'],ROOT),
 ('dynamic-programming',[sys.executable,'algorithmic-problem-solving/topics/dynamic-programming/run_all_tests.py'],ROOT),
 ('lexical-binding',[sys.executable,'-m','unittest','discover','-s','books/crafting-interpreters/generated/chapters/11/code','-v'],ROOT),
 ('operation-workbench',[sys.executable,'-m','unittest','discover','-s','production-systems-engineering/labs/operation-workbench','-v'],ROOT),
 ('initial-value-evidence',[sys.executable,'-m','unittest','discover','-s','foundations/mathematics/initial-value-evidence','-v'],ROOT),
 ('compiler-runtime',[sys.executable,'-m','unittest','discover','-s','02-programming/compiler-runtime','-v'],ROOT),
 ('published-index-recovery',[sys.executable,'-m','unittest','discover','-s','07-databases-data-systems/recovery-planning','-v'],ROOT),
 ('hidden-plant',[sys.executable,'-m','unittest','discover','-s','reverse-engineering-systems/exercises/03-hidden-plant','-v'],ROOT),
 ('systems-models',[sys.executable,'-m','unittest','discover','-s','04-computer-systems/abi-loading','-v'],ROOT),
]
fail=[]
for name,cmd,cwd in tests:
 try:
  p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=120)
 except subprocess.TimeoutExpired:
  print(f'[{name}] FAIL: 120 second per-group timeout')
  fail.append(name)
  continue
 print(f'[{name}] exit={p.returncode}')
 if p.stdout: print(p.stdout.strip())
 if p.stderr: print(p.stderr.strip())
 if p.returncode or 'Ran 0 tests' in p.stdout+p.stderr or 'NO TESTS RAN' in p.stdout+p.stderr: fail.append(name)
print(f'REFERENCE TEST GROUPS: {len(tests)-len(fail)}/{len(tests)} passed')
raise SystemExit(bool(fail))
