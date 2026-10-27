"""Deterministic synthetic learning experiment; stdout is observed JSON only."""
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import sys
import time
from tiny_models import CharacterTokenizer,MLP,TinyDecoder,sgd


def score(model,sequences):
    return sum(model.loss(s).data for s in sequences)/len(sequences)


def train(model,sequences,steps,rate,seed,clip=1):
    rng=random.Random(seed);trace=[]
    start=time.perf_counter()
    for step in range(steps):
        sequence=sequences[rng.randrange(len(sequences))]
        loss=model.loss(sequence)
        loss.backward()
        gradient_norm=sgd(model.parameters(),rate,clip_norm=clip)
        if step in {0,steps//4,steps//2,steps-1}:
            trace.append(dict(step=step+1,selected_loss_before_update=loss.data,gradient_l2_before_clipping=gradient_norm))
    return dict(steps=steps,learning_rate=rate,clip_norm=clip,trace=trace,elapsed_seconds=time.perf_counter()-start)


def main():
    xor=[([-1,-1],-1),([-1,1],1),([1,-1],1),([1,1],-1)]
    net=MLP(seed=7);xor_before=net.loss(xor).data
    for _ in range(300):
        loss=net.loss(xor);loss.backward();sgd(net.parameters(),.1)
    train_text=['abcab','bcabc'];held_text=['cabca'];shift_text=['acbac']
    tokenizer=CharacterTokenizer(''.join(train_text))
    training=[tokenizer.encode(s) for s in train_text]
    held=[tokenizer.encode(s) for s in held_text]
    shifted=[tokenizer.encode(s) for s in shift_text]
    model=TinyDecoder(len(tokenizer.symbols),seed=11)
    initial=dict(train_nll=score(model,training),held_nll=score(model,held),shift_nll=score(model,shifted))
    run=train(model,training,180,.08,seed=13)
    final=dict(train_nll=score(model,training),held_nll=score(model,held),shift_nll=score(model,shifted))
    final['held_perplexity']=math.exp(final['held_nll'])
    clean_generation=tokenizer.decode(model.generate(tokenizer.encode('c'),15,top_k=1))
    # Deliberate protocol violation: optimize on the held-out case. A lower
    # subsequent 'test' loss cannot be presented as fresh generalization.
    before_contamination=score(model,held)
    contaminated_run=train(model,held,40,.08,seed=17)
    after_contamination=score(model,held)
    unstable=TinyDecoder(len(tokenizer.symbols),seed=11)
    high_rate=train(unstable,training,30,3,seed=13,clip=None)
    high_rate['final_train_nll']=score(unstable,training)
    payload={'kind':'executed synthetic software experiment; no published benchmark reproduction',
      'environment':dict(python=sys.version,platform=platform.platform()),
      'xor':dict(seed=7,steps=300,initial_mse=xor_before,final_mse=net.loss(xor).data,predictions=[net(x).data for x,y in xor],all_truth_table_rows_used_for_training=True),
      'corpus':dict(training_strings=train_text,held_strings=held_text,shift_strings=shift_text,vocabulary=tokenizer.symbols,sha256=hashlib.sha256(json.dumps([train_text,held_text,shift_text]).encode()).hexdigest(),train_held_exact_overlap=bool(set(train_text)&set(held_text))),
      'decoder':dict(config=model.config,parameters=len(model.parameters()),initial=initial,training=run,final_before_contamination=final,greedy_generation_before_contamination=clean_generation),
      'deliberate_test_contamination':dict(before_held_nll=before_contamination,after_held_nll=after_contamination,training=contaminated_run,valid_heldout_evaluation=False),
      'high_learning_rate':high_rate,
      'limitations':['Two training strings and one held string do not estimate natural-language generalization.','Vocabulary is fixed from training strings, never fit on held strings.','XOR truth table fit uses every row: no held-out XOR generalization claim.','Decoder is original one-block pre-norm/tanh/learned-position variation, not paper architecture.','Timing is one local run, not a performance comparison.']}
    print(json.dumps(payload,indent=2,allow_nan=False))


if __name__=='__main__':main()
