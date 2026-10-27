# Attention source verification

Access date: **2026-10-22**. This record describes what was inspected, not a
claim that the entire AI curriculum or every numerical statement is verified.
Original educational code and examples are independently written here.

## A17 — primary architecture paper

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N.
Gomez, Łukasz Kaiser, Illia Polosukhin. *Attention Is All You Need*. 2017.
Inspected version: [arXiv:1706.03762v7](https://arxiv.org/html/1706.03762v7),
revision displayed 2023-08-02. Read sections 1–6, formula (1), footnote 1,
Tables 1–3 and the architecture descriptions. This is the original paper, not
an implementation tutorial. The repository does not copy its tables/figures,
bundle the paper, or presume an unrestricted redistribution license. The page
identifies arXiv's non-exclusive license and a separate limited Google grant
for scholarly/journalistic table and figure reproduction.

Claim map:

| Local material | Inspected locator | Scope |
| --- | --- | --- |
| Scaled dot-product formula and independent-coordinate variance premise | §3.2.1, equation (1), footnote 1 | Historical formula/premise; local algebra and examples independently derived |
| Multiple projections/concatenation | §3.2.2 | Architectural mechanism, not semantic labels for heads |
| Causal masking | §3.1 decoder, §3.2.3 | Forbidden connections excluded before softmax |
| Research reported numbers | §6.1, Table 2 | Reported, not independently reproduced; EN-FR prose/table discrepancy retained |
| Toy VJP and cache | local DERIVATION.md and code | Original derivations; not claimed as this paper's contribution or experiment |

## Local execution evidence

[Experiment JSON](evidence/2026-10-22-attention.json) records Python/platform,
seed, input dimensions and observations. [Test log](evidence/2026-10-22-tests.txt)
records actual execution. Tests are implementation evidence; they do not verify
reported research benchmarks or imply learner mastery.
