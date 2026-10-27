# SQL relation state and NULL-extended rows

A SQL row model and a storage-engine page layout answer different questions.
This developed [join/aggregation lesson](units/null-and-joins/README.md) follows
logical rows; B-trees, buffer pools, WAL and physical query execution remain
separate uncompleted topics here.

LEFT JOIN first identifies matches under ON, then conceptually adds a NULL right
row for an unmatched left row. WHERE is applied after that extension. Moving a
right-side positive-amount predicate from ON to WHERE can remove the unmatched
customer because NULL>0 is unknown. [The lab](units/null-and-joins/lab.py) holds
tables fixed and changes only predicate placement; its retained output changes
from three customer rows to one. The documentation explicitly separates logical
processing explanation from the optimizer's physical execution plan.

COUNT(*) counts joined rows, including an extension row. COUNT(right.id) counts
actual matches only when the right identifier is guaranteed nonnull. COUNT(amount)
counts known measurements; SUM(amount) returns NULL without nonnull input. Draw
one customer with no order and one with an unknown order amount to derive these
counts before seeing [the solutions](units/null-and-joins/SOLUTIONS.md).
Transaction isolation, persistence and concurrent clients cannot be inferred from
this in-memory single-connection semantic experiment.
