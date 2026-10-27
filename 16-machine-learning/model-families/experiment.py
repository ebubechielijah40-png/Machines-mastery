"""Execute bounded synthetic model-family protocols; print actual observations."""
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import sys
import time
from discriminative import Logistic, CircularCNN, ScalarRNN, Standardizer, batch_step, metrics
from generative import GaussianMixture, Bigram


def train(model, parameters, examples, steps, rate, clip=5):
    started = time.perf_counter()
    before = metrics(model, parameters, examples)
    checkpoints = []
    for step in range(steps):
        parameters, row = batch_step(model, parameters, examples, rate, clip)
        if step in (0, steps//4, steps//2, steps-1):
            checkpoints.append(dict(step=step, **row))
    return parameters, dict(steps=steps, rate=rate, clip=clip, before=before,
                            after=metrics(model, parameters, examples),
                            checkpoints=checkpoints, seconds=time.perf_counter()-started)


def classification():
    def sample(seed, count, mode):
        rng, out = random.Random(seed), []
        for _ in range(count):
            y = rng.randrange(2)
            x = (2*y-1)*.45 + rng.uniform(-.8,.8)
            shortcut = 4*(2*y-1) if mode == 'label_written_after_outcome' else -4*(2*y-1)
            out.append(((x, shortcut), y))
        return out
    fitting = sample(421, 80, 'label_written_after_outcome')
    iid = sample(422, 128, 'label_written_after_outcome')
    shift = sample(422, 128, 'flipped_shortcut')
    model = Logistic(2)
    p, run = train(model, (0,0,0), fitting, 500, .15)
    stable = Logistic(1)
    stable_train = [(x[:1], y) for x,y in fitting]
    q, stable_run = train(stable, (0,0), stable_train, 500, .15)
    scaler = Standardizer.fit(x for x,_ in fitting)
    leaked_scaler = Standardizer.fit([x for x,_ in fitting]+[x for x,_ in shift])
    return dict(question='What if a label-derived shortcut is available during fitting but changes during deployment?',
                data='Synthetic: y uniform; stable x=.45*(2y-1)+Uniform(-.8,.8); shortcut=+/-4*(2y-1).',
                seeds=dict(train=421,test=422), training=run, parameters=p,
                iid=metrics(model,p,iid),flipped_shortcut=metrics(model,p,shift),
                stable_feature_only=dict(training=stable_run,parameters=q,test=metrics(stable,q,[(x[:1],y) for x,y in shift])),
                scaling=dict(train_only_means=scaler.means,train_and_test_means=leaked_scaler.means,
                             limit='Different means alone do not quantify metric inflation; no claim that this dataset gains accuracy from leaked scaling.'),
                limitations='The shortcut is explicitly constructed from the target; this is not a real observational dataset or proof of causal sufficiency.')


def convolution():
    def ring(start, adjacent, n=12):
        x=[0]*n;x[start%n]=1;x[(start+(1 if adjacent else 5))%n]=1
        return tuple(x)
    fitting=[(ring(i,y),y) for i in range(3) for y in (0,1)]
    held=[(ring(i,y),y) for i in range(3,12) for y in (0,1)]
    cnn=CircularCNN(1,2,'max')
    p,run=train(cnn,(.3,.4,-.2,1,0),fitting,800,.3)
    flat=Logistic(12)
    q,flat_run=train(flat,(0,)*13,fitting,800,.3)
    z=[cnn.logit(p,ring(i,1)) for i in range(12)]
    return dict(question='Can sharing a local detector transfer to unseen circular positions?',
                data='Length12 periodic rings with exactly two ones: adjacent is1; separation5 is0.',
                training_positions=[0,1,2],held_positions=list(range(3,12)),
                cnn=dict(training=run,parameters=p,held=metrics(cnn,p,held),rotated_positive_logit_range=max(z)-min(z)),
                flattened_linear=dict(training=flat_run,parameters=q,held=metrics(flat,q,held)),
                parameters=dict(cnn=cnn.parameter_count,flat_linear=flat.parameter_count),
                limitations='Held rotations are a structural equivariance check, not independent examples from an unknown natural-image distribution. Circular padding and global pooling are essential.')


def recurrence():
    model=ScalarRNN()
    fitting=[((s,)+(0,)*(n-1),int(s>0)) for n in (2,4,8) for s in (-1,1)]
    p,run=train(model,(.7,.7,0,1,0),fitting,900,.15,clip=1)
    lengths={}
    for n in (2,8,16,32,64,128):
        tests=[((s,)+(0,)*(n-1),int(s>0)) for s in (-1,1)]
        lengths[str(n)]=metrics(model,p,tests)
    perturb=[((s,)+(0,)*6+(last,),int(s>0)) for s in (-1,1) for last in (-10,10)]
    init=(.7,.5,0,1,0)
    derivatives={str(n):model.gradients(init,(1,)+(0,)*(n-1),1)[2][0] for n in (2,8,16,32,64,128)}
    linear={str(a):{str(n):a**(n-1) for n in (2,8,32,64)} for a in (.5,1,1.5)}
    return dict(question='Does a fitted recurrent state retain the first sign across blank steps, and what training assumptions break?',
                training=run,parameters=p,training_lengths=[2,4,8],blank_extension=lengths,
                large_final_distractor=metrics(model,p,perturb),initial_first_input_loss_derivative=derivatives,
                analytic_linear_state_derivative=linear,
                limitations='Only six noiseless training sequences; two examples at each held blank length are not a real sequence benchmark. The large new distractor is a declared distribution change.')


def mixtures():
    def data(seed,count):
        rng=random.Random(seed)
        return tuple(rng.gauss(-2,.35) if rng.random()<.4 else rng.gauss(2,.55) for _ in range(count))
    fitting,held=data(601,160),data(602,512)
    results={}
    for name,initial in [('separated_initialization',(-1,1)),('identical_initialization',(0,0))]:
        model=GaussianMixture((.5,.5),initial,(2,2))
        before=model.nll(fitting);history=[before]
        for _ in range(40):
            model=model.em_step(fitting,.01);history.append(model.nll(fitting))
        results[name]=dict(before_nll=before,training_nll=model.nll(fitting),held_nll=model.nll(held),
                           likelihood_decrease_max=max([0]+[history[i+1]-history[i] for i in range(len(history)-1)]),
                           weights=model.weights,means=model.means,variances=model.variances,
                           sample=model.sample(12,seed=603),history=history)
    floor_cases=[]
    for floor in (.01,1e-6,1e-12):
        model=GaussianMixture((1,),(1,),(1,)).em_step([1,1,1],floor)
        floor_cases.append(dict(floor=floor,variance=model.variances[0],nll=model.nll([1,1,1])))
    return dict(question='Can latent assignments fit a two-mode density, and does better likelihood ensure meaningful structure?',
                data='Independent synthetic draws: weight.4 N(-2,.35^2), weight.6 N(2,.55^2).',
                seeds=dict(train=601,held=602,sample=603),training_count=len(fitting),held_count=len(held),
                steps=40,variance_floor=.01,runs=results,identical_data_floor_cases=floor_cases,
                limitations='A one-dimensional assumed Gaussian family with known synthetic generating process; component identities are permutable. Degenerate repeated data are not evidence of useful generalization.')


def bigrams():
    documents=['a'+'x'*k+'a' for k in (2,3,4,5)] + ['b'+'x'*k+'b' for k in (2,3,4,5)]
    model=Bigram.fit(documents,('a','b','x'),alpha=.1)
    p=model.distribution('x')
    return dict(question='Does matching local transitions preserve a dependency on the first symbol?',
                documents=documents,alphabet=model.alphabet,alpha=model.alpha,counts=model.counts,
                training_nll_including_eos=model.nll(documents),
                condition_on_next_symbol_being_a_or_b=dict(a=p[0]/(p[0]+p[1]),b=p[1]/(p[0]+p[1])),
                samples=[model.sample(24,seed=i) for i in range(16)],
                limitations='The model conditions on only the previous character. Equal a/b conditional probability is an exact structural failure to remember the first bit, even if some samples happen to match it.')


if __name__=='__main__':
    root=Path(__file__).resolve().parent
    report=dict(observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,
                platform=platform.platform(),source_sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
                    for n in ('discriminative.py','generative.py','experiment.py','test_families.py')},
                classification=classification(),convolution=convolution(),recurrence=recurrence(),mixtures=mixtures(),bigrams=bigrams(),
                scope='Actual independent synthetic teaching experiments. No historical benchmark, natural image task, real language model, causal estimate or production performance certification.')
    print(json.dumps(report,indent=2,allow_nan=False))
