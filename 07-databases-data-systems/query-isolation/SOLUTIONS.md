# Solutions and checks after an original attempt

1. Bag projection A,A,A,B,NULL; distinct categories A,B,NULL. Without ORDER BY,
   do not require that printed order. Individual values/readings and identities
   are lost even though occurrence counts remain.
2. A=(3,2,6,3); B=(1,0,NULL,NULL). Filling absent readings with0 changes A's mean
   from6/2=3 to6/3=2 and asserts a measurement that was absent.
3. The README gives the symmetric truth table; add F AND T=F, U AND T=U,
   F OR T=T, U OR T=T and U with F using symmetry. NOT U=U. Only true survives.
4. The a row pairs with values2,3,4; the b row does too. Four NULL-key candidate
   comparisons involving at least one missing key are unknown; the remaining
   unmatched pairs are also excluded. Six qualifying pairs out of12.
5. Two right rows (1,'x'),(1,'y') and one left(1,) must yield two outputs.
   A scalar payload map overwrites one. Buckets preserve all occurrences.
6. Compare your original attempt to [relations.py](relations.py) only now. Its
   equality domain is narrower than full SQL. Explain each restriction before
   claiming a differential match on new input types.
7. Correct output [(1,),(1,)] and wrong output [(1,)] have equal sets but
   different bags. Counter(tuple_rows) retains the lost multiplicity.
8. ON preserves(2,NULL); WHERE drops it because the comparison is unknown.
9. If all n left/right keys equal1, k=n². O(n+m+k) therefore becomes O(n²)
   even under ideal hash lookup; the k term was necessary.
10. A's first SELECT after BEGIN establishes the view. B's committed transfer
    does not change it. The stale writer cannot extend the current history from
    that view. Rollback ends it; a fresh read observes(90,110).
11. B's replacement80 uses a stale100 and erases A's debit10. The units were
    separate SQL transactions. Atomic relative debits produce70 here; a larger
    read/check/update operation needs a protected transaction and retry policy.
12. The recorded run has10 matches on1000 rows, a scan before and an indexed
    search after, with equal ordered results. Timing conclusions require timing
    observations. The plan record alone cannot supply them.
13. One solution is a NOT EXISTS subquery selecting attempts with matching job
    ID and outcome='success'. For a job with no attempts, EXISTS is false and
    NOT EXISTS true. For NULL outcomes, equality is unknown and is not success.
    A LEFT JOIN filtered in ON and grouped with count(attempt.id)=0 also works
    if attempt.id is guaranteed non-NULL; count(*) would count the synthetic
    unmatched row and give the wrong answer. Read permissions and a consistent
    observation boundary are additional assumptions, not consequences of SQL text.

Reconstruction: reproduce the job solution plus missing/duplicate/success cases
without opening code. Grade the reasoning and counterexamples in addition to
reference-test behavior. No prepared answer proves unaided mastery.
