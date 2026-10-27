# Training unit source scopes

Inspected2026-10-22. This repository supplies original code, numeric examples,
derivations and synthetic experiments. It copies no paper figures, prose,
weights or datasets; source access is not an inferred redistribution license.

| ID | Primary source and inspected version | Exact scope used | Boundary |
| --- | --- | --- | --- |
| T17 | Vaswani et al., *Attention Is All You Need*,2017, [arXiv1706.03762v7](https://arxiv.org/html/1706.03762v7), displayed revision2023-08-02 | §3.1–3.5, equation1, decoder masking, multi-head projections, FFN, embeddings/positions | Historical components only. Our one-block pre-norm/tanh/learned-position decoder differs; no reported BLEU/training result reproduced |
| T00 | Bengio, Ducharme and Vincent, *A Neural Probabilistic Language Model*, NeurIPS2000 [original proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2000/file/728f206c2a01bf572b5940d7d9a8fa4c-Paper.pdf) | PDF pp.1–3, factorized next-word probability and learned distributed representation/model mechanism | Historical intellectual context, not a reconstructed empirical study. Do not confuse this three-author proceedings version with later expanded publications |
| B16 | Sennrich, Haddow and Birch, *Neural Machine Translation of Rare Words with Subword Units*, [arXiv1508.07909v5](https://arxiv.org/html/1508.07909v5),2016-06-10 | §3.2 frequent-symbol-pair merging and encoding discussion | Local byte-level stream variant does not reproduce its word-frequency/end-of-word or translation settings. No translation claim follows |

All scalar gradients, XOR impossibility argument, shapes, finite-difference
oracles, repeated-backward API, optimization settings and observed toy losses
are derived/implemented here. The paper sources do not verify our code. Local
actual logs and independent tests provide separate implementation evidence.
The underlying probability/calculus claims are explained in the internal
foundation lessons rather than replaced by external tutorial links.
