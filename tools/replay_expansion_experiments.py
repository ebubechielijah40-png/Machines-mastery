#!/usr/bin/env python3
"""Replay trusted bounded expansion experiments; retain new raw observations."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
EXPERIMENTS={
    'elastic':'foundations/chemistry-materials/elastic-evidence/experiment.py',
    'device-logic':'hardware-electronics-mastery/device-logic/experiment.py',
    'page-shape':'07-databases-data-systems/page-index/experiment.py',
    'wal-rebuild':'07-databases-data-systems/page-index/experiment_rebuild.py',
    'model-families':'16-machine-learning/model-families/experiment.py',
    'ordered-structures':'algorithmic-problem-solving/mechanisms/ordered-state/experiment.py',
    'dynamic-programming':'algorithmic-problem-solving/topics/dynamic-programming/experiment.py',
    'lexical-binding':'books/crafting-interpreters/generated/chapters/11/code/experiment.py',
    'operations':'production-systems-engineering/labs/operation-workbench/experiment.py',
    'binary-records':'reverse-engineering-systems/exercises/02-binary-records/experiment.py',
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir',type=Path,required=True)
    args=parser.parse_args();destination=(ROOT/args.report_dir).resolve()
    if not destination.is_relative_to(ROOT):parser.error('report directory must stay inside repository')
    destination.mkdir(parents=True,exist_ok=True);results=[]
    for name,path in EXPERIMENTS.items():
        command=[sys.executable,path];started=datetime.now(timezone.utc).isoformat()
        p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120)
        (destination/(name+'.stdout.txt')).write_text(p.stdout)
        (destination/(name+'.stderr.txt')).write_text(p.stderr)
        try:observed=json.loads(p.stdout)
        except ValueError:observed=None
        good=p.returncode==0 and isinstance(observed,(dict,list))
        if good:(destination/(name+'.json')).write_text(json.dumps(observed,indent=2)+'\n')
        record=dict(name=name,command=command,started_at_utc=started,exit_code=p.returncode,status='PASS' if good else 'FAIL')
        results.append(record);print(json.dumps(record),flush=True)
    (destination/'results.json').write_text(json.dumps({'results':results,'limits':'Actual local synthetic observations; PASS means executable JSON contract, not agreement with every scientific claim or a historical benchmark.'},indent=2)+'\n')
    return int(any(x['status']=='FAIL' for x in results))


if __name__=='__main__':raise SystemExit(main())
