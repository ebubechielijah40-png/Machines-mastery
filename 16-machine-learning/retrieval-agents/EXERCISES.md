# Retrieval/control exercises

1. Hand-compute cosine for query[1,0] and document[1,1]. Prove positive rescaling
   of either complete vector leaves the score unchanged.
2. Compute idf when N=3 and a term occurs in every document, then one document.
3. Why is an all-out-of-vocabulary query rejected as evidence rather than assigned
   a confident arbitrary hit? Explain the zero denominator.
4. Give one morphological and one semantic query mismatch for a word-overlap index.
5. Trace accepted AST nodes and intermediate values for `(2+3)*4/2`.
6. Add an independently labeled query where relevant evidence ranks second;
   compare recall@1,@2 and the extraction stage's returned paragraph.
7. Add a tool whose arguments have a strict data type and range. Write rejection
   tests before adding it to the dispatch table; keep it local/read-only.
8. Test a trace that reaches the budget after a successful tool result but before
   finish. Explain why this is distinct from a final answer.
9. Why does a cited document ID not establish factual truth or answer entailment?
10. Demonstrate the difference between per-label memory separation and authenticated
    user isolation. Which contract is outside this code?
11. Challenge: replace the deterministic policy with a deliberately unreliable
    proposal sequence. Preserve executor permissions while testing rejected tool,
    repeated search, unsupported final claim and budget exhaustion separately.
12. Experiment: freeze ten queries/labels before evaluating, retain every failure,
    then compare original tokenization to a documented stemming variant. Do not
    retune labels or call this a universal semantic-retrieval result.
13. Reconstruct from memory an index, typed calculator/executor and bounded loop.
    Supply a hand oracle, injection-as-data test, abstention test and one query
    that fails. State what must change before a learned planner could act safely.
