# Inspected source and claim limits

Inspected2026-10-22: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran,
Karthik Narasimhan and Yuan Cao, *ReAct: Synergizing Reasoning and Acting in
Language Models*, [arXiv2210.03629v3](https://arxiv.org/html/2210.03629v3),
revision2023-03-10. Exact scope: §2 policy/context/action/observation setup and
§3.1 search/lookup/finish action space. The source page reports CC BY4.0, but no
paper prose, figures or data are reproduced in this unit.

The source supports the historical policy/action/observation framing. It does
not verify our TF-IDF variant, typed executor, memory interface, calculator,
retrieval labels or results. Those are original bounded specifications and
implementations here. No LLM-generated reasoning or published benchmark result
is reproduced by a deterministic control test. The learned policy and generative
answer stage remain separate future implementation work.
