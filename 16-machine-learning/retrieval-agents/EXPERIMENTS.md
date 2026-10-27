# Retrieval/control experiment

Research question: does surface-word overlap retrieve semantically related
runbooks, and can control failures be identified independently of retrieval?
Prediction: exact-word queries succeed; morphology/semantic changes can fail.
A single permitted controller step can run a tool but cannot also finish.
An unlisted tool proposal must be rejected, regardless of its text.

Controls: four frozen original paragraphs and six predefined query/target pairs;
same weighting/tokenization/tie rule. Independent variables across cases are
wording; the separate budget case changes max_steps3→1. Instrumentation: exact
ranked IDs, recall@1,@2, trace events and terminal status. This small case set
is not an unbiased sample of user tasks.

Procedure: run `python3 16-machine-learning/retrieval-agents/experiment.py` from
root and retain stdout. [Executed raw output](evidence/results-2026-10-22.json)
records Python/platform, complete inputs, hits and failures. Expected labels
are part of the script before execution, not generated from observed rankings.

Actual observations: the four direct lexical cases retrieved their target at
rank1; the morphological and semantic cases returned no hit. Mean recall@1
and@2 were both4/6≈.666667. The absent-evidence query abstained; the one-step
case exhausted its budget; the shell proposal was rejected; bounded arithmetic
returned20. These are deterministic local observations, not ReAct/RAG benchmark
numbers or proof of real-model prompt-injection resistance.

Interpretation: word normalization/overlap imposes a visible failure mode, while
executor/budget tests isolate different contracts. Alternative explanations for
rank failures include document granularity and our particular weighting; these
six cases cannot tell which retriever is generally best. Follow-ups: frozen
larger labels, stemming versus dense retrieval under identical cases, noisy
source versions, multi-document evidence and learned-proposer failures. No
unrun result is claimed.
