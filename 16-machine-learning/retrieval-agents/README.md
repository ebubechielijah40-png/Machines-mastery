# Retrieval, typed tools and a bounded decision loop

This build follows the [trained numerical-model sequence](../training/README.md).
Training teaches parameters to fit examples; it does not grant current factual
knowledge, execute tools or establish which source supports a claim. Here we
separate **retrieval quality**, **answer support**, **action authorization** and
**control flow** so failures can be measured independently.

The implementation is a real local lexical index, a constrained arithmetic tool
and a deterministic controller. It does **not** call an LLM or implement a learned
planner. Its answer stage extracts the first retrieved document. This is a
retrieval/tool-system teaching baseline, not a claimed full generative RAG or
ReAct benchmark reproduction. A learned proposer can later replace the policy
without acquiring permission to bypass the executor.

## 1. What problem retrieval solves, and what it cannot solve

Imagine a model whose parameters were fixed before a lab changed its runbook.
Retraining every time a document changes is one way to update behavior, but
it mixes data maintenance with expensive parameter estimation. Retrieval keeps
records in a separately inspectable corpus and selects evidence at request time.
The selected record can still be stale, incorrect, irrelevant or malicious.
A citation says where text came from; it does not prove the text true.

Our corpus has four original synthetic runbook paragraphs with stable IDs.
The input is a query string; outputs are ranked `(id,score,text)` hits. The
index state contains token counts, document frequencies, weighted vectors and
norms. It never fetches the network or reads arbitrary files. The caller owns
the corpus and chooses a bounded query/number of hits.

Prerequisites: [vectors/dot products](../../foundations/mathematics/core/03_VECTORS_MAPS.md),
logarithms as monotone scale transforms, Python dictionaries/loops and the
[probability/evaluation bridge](../../foundations/statistics/probability-inference/README.md).
No electronics, chemistry or physical-model assumption is needed. You should be
able to compute one vector norm and distinguish an expected label from a
retrieved document before interpreting evaluation numbers.

## 2. Build a lexical ranker from arithmetic

Tokenize by lowercasing and splitting into word-character runs. This simple
rule has no stemming or learned semantics: `commit` and `committed` are different
features. Let tf(t,d) count term t in document d, and df(t) count documents
containing t. For N documents, define the particular weighting used here:

\[
\operatorname{idf}(t)=\log\frac{N+1}{\operatorname{df}(t)+1}+1,
\quad w(t,d)=(1+\log\operatorname{tf}(t,d))\operatorname{idf}(t)
\]

for nonzero counts, and weight0 when absent. These are an explicit local
TF-IDF variant, not a universal formula or a claim that its heuristic is optimal.
A frequent word still carries positive weight; the logarithms moderate repetition.
Build a query vector using the same frozen vocabulary and idf values.

Cosine score is q·d/(||q|| ||d||). Dot products count overlap in weighted
coordinates; division removes vector length scale. It does not infer a semantic
relationship between disjoint word sets. If the query has no indexed terms, its
norm is zero and the implementation returns no hit instead of dividing by zero.
An empty document likewise cannot supply a positive cosine denominator.

**Hand oracle:** two documents both contain `x y`, and the query is x. Every
present feature has idf1 and weight1. The document norm is sqrt2, query norm1,
dot product1, so each score is1/sqrt2≈.707107. A stable document-ID tie rule
chooses a before b regardless of insertion order. This independently calculated
case tests ranking arithmetic, not its usefulness on natural-language questions.

Multiplying every coordinate of one vector by a positive constant leaves cosine
unchanged. Repeating only one term changes its direction and usually its score.
Adding irrelevant terms can lower the cosine of a relevant document; document
chunk size therefore matters. A production retriever may need sparse inverted
postings or a dense index, filters and versioning. This tiny implementation scans
all document vectors: memory follows total nonzero features, and query work
includes every document. No billion-document scalability claim is made.

## 3. Evidence selection differs from generation

Retrieval-augmented generation would normally pass selected evidence and a
question to a generative model. That model might paraphrase, combine unsupported
claims, ignore sources or follow instructions embedded in a document. Our
baseline instead returns the first hit's exact original text and its ID. This
makes provenance easy to inspect while leaving relevance and truth unresolved.
An overlap-only ranker can confidently select the wrong paragraph.

