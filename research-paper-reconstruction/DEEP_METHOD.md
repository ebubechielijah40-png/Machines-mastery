# How to reconstruct a research paper deeply

Do not start by summarizing sections. Rebuild the causal/evidential structure.

1. **World before the paper:** what capability/problem existed?
2. **Gap:** what could prior methods not do, or what evidence was missing?
3. **Question:** exact research question or engineering objective.
4. **Assumptions:** data distribution, hardware, threat model, workload, mathematical model.
5. **Method:** inputs → transformations → outputs, with algorithms and state.
6. **Design choices:** why this architecture/loss/metric/baseline/dataset?
7. **Experiment:** variables, controls, baselines, metrics, repetitions, statistical treatment.
8. **Results:** what was actually observed?
9. **Claim boundary:** what does that evidence support, and what does it not?
10. **Reproduction:** what code/data/environment is needed? What is unavailable?
11. **Modern relevance:** which ideas survived, changed, or became obsolete?
12. **Falsification:** what observation would weaken the central conclusion?

A good reconstruction should let you explain the paper to a technical peer, reimplement the core method where feasible, and critique it without relying on vague prestige or citation count.
