# 16 — Retrieval-augmented generation (RAG)

RAG adds an external evidence-retrieval pipeline around a generative model.

```text
query → representation → retrieve candidates → rank/filter
→ assemble context → generation → citation/verification
```

## Why it exists

Model parameters are slow to update and do not provide transparent provenance. Retrieval can inject fresher or private information and expose source documents. It also creates new failure modes.

## Failure modes

- relevant document not retrieved;
- irrelevant document ranked highly;
- chunk boundaries remove necessary context;
- stale or poisoned documents;
- generator ignores evidence;
- citations do not support the claim;
- access control leaks restricted documents.

## Evaluation

Separate retrieval quality from generation quality. Measure recall/precision or task-specific hit rates at retrieval, then groundedness/correctness at generation. A good answer cannot tell you which stage succeeded.

## Project

Build a local RAG system over repository documentation. Use a simple lexical baseline first, then embeddings. Create a gold set of questions with known supporting files. Measure retrieval recall before adding generation. Then deliberately insert a misleading document and study ranking/grounding behavior.

## Developed first build: evidence retrieval with measured failures

Begin with [the local retrieval/controller unit](retrieval-agents/README.md).
It derives smoothed TF-IDF/cosine from term counts, implements an index, handles
zero vectors and stable ties, and evaluates six predeclared synthetic questions.
The [actual experiment](retrieval-agents/EXPERIMENTS.md) finds four rank-one hits
and two vocabulary failures. Recall4/6 is a retrieval result on this set, not an
answer-correctness score or a general claim about RAG.

The controller returns cited evidence directly. It deliberately has no generative
model, semantic embedding service, document authorization or corpus freshness
service. Add a generator only after preserving this baseline and measuring
retrieval, support and answer accuracy independently. The [exercises](retrieval-agents/EXERCISES.md)
require an answer-support counterexample, retrieval failure analysis and a
train/evaluation boundary for any learned reranker.
