# Hints

1. Presence is a different question from equality. WHERE accepts exactly true.
2. A real order has a nonnull ID even if its measured amount is unknown.
3. Think of IN as known equality witnesses, then consider whether a missing
   witness suffices to prove nonmembership when unknowns remain.
4. Put the positive predicate in ON and count the nonnull right order ID.
5. A NULL-extended row still exists in the joined result, but has no right ID.
6. Define each result population before running any query. Separate dialect
   behavior from application policy about missing data.
