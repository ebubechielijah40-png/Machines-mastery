"""Original scalar-autodiff MLP and one-block causal decoder, standard library.

This intentionally exposes every operation. It is slow, bounded, unoptimized,
and neither a pretrained model nor a reproduction of a published experiment.
Run commands from training/README.md. No external weights/data are downloaded.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from autodiff import Value


def dot(a,b):
    if len(a)!=len(b) or not a:
        raise ValueError('equal nonempty vector widths required')
    return sum((x*y for x,y in zip(a,b)),Value(0))


def linear(vector,weights,bias=None):
    if len(weights)!=len(vector) or not weights or not weights[0] or any(len(r)!=len(weights[0]) for r in weights):
        raise ValueError('weights must have shape (input width, output width)')
    result=[sum((vector[i]*weights[i][j] for i in range(len(vector))),Value(0)) for j in range(len(weights[0]))]
    if bias is not None:
        if len(bias)!=len(result):raise ValueError('bias width mismatch')
        result=[x+b for x,b in zip(result,bias)]
    return result


def normalized_exp(scores):
    if not scores:raise ValueError('empty softmax')
    shift=max(x.data for x in scores)
    weights=[(x-shift).exp() for x in scores]
    total=sum(weights,Value(0))
    return [w/total for w in weights]


def cross_entropy(logits,target):
    if type(target) is not int or not 0<=target<len(logits):
        raise ValueError('target index outside logits')
    shift=max(x.data for x in logits)
    shifted=[x-shift for x in logits]
    return sum((x.exp() for x in shifted),Value(0)).log()-shifted[target]


def normalize(vector,epsilon=1e-5):
    if epsilon<=0:raise ValueError('epsilon must be positive')
    mean=sum(vector,Value(0))/len(vector)
    centered=[x-mean for x in vector]
    variance=sum((x*x for x in centered),Value(0))/len(vector)
    scale=(variance+epsilon)**-.5
    return [x*scale for x in centered]


def sgd(parameters,learning_rate,clip_norm=None):
    parameters=list(parameters)
    if any(not isinstance(p,Value) for p in parameters) or len({id(p) for p in parameters})!=len(parameters):
        raise ValueError('unique scalar Value parameters required')
    if type(learning_rate) not in (int,float) or not math.isfinite(learning_rate) or learning_rate<=0:
        raise ValueError('positive finite learning rate required')
    if any(not math.isfinite(p.grad) for p in parameters):
        raise ValueError('nonfinite gradient; parameters not updated')
    norm=math.sqrt(math.fsum(p.grad*p.grad for p in parameters))
    if not math.isfinite(norm):raise ValueError('gradient norm overflow; parameters not updated')
    if clip_norm is not None and (type(clip_norm) not in (int,float) or not math.isfinite(clip_norm) or clip_norm<=0):
        raise ValueError('clip norm must be positive and finite')
    scale=min(1.0,clip_norm/norm) if clip_norm is not None and norm else 1.0
    proposed=[p.data-learning_rate*scale*p.grad for p in parameters]
    if any(not math.isfinite(x) for x in proposed):
        raise ValueError('nonfinite update; parameters not updated')
    for p,value in zip(parameters,proposed):p.data=value
    return norm


class CharacterTokenizer:
    def __init__(self,training_text):
        if not isinstance(training_text,str) or not training_text:
            raise ValueError('nonempty training text required')
        self.symbols=tuple(sorted(set(training_text)))
        self.ids={c:i for i,c in enumerate(self.symbols)}

    def encode(self,text):
        if not isinstance(text,str):raise ValueError('text must be str')
        try:return [self.ids[c] for c in text]
        except KeyError as error:raise ValueError(f'unknown character {error.args[0]!r}') from error

    def decode(self,ids):
        ids=list(ids)
        if any(type(i) is not int or not 0<=i<len(self.symbols) for i in ids):
            raise ValueError('token ID outside vocabulary')
        return ''.join(self.symbols[i] for i in ids)


class MLP:
    def __init__(self,seed=0,hidden=4):
        if type(hidden) is not int or not 1<=hidden<=32:raise ValueError('hidden width1..32')
        rng=random.Random(seed)
        self.w1=[[Value(rng.gauss(0,.8)) for _ in range(hidden)] for _ in range(2)]
        self.b1=[Value(0) for _ in range(hidden)]
        self.w2=[[Value(rng.gauss(0,.5))] for _ in range(hidden)]
        self.b2=[Value(0)]

    def parameters(self):
        return [p for rows in [self.w1,self.w2] for row in rows for p in row]+self.b1+self.b2

    def __call__(self,x):
        if len(x)!=2:raise ValueError('two inputs required')
        hidden=[v.tanh() for v in linear(x,self.w1,self.b1)]
        return linear(hidden,self.w2,self.b2)[0].tanh()

    def loss(self,data):
        if not data:raise ValueError('nonempty dataset required')
        return sum(((self(x)-y)**2 for x,y in data),Value(0))/len(data)


class TinyDecoder:
    """One pre-normalized multi-head causal block with learned position vectors.

    Token embedding + learned position -> pre-norm attention -> residual ->
    pre-norm tanh feedforward -> residual -> norm -> vocabulary logits.
    No dropout, padding, tied weights, quantization, KV cache, or GPU code.
    """
    def __init__(self,vocab_size,d_model=8,heads=2,context=4,ff_width=12,seed=0):
        if any(type(v) is not int for v in [vocab_size,d_model,heads,context,ff_width]):
            raise ValueError('integer dimensions required')
        if not (2<=vocab_size<=32 and 2<=d_model<=16 and 1<=heads<=d_model and d_model%heads==0 and 1<=context<=16 and 1<=ff_width<=32):
            raise ValueError('bounded dimensions invalid')
        if type(seed) is not int:raise ValueError('integer seed required')
        self.config=dict(vocab_size=vocab_size,d_model=d_model,heads=heads,context=context,ff_width=ff_width,seed=seed)
        self.d=d_model;self.heads=heads;self.context=context;self.vocab_size=vocab_size
        self._rng=random.Random(seed)
        self.embedding=self._matrix(vocab_size,d_model,.2)
        self.position=self._matrix(context,d_model,.1)
        self.wq=self._matrix(d_model,d_model)
        self.wk=self._matrix(d_model,d_model)
        self.wv=self._matrix(d_model,d_model)
        self.wo=self._matrix(d_model,d_model,.15)
        self.w1=self._matrix(d_model,ff_width)
        self.b1=[Value(0) for _ in range(ff_width)]
        self.w2=self._matrix(ff_width,d_model,.15)
        self.b2=[Value(0) for _ in range(d_model)]
        self.output=self._matrix(d_model,vocab_size,.15)

    def _matrix(self,n,m,scale=None):
        if scale is None:scale=1/math.sqrt(n)
        return [[Value(self._rng.gauss(0,scale)) for _ in range(m)] for _ in range(n)]

    def parameters(self):
        matrices=[self.embedding,self.position,self.wq,self.wk,self.wv,self.wo,self.w1,self.w2,self.output]
        return [p for matrix in matrices for row in matrix for p in row]+self.b1+self.b2

    def logits(self,token_ids):
        if not 1<=len(token_ids)<=self.context or any(type(i) is not int or not 0<=i<self.vocab_size for i in token_ids):
            raise ValueError('nonempty bounded context of valid token IDs required')
        x=[[e+p for e,p in zip(self.embedding[token],self.position[t])] for t,token in enumerate(token_ids)]
        n=[normalize(row) for row in x]
        q=[linear(row,self.wq) for row in n];k=[linear(row,self.wk) for row in n];v=[linear(row,self.wv) for row in n]
        width=self.d//self.heads
        output=[]
        for t in range(len(x)):
            joined=[]
            for h in range(self.heads):
                lo=h*width;hi=lo+width
                scores=[dot(q[t][lo:hi],k[j][lo:hi])/math.sqrt(width) for j in range(t+1)]
                weights=normalized_exp(scores)
                joined.extend(sum((weights[j]*v[j][c] for j in range(t+1)),Value(0)) for c in range(lo,hi))
            attn=linear(joined,self.wo)
            residual=[a+b for a,b in zip(x[t],attn)]
            hidden=[a.tanh() for a in linear(normalize(residual),self.w1,self.b1)]
            feed=linear(hidden,self.w2,self.b2)
            final=normalize([a+b for a,b in zip(residual,feed)])
            output.append(linear(final,self.output))
        return output

    def loss(self,sequence):
        if len(sequence)<2:raise ValueError('at least two tokens needed')
        logits=self.logits(sequence[:-1])
        return sum((cross_entropy(row,target) for row,target in zip(logits,sequence[1:])),Value(0))/len(logits)

    def generate(self,prefix,count,temperature=1.0,top_k=None,seed=0):
        if type(count) is not int or not 0<=count<=100 or not math.isfinite(temperature) or temperature<=0:
            raise ValueError('bounded count0..100 and positive temperature required')
        if top_k is not None and (type(top_k) is not int or not 1<=top_k<=self.vocab_size):
            raise ValueError('top_k outside vocabulary')
        ids=list(prefix)
        if not ids:raise ValueError('prefix must be nonempty')
        # Validate the entire prefix even when generation crops to the context.
        if any(type(i) is not int or not 0<=i<self.vocab_size for i in ids):raise ValueError('invalid prefix IDs')
        rng=random.Random(seed)
        for _ in range(count):
            logits=self.logits(ids[-self.context:])[-1]
            scores=[v.data/temperature for v in logits]
            if any(not math.isfinite(x) for x in scores):raise ValueError('temperature scaling overflow')
            eligible=sorted(range(self.vocab_size),key=lambda i:(-scores[i],i))[:top_k]
            maximum=max(scores[i] for i in eligible)
            weights=[math.exp(scores[i]-maximum) for i in eligible]
            threshold=rng.random()*sum(weights);cumulative=0.0
            selected=eligible[-1]
            for i,w in zip(eligible,weights):
                cumulative+=w
                if threshold<cumulative:selected=i;break
            ids.append(selected)
        return ids

    def save(self,path):
        Path(path).write_text(json.dumps({'format':'mm-tiny-decoder-v1','config':self.config,'parameters':[p.data for p in self.parameters()]},sort_keys=True))

    @classmethod
    def load(cls,path):
        # Local teaching artifact: a size/schema bound is not authentication.
        with Path(path).open('rb') as stream:
            raw=stream.read(1_000_001)
        if len(raw)>1_000_000:raise ValueError('checkpoint exceeds local size bound')
        try:payload=json.loads(raw)
        except (ValueError,UnicodeDecodeError) as exc:raise ValueError('invalid checkpoint JSON') from exc
        if not isinstance(payload,dict) or set(payload)!={'format','config','parameters'} or payload['format']!='mm-tiny-decoder-v1':
            raise ValueError('unsupported checkpoint schema or format')
        config=payload['config']
        fields={'vocab_size','d_model','heads','context','ff_width','seed'}
        if not isinstance(config,dict) or set(config)!=fields:
            raise ValueError('invalid checkpoint configuration schema')
        model=cls(**config);values=payload['parameters'];parameters=model.parameters()
        if not isinstance(values,list) or len(parameters)!=len(values):
            raise ValueError('invalid checkpoint parameter shape')
        try:
            if any(type(v) not in (float,int) or not math.isfinite(v) for v in values):
                raise ValueError('invalid checkpoint numeric values')
        except (TypeError,OverflowError) as exc:
            raise ValueError('invalid checkpoint numeric values') from exc
        for p,v in zip(parameters,values):p.data=float(v)
        return model
