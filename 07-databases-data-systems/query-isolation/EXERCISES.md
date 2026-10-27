# Exercises: attempt before opening hints or solutions

1. Project the device column of the five-row worked fixture. Distinguish bag,
   DISTINCT result and possible output order. What information was discarded?
2. Compute count(*),count(value),sum(value),avg(value) for A and B. Explain why
   filling NULL with0 changes the question.
3. Derive every three-valued AND/OR pair and NOT U. Which predicates survive WHERE?
4. Trace all12 pairs in the worked equijoin and identify its six outputs.
5. Prove that a right-side hash bucket must store a list, not one row. Give a
   smallest counterexample for overwriting it.
6. Implement bag projection, selection and both joins from blank files. Check
   duplicate multiplicities against independently hand-computed fixtures.
7. Why is a set comparison insufficient as a join oracle? Construct an incorrect
   output with the correct set of rows.
8. Move the worked LEFT JOIN predicate between ON and WHERE and predict the
   unmatched row. Then execute both and retain observations.
9. Derive expected hash complexity including k outputs. Construct n=m with k=n*m.
   Does this contradict the claimed complexity?
10. Trace the five-event WAL schedule. At which SELECT is the deferred read
    snapshot established? What changes after rollback and why is an upgrade rejected?
11. Explain how separate autocommit read/replace statements lose a debit without
    contradicting isolation of individual SQL transactions. Design a repair.
12. Experiment: hold data/query/version fixed, create one index and compare
    correctness/plans. If measuring time, use repeated warm/cold protocols and
    retain distributions; do not infer time from a plan label alone.
13. Transfer: model jobs and attempts with repeated job IDs and missing outcomes.
    Derive a query for jobs with zero successful attempts that preserves jobs with
    no attempts. Explain authorization and transaction assumptions, then implement
    and test it without consulting the sensor fixture.
