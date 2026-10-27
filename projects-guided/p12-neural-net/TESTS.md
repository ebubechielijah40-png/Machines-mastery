# Executable verification and independent checks

Python3.10+ standard library; repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/code -p test_autodiff.py -v
python3 -m unittest discover -s 16-machine-learning/training -v
```

The scalar suite checks shared paths, repeated/different roots, accumulation,
forward operand capture, central differences, real-domain failures, exponent0
and a deep graph. The training suite adds a hand cross-entropy oracle, causal
future mutation, sampled decoder parameter gradients, finite atomic SGD updates,
checkpoint round trip, seeded generation, tokenizer boundaries and an actual
250-step XOR fit. Byte-pair tests check unseen Unicode round trips, deterministic
merges and nonoverlapping replacement. Read the test names and source to know
which contract each assertion covers; sampled gradients do not check all weights.

Your tests must include independent arithmetic: for `(x*x+1)^2` at x=3 expect120;
for `x+x*x` at x=2 expect5; for logits[ln2,ln3] and target1 expect gradients
[.4,-.4]. Add a branched failure that an unbranched chain cannot reveal. Keep
ordinary cases, zero/boundary cases and invalid inputs distinct. Finite-difference
agreement can fail near nondifferentiable points or extreme numeric ranges.

Prepared [actual validation evidence](../../16-machine-learning/training/evidence/validation.json)
records executed commands/environment/output. It does not certify your unaided
implementation or constitute full formal verification.
