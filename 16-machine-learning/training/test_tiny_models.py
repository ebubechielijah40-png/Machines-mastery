import math
import json
from pathlib import Path
import tempfile
import unittest
from tiny_models import CharacterTokenizer,MLP,TinyDecoder,Value,cross_entropy,normalized_exp,sgd


class TrainingTests(unittest.TestCase):
    def test_tokenizer_roundtrip_and_frozen_unknown_boundary(self):
        tok=CharacterTokenizer('cabca')
        self.assertEqual(tok.symbols,('a','b','c'))
        self.assertEqual(tok.decode(tok.encode('abccba')),'abccba')
        self.assertEqual(tok.decode(iter([2,0,1])),'cab')
        for x in ['x']:
            with self.assertRaises(ValueError):tok.encode(x)
        with self.assertRaises(ValueError):tok.decode([True])

    def test_cross_entropy_hand_oracle_and_gradients(self):
        logits=[Value(math.log(2)),Value(math.log(3))]
        loss=cross_entropy(logits,1);loss.backward()
        self.assertAlmostEqual(loss.data,-math.log(.6))
        self.assertAlmostEqual(logits[0].grad,.4)
        self.assertAlmostEqual(logits[1].grad,-.4)
        shifted=cross_entropy([Value(math.log(2)+1000),Value(math.log(3)+1000)],1)
        self.assertAlmostEqual(loss.data,shifted.data,places=12)

    def test_causal_prefix_and_future_mutation(self):
        model=TinyDecoder(3,d_model=4,heads=2,ff_width=4,context=4,seed=3)
        original=model.logits([0,1,2,0]);changed=model.logits([0,1,0,2])
        for t in range(2):
            self.assertEqual([x.data for x in original[t]],[x.data for x in changed[t]])
        prefix=model.logits([0,1])
        self.assertEqual([x.data for x in original[1]],[x.data for x in prefix[1]])

    def test_decoder_parameter_gradients_independent_finite_difference(self):
        model=TinyDecoder(3,d_model=4,heads=2,ff_width=4,context=3,seed=2)
        loss=model.loss([0,1,2,0]);loss.backward()
        params=model.parameters()
        for i in [0,4,12,23,27,40,62,85,100,130,len(params)-1]:
            p=params[i];analytic=p.grad;old=p.data;h=1e-5
            p.data=old+h;positive=model.loss([0,1,2,0]).data
            p.data=old-h;negative=model.loss([0,1,2,0]).data
            p.data=old
            self.assertAlmostEqual(analytic,(positive-negative)/(2*h),places=5,msg=f'parameter{i}')

    def test_model_save_load_and_generation_seed(self):
        model=TinyDecoder(3,d_model=4,heads=2,ff_width=4,context=3,seed=2)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'model.json';model.save(p);copy=TinyDecoder.load(p)
            self.assertEqual([x.data for x in model.parameters()],[x.data for x in copy.parameters()])
            self.assertEqual(model.generate([0],5,seed=1),copy.generate([0],5,seed=1))
        greedy=model.generate([0],6,top_k=1)
        self.assertEqual(greedy,model.generate([0],6,top_k=1,seed=99))

    def test_sgd_clipping_and_atomic_rejection(self):
        a,b=Value(1),Value(2);a.grad=3;b.grad=4
        self.assertEqual(sgd([a,b],.1,clip_norm=1),5)
        self.assertAlmostEqual(a.data,.94);self.assertAlmostEqual(b.data,1.92)
        a.grad=math.nan
        with self.assertRaises(ValueError):sgd([a,b],.1)
        self.assertAlmostEqual(b.data,1.92)

    def test_mlp_learns_truth_table_not_a_generalization_claim(self):
        data=[([-1,-1],-1),([-1,1],1),([1,-1],1),([1,1],-1)]
        net=MLP(seed=7);before=net.loss(data).data
        for _ in range(250):
            loss=net.loss(data);loss.backward();sgd(net.parameters(),.1)
        self.assertLess(net.loss(data).data,before*.05)
        self.assertEqual([int(net(x).data>0) for x,y in data],[0,1,1,0])

    def test_iterable_sgd_updates_and_duplicate_parameter_rejection(self):
        a,b=Value(1),Value(2);a.grad=2;b.grad=-3
        norm=sgd(iter([a,b]),.1)
        self.assertAlmostEqual(norm,math.sqrt(13))
        self.assertAlmostEqual(a.data,.8);self.assertAlmostEqual(b.data,2.3)
        with self.assertRaises(ValueError):sgd([a,a],.1)
        self.assertAlmostEqual(a.data,.8)

    def test_checkpoint_schema_numeric_and_size_boundaries(self):
        model=TinyDecoder(3,d_model=4,heads=2,context=3,ff_width=4,seed=2)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'model.json';model.save(path)
            original=json.loads(path.read_text())
            bad=[]
            for payload in [[],None,{'format':'mm-tiny-decoder-v1'},dict(original,extra=1),dict(original,config=[]),dict(original,parameters={})]:
                bad.append(payload)
            boolean=json.loads(json.dumps(original));boolean['parameters'][0]=True;bad.append(boolean)
            wrong_config=json.loads(json.dumps(original));wrong_config['config']['seed']=True;bad.append(wrong_config)
            missing_config=json.loads(json.dumps(original));del missing_config['config']['heads'];bad.append(missing_config)
            nonfinite=json.loads(json.dumps(original));nonfinite['parameters'][0]=float('inf');bad.append(nonfinite)
            for payload in bad:
                path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError):TinyDecoder.load(path)
            path.write_bytes(b' '*1_000_001)
            with self.assertRaises(ValueError):TinyDecoder.load(path)

    def test_invalid_shapes_and_token_contracts(self):
        for kwargs in [dict(vocab_size=1),dict(vocab_size=3,d_model=5,heads=2),dict(vocab_size=3,context=100)]:
            with self.assertRaises(ValueError):TinyDecoder(**kwargs)
        model=TinyDecoder(3)
        for seq in [[],[True],[3],[0]*5]:
            with self.assertRaises(ValueError):model.logits(seq)
        with self.assertRaises(ValueError):model.generate([0],1,temperature=0)
        with self.assertRaises(ValueError):model.generate([0],1,temperature=1e-320)


if __name__=='__main__':unittest.main(verbosity=2)
