# Query reasoning attempts

1. Predict `NULL=0`, `NULL IS NULL`, `0 AND NULL`, `1 OR NULL`, `NOT NULL`.
   Explain which survive a WHERE predicate and why Python's bool(None) is not a model.
2. Add customer4 with one order of unknown amount. Distinguish it from Cia using
   COUNT(o.id), COUNT(o.amount) and SUM(o.amount).
3. Remove the NULL blocked row, then remove all blocked rows. Predict NOT IN and
   NOT EXISTS for known keys. What additional policy is required for a NULL key?
4. Write one query returning every customer with the number of positive orders,
   including zero. Explain why WHERE amount>0 after LEFT JOIN fails that requirement.
5. Give a dataset where COUNT(*) and COUNT(right.id) differ after LEFT JOIN. Which
   invariant about right.id does your explanation require?
6. From memory rebuild the truth model and row-by-row joins without SQLite, then
   compare against the real engine. Add a NULL left key to expose the scope limit
   of the nonnull-key anti-join oracle.
