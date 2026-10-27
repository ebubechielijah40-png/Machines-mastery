# Differential privacy source verification

C. Dwork and A. Roth, *The Algorithmic Foundations of Differential Privacy*, Foundations and Trends in Theoretical Computer Science 9(3–4), 211–407, 2014, DOI [10.1561/0400000042](https://doi.org/10.1561/0400000042). Inspected the [author-hosted complete PDF](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) on 2026-10-22. This is a bounded concept reconstruction, not a reconstruction of the whole monograph.

| ID | Exact inspected scope | Supports | Not claimed |
| --- | --- | --- | --- |
| P1 | Printed p17, Definition 2.4 (PDF page21); pp31–33, Definitions3.1–3.3, Theorem3.6 (PDF pages35–37) | Neighbor-based privacy definition, L1 sensitivity, Laplace scale and density-ratio proof | Certified finite-float sampler; person-level contribution enforcement; all DP mechanisms |
| P2 | Printed pp42–43 (PDF pages46–47), Theorems3.14 and3.16 and Corollary3.15 | Conservative additive composition context | Advanced composition or adaptive accountant implementation |

The lesson develops original scalar examples, explicit derivations, exercises and experiments; it does not reproduce book passages, figures or full chapters. Source copyright remains with its authors/publisher; link the source rather than redistributing its content. Noise utility observations are independently executed on synthetic data and are not the monograph's reported experiments.

Unit classification: STRONG as a transparent mathematical/simulation lesson with explicit implementation limits. Privacy engineering as a domain remains PARTIAL: production finite-precision mechanisms, persistent budget enforcement, person-level contribution controls, retention/deletion, linkability analysis and organizational privacy operations are not completed here.
