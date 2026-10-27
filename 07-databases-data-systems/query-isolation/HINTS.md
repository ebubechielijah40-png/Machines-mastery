# Hints

1–3: projection removes columns, not occurrences. Aggregate absence and row
absence differ. Evaluate whether any possible unknown resolution can make a
conjunction true or a disjunction false.

4–7: label occurrences even when values are identical. Count every left-right
occurrence pair. A set collapses multiplicity, hiding missing duplicates.

8: outer-row construction occurs before the WHERE filter. Evaluate NULL>1 rather
than substituting a numeric zero silently.

9: include the cost of emitting results. Hashing cannot make a genuinely huge
answer free. Skew changes output size as well as bucket work.

10–11: a BEGIN followed by no read has not yet established the read view used in
this example. Distinguish one application operation from each independently
committed statement. A retry must restart the relevant observation boundary.

12: an access path is an algorithmic choice, not a measured duration. Preserve
the exact ordered result before comparing plans or times.

13: start with jobs as the preserved side; count successful attempt IDs only
under an explicit success predicate. Decide whether a NULL outcome counts as
success before writing SQL. [Full solutions](SOLUTIONS.md).
