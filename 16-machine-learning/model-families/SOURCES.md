# Claim-level source map

Selected primary author/course scopes were actually inspected on2026-10-23.
These are intellectual references; the derivations, examples, bounded code and
synthetic observations in this unit are original. No full source book, PDF,
figure, dataset or substantial passage is distributed. A live URL is not a
pinned edition, and access does not grant blanket redistribution rights.

| Source and version | Inspected scope | Supported use and limitation |
| --- | --- | --- |
| Stanford CS231n course notes, [Linear Classification](https://cs231n.github.io/linear-classify/) and [Neural Networks1](https://cs231n.github.io/neural-networks-1/), live author/course pages | score/loss distinction, regularization, softmax probability interpretation; single-neuron logistic classifier and tanh/sigmoid saturation | Unit1's conditional modeling foundations; our exact stable scalar loss, gradients, leakage construction and bounds are derived/tested here |
| Stanford CS231n, [Convolutional Networks](https://cs231n.github.io/convolutional-networks/), live course notes | local connectivity, shared parameters, spatial arrangement, sizing and pooling sections | Unit2's operator foundations; periodic ring convention, exact rotation proof and synthetic comparison are ours, not a claimed source benchmark |
| Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, *Dive into Deep Learning*, documentation1.0.3, [§9.7](https://d2l.ai/chapter_recurrent-neural-networks/bptt.html) | §9.7.1 chain-rule parameter dependence and truncation; §9.7.2 unrolled shared parameters and temporal Jacobian products | Unit3's recurrence/reverse-pass foundation; our scalar tanh classifier has a final-only loss and biases, unlike the source's simplified detailed linear example |
| Andrew Ng, Stanford CS229, [Mixtures of Gaussians and the EM algorithm](https://cs229.stanford.edu/summer2019/cs229-notes7b.pdf), four-page handout, summer2019 URL | pp1–3 latent mixture, posterior responsibilities and weighted parameter updates | Unit4's mixture mechanism; exact one-dimensional examples, variance floor and failure experiments are independent derivations |
| Andrew Ng, Stanford Engineering Everywhere CS229, [Part IX: The EM algorithm](https://see.stanford.edu/materials/aimlcs229/cs229-notes8.pdf), eight-page handout, no internal revision date | §§1–2 Jensen's inequality, posterior-tight lower bound and likelihood monotonicity argument | Unit4's bound argument; no global-optimum, finite-precision or held-data guarantee is inferred |
| Daniel Jurafsky and James H. Martin, *Speech and Language Processing*, third-edition draft, [chapter3](https://web.stanford.edu/~jurafsky/slp3/3.pdf), August19,2026 imprint | §3.1 chain factorization, Markov approximation, counts and start/end markers; §3.6.1–2 add-one/add-k discussion | Unit4's n-gram foundations; our character alphabet, smoothing choice and corpus are original; the full book is not bundled or reconstructed |

CS229 spring2020 notes8 and CS231n2025 lecture7 endpoints failed retrieval during
this inspection. They are not counted as inspected full text. Selected successful
alternatives above support the teaching. Dempster/Laird/Rubin1977 and Elman1990
publication metadata/abstracts were located, but their full original papers were
not inspected in this batch; no full paper-reconstruction completion or reported
benchmark is claimed. See the repository's separate research audit for paper gaps.

Source notes establish the cited general mechanisms. The actual run JSON and
[test_families.py](test_families.py) establish only the finite local contracts
and observations described in this unit. They do not verify every statement in
those publications or provide a reproduction of their experiments.
