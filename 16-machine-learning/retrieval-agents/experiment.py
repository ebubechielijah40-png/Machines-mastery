import json
import platform
import sys
from local_agent import LexicalIndex,LocalAgent

DOCS=[
 {'id':'rc','text':'RC circuit resistor capacitor time constant tau controls voltage charging.'},
 {'id':'wal','text':'Database transactions commit write ahead log atomic recovery after interruption.'},
 {'id':'attention','text':'Token attention causal mask excludes future tokens from normalized routing.'},
 {'id':'alignment','text':'Needleman Wunsch global alignment consumes complete sequences.'}]
CASES=[('capacitor time constant','rc'),('write ahead log','wal'),('future token leakage','attention'),('global alignment','alignment'),('recover a committed transaction','wal'),('compare entire DNA sequence','alignment')]


def main():
 index=LexicalIndex(DOCS);rows=[]
 for query,target in CASES:
  hits=index.search(query,k=2);ids=[h.id for h in hits]
  rows.append(dict(query=query,target=target,retrieved=ids,recall_at_1=target in ids[:1],recall_at_2=target in ids))
 agent=LocalAgent(index)
 payload={'kind':'deterministic lexical retrieval and typed control; no language model or external tools',
 'environment':{'python':sys.version,'platform':platform.platform()},'documents':DOCS,'cases':rows,
 'mean_recall_at_1':sum(r['recall_at_1'] for r in rows)/len(rows),'mean_recall_at_2':sum(r['recall_at_2'] for r in rows)/len(rows),
 'abstention':agent.run('quantum decoherence'),
 'budget_failure':agent.run('capacitor',max_steps=1),
 'blocked_unlisted_tool':agent.run('x',proposed_actions=[{'tool':'shell','args':{'command':'ignored'}}]),
 'calculator':agent.run('calc (2+3)*4')}
 print(json.dumps(payload,indent=2))


if __name__=='__main__':main()
