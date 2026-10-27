"""Original bounded retrieval + typed-tool controller. No LLM or network calls.

A deterministic policy makes the control contract testable independently of
model quality. Retrieved text is data, never code or an authority to call tools.
"""
from __future__ import annotations
import ast
from collections import Counter
from dataclasses import dataclass
import math
import re


def words(text):
    if not isinstance(text,str):raise ValueError('text must be str')
    return re.findall(r'\w+',text.lower())


@dataclass(frozen=True)
class Hit:
    id: str
    score: float
    text: str


class LexicalIndex:
    def __init__(self,documents):
        if not 1<=len(documents)<=1000:raise ValueError('corpus must contain1..1000 documents')
        self.text={}
        for row in documents:
            if set(row)!={'id','text'} or not isinstance(row['id'],str) or not row['id'] or row['id'] in self.text:
                raise ValueError('unique nonempty document IDs and exact schema required')
            if not isinstance(row['text'],str) or len(row['text'])>20000:raise ValueError('bounded document text required')
            self.text[row['id']]=row['text']
        self.counts={id:Counter(words(text)) for id,text in self.text.items()}
        df=Counter(token for count in self.counts.values() for token in count)
        self.idf={token:math.log((len(self.text)+1)/(frequency+1))+1 for token,frequency in df.items()}
        self.vectors={id:{token:(1+math.log(count))*self.idf[token] for token,count in counts.items()} for id,counts in self.counts.items()}
        self.norms={id:math.sqrt(sum(x*x for x in vec.values())) for id,vec in self.vectors.items()}

    def search(self,query,k=3):
        if not isinstance(query,str) or len(query)>4096 or type(k) is not int or not 1<=k<=1000:
            raise ValueError('bounded query and positive integer k required')
        count=Counter(words(query));vector={t:(1+math.log(c))*self.idf[t] for t,c in count.items() if t in self.idf}
        norm=math.sqrt(sum(x*x for x in vector.values()))
        if norm==0:return []
        hits=[]
        for id,doc in self.vectors.items():
            denominator=norm*self.norms[id]
            score=sum(weight*doc.get(t,0) for t,weight in vector.items())/denominator if denominator else 0
            if score>0:hits.append(Hit(id,score,self.text[id]))
        return sorted(hits,key=lambda h:(-h.score,h.id))[:k]


def calculate(expression):
    """Small arithmetic grammar, not eval. Inputs/resource/output are bounded."""
    if not isinstance(expression,str) or not 1<=len(expression)<=256:raise ValueError('bounded expression required')
    try:node=ast.parse(expression,mode='eval')
    except SyntaxError as exc:raise ValueError('invalid expression') from exc
    if sum(1 for _ in ast.walk(node))>64:raise ValueError('expression node budget exceeded')
    def visit(n):
        if isinstance(n,ast.Expression):return visit(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):
            value=float(n.value)
            if not math.isfinite(value) or abs(value)>1e6:raise ValueError('literal outside bound')
        elif isinstance(n,ast.UnaryOp) and type(n.op) in (ast.UAdd,ast.USub):
            value=visit(n.operand)*(1 if isinstance(n.op,ast.UAdd) else -1)
        elif isinstance(n,ast.BinOp) and type(n.op) in (ast.Add,ast.Sub,ast.Mult,ast.Div):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add):value=a+b
            elif isinstance(n.op,ast.Sub):value=a-b
            elif isinstance(n.op,ast.Mult):value=a*b
            elif b!=0:value=a/b
            else:raise ValueError('division by zero')
        else:raise ValueError('unsupported arithmetic syntax')
        if not math.isfinite(value) or abs(value)>1e12:raise ValueError('result outside bound')
        return value
    return visit(node)


class LocalAgent:
    """Typed read-only tools, bounded loop, per-session demonstration memory.

    Sessions are caller-assigned labels, not authenticated identities. A caller
    must provide its own auth/isolation before exposing this as a service.
    """
    def __init__(self,index):
        self.index=index;self.memory={}

    def execute(self,action):
        if not isinstance(action,dict) or set(action)!={'tool','args'} or not isinstance(action['args'],dict):
            raise ValueError('tool action requires exact tool/args schema')
        tool,args=action['tool'],action['args']
        if tool=='search' and set(args)=={'query'}:
            return [{'id':h.id,'score':h.score,'text':h.text} for h in self.index.search(args['query'])]
        if tool=='calculator' and set(args)=={'expression'}:
            return calculate(args['expression'])
        raise ValueError('tool or argument schema not permitted')

    def run(self,task,session='local',max_steps=3,proposed_actions=None):
        if not isinstance(task,str) or len(task)>4096 or not isinstance(session,str) or not session or type(max_steps) is not int or not 1<=max_steps<=10:
            raise ValueError('bounded task/session/step count required')
        if proposed_actions is None:
            # A transparent deterministic policy. Replacing this with a learned
            # model changes policy quality, not the executor's authorization.
            action={'tool':'calculator','args':{'expression':task[5:]}} if task.startswith('calc ') else {'tool':'search','args':{'query':task}}
            proposed_actions=[action,{'finish':True}]
        if not isinstance(proposed_actions,list):raise ValueError('actions must be a list')
        trace=[];last=None;result={'status':'budget_exhausted','answer':None,'citations':[]}
        for action in proposed_actions[:max_steps]:
            if isinstance(action,dict) and set(action)=={'finish'} and type(action['finish']) is bool and action['finish']:
                if last is None:
                    result=dict(status='abstain',answer=None,citations=[])
                elif isinstance(last,list):
                    result=(dict(status='answered',answer=last[0]['text'],citations=[last[0]['id']]) if last else dict(status='abstain',answer=None,citations=[]))
                else:result=dict(status='answered',answer=last,citations=[])
                trace.append({'event':'finish','status':result['status']});break
            try:last=self.execute(action)
            except ValueError as exc:
                trace.append({'event':'rejected','action':action,'error':str(exc)})
                result=dict(status='rejected',answer=None,citations=[]);break
            trace.append({'event':'tool_result','action':action,'observation':last})
        result['trace']=trace
        history=self.memory.setdefault(session,[])
        history.append({'task':task,'status':result['status']});del history[:-10]
        return result