A future model adapter should return a typed proposal and an answer with claim-
to-evidence mappings. Check citation existence, source version, support and
contradictions separately. Merely appending an ID to fluent text does not prove
entailment. The three-character decoder in the previous unit cannot answer these
runbook questions; attaching it would not supply a meaningful factual model.

## 4. Tools are typed capabilities, not executable prose

The executor accepts exactly `{"tool":name,"args":object}`. Permitted tools are
`search` with one query string and `calculator` with one expression string.
Extra keys, an unknown tool or wrong argument schema are rejected. The calculator
parses an arithmetic grammar using Python's AST and a hand-written visitor. It
allows numeric constants, unary signs and +,-,*,/; it never calls `eval`.
Calls, attribute lookup, indexing, lists and exponentiation are outside the grammar.
Input length, AST node count, literal magnitude and intermediate magnitude are
bounded. For `(2+3)*4/2`, the tree computes5, then20, then10. For `1/0`, it reports
a domain failure. For a call-like string it rejects the node instead of treating
it as an instruction.

These limits describe this controlled local tool, not a general sandbox for
arbitrary programs. A new tool may write files, incur cost or reveal data; adding
its name requires its own authorization, resource and idempotency contract.
A proposer can suggest an action; it cannot create a capability by naming it.

The injection test indexes text saying to ignore rules and call a shell. The
answer still contains that untrusted sentence because extraction copies data,
but **no new action** is parsed from it. The separate proposal for a shell tool
is rejected. This establishes a local data/control boundary. It is not evidence
that a real LLM resists all prompt injection or that displaying malicious advice
is semantically safe in every product.

## 5. A small agent is an inspectable state machine

Our transparent policy chooses a calculator action for tasks prefixed `calc `,
otherwise search, then finish. The controller records accepted actions,
observations, rejection events and termination status. Its current policy is
written code, not a trained language model or a private reasoning trace. ReAct's
inspected framework motivates separating a policy, actions and observations
[RA23,§2]; its actual LLM results are not reproduced here.

A maximum-step budget bounds attempts. With only one allowed step, search may
succeed but finish has not occurred: status is `budget_exhausted`, answer is None.
An invalid action returns `rejected`. A search with no overlap finishes as
`abstain`. These statuses should not be silently converted to a fabricated answer
or a successful run. Retries, fallback policies and tool deadlines are not
implemented. An external tool returning uncertain outcome needs reconciliation,
not blind retry; study the database log and ordered-write projects for that issue.

Session history records the last ten task/status pairs per caller-supplied label.
Tests show labels a and b keep separate histories; labels are **not authenticated
identities**. The number of distinct labels is not globally capped, so this is
not a ready multi-tenant memory service. Longer-term semantic memory also needs
retention, consent, stale-record handling, correction and retrieval evaluation.

## 6. Evaluate a pipeline by its failure stage

For each query, define the expected supporting document before running. Recall@k
is1 if that document appears among the first k, otherwise0; average across the
frozen query list. This measures evidence retrieval, not final answer correctness.
A top hit ID can be wrong, while a correct second hit may never reach the answer
stage. Answer support, arithmetic correctness, authorized-action rate, abstention
and termination require separate checks.

The [raw experiment](evidence/results-2026-10-22.json) uses six original queries
and four paragraphs. It intentionally includes morphological and semantic
mismatches to expose lexical failure. The query `recover a committed transaction`
shares no exact feature with `transactions commit ... recovery` under this
particular tokenizer; it may retrieve nothing despite being semantically related.
Do not repair the evaluation label after seeing output just to improve the score.

## Build and replay

Python3.10+ standard library; from repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/retrieval-agents -v
python3 16-machine-learning/retrieval-agents/experiment.py
```

Milestones: hand-score two vectors; build the index/tie/zero-overlap contracts;
freeze query labels; implement the arithmetic visitor and rejection tests;
add typed action validation; add bounded state transitions and trace output;
measure recall and failure statuses. Deliver raw output, source/version map,
independent test cases and a failure report. Use [EXERCISES](EXERCISES.md), then
[HINTS](HINTS.md) and [SOLUTIONS](SOLUTIONS.md). Inspected source scopes are in
[SOURCES](SOURCES.md). No external service, credential or real user data is needed.
