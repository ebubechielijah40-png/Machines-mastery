# Information about a variable depends on the model

A four-byte integer always occupies 32 wire bits, but its uncertainty need not be 32 bits. If a header length is always six, learning it removes no uncertainty for an observer who already knows that rule. If its four possible lengths are equally likely, identifying it resolves two bits of uncertainty. This distinction prepares [bounded framing](../../06-networking/stream-boundaries/LESSON.md), [provenance](../../security-cryptography-mastery/provenance/LESSON.md) and [privacy count release](../../13-privacy/count-release/LESSON.md).

Entry gate: interpret a probability table that sums to one, multiply independent probabilities, and use `log2(8)=3`. If needed, review [algebra](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md). This unit treats finite distributions. It does not implement compression or reconstruct the noisy-channel coding theorem.

## From alternatives to expected uncertainty

For N equally probable possibilities, a binary decision tree needs log2 N balanced decisions when N is a power of two. Unequal probabilities motivate surprise `s(x)=-log2 p(x)`: an event of probability 1/8 carries three bits by this convention. Independent events have multiplying probabilities, so their surprises add. Average surprise is discrete entropy `H(X)=-sum_x p(x)log2 p(x)` with the zero-probability contribution defined by its limit as zero. These are the finite-entropy concepts developed in Shannon's primary paper [I1].

Work the original distribution `[1/4,1/2,1/4]`: surprises are 2,1,2; the weighted mean is `.25*2+.5*1+.25*2=1.5` bits. Labels can be `low,mid,high` or `0,1,2`; renaming categories bijectively leaves the probabilities and H unchanged. A fixed two-bit encoding still uses two bits per symbol. Expected uncertainty and a concrete code length are different quantities; no optimal code implementation is supplied here.

## Joint tables preserve relationships

For two bits X,Y, list probabilities in a two-by-two table. If all four cells are .25, X and Y are independent: `H(X)=H(Y)=1` and `H(X,Y)=2`. If only the two diagonal cells have .5 each, `H(X,Y)=1`: knowing Y determines X, leaving `H(X|Y)=H(X,Y)-H(Y)=0`. The mutual information `I(X;Y)=H(X)+H(Y)-H(X,Y)` is respectively zero or one bit. One can also calculate it directly as `sum p(x,y)log2[p(x,y)/(p(x)p(y))]`; the tests use that separate expression as an oracle.

Now construct Y as X flipped with independent probability r. X is fair, so Y remains fair. Conditional uncertainty is the binary entropy of r. Thus `I(X;Y)=1-H_binary(r)`. At r=0, Y equals X; at .5 it contains no information about X; at 1 it is always the opposite of X and again determines X perfectly. Therefore a high raw disagreement rate does not by itself mean low recoverable information. A receiver knowing the deterministic inversion can invert it. A physical channel with unknown changing flip behavior requires a richer model.

## Executable controlled calculation

[information.py](information.py) normalizes finite nonnegative weights, skips zero terms, and computes marginals from a rectangular joint table. The table has at most 64×64 cells. No random samples are used; these are finite model calculations with floating log approximations. It does not estimate entropy consistently from arbitrary small samples, certify a cryptographic random source or prove that observed independence equals causal independence.

```sh
python3 -m unittest discover -s 08-information-science/finite-information -v
python3 08-information-science/finite-information/experiment.py
```

Question: does disagreement monotonically destroy information? Hold uniform X and the independent bit-flip mechanism fixed; vary r across 0,.01,.1,.25,.5,.75,.9,1. Predict a decrease to zero and then an increase. [Actual computed tables](evidence/observed.json) report exact model probabilities and numerically calculated entropies, not observed packet errors or private-data leakage. The r=1 endpoint distinguishes the prediction from the tempting monotonic claim.

A cryptographic ciphertext may have high measured byte entropy while still exposing a reused keystream or known seed. An authenticated record may have predictable fields while still requiring integrity. This unit's numbers are not security certifications. Continue with [exercises](EXERCISES.md) and [source scope](SOURCES.md).
