# SQL NULL is an operator-dependent marker

The developed [NULL and joins unit](units/null-and-joins/README.md) teaches a
bounded SQLite semantics slice with seven passing suites and actual rows. It
does not complete SQL types/affinity/coercion across engines.

A known zero amount, an order with an unknown amount and no matching order are
three different states. Ordinary equality with NULL yields unknown; a WHERE
predicate accepts only true. Thus amount=NULL retains no row, while amount IS
NULL identifies the missing amount. False AND unknown is false; true OR unknown
is true; NOT unknown remains unknown. [The independent truth model](units/null-and-joins/test_lab.py)
checks all nine operand pairs against SQLite.

NOT IN with a NULL right entry can reject every apparent nonmember through unknown
results. NOT EXISTS with an explicit equality predicate expresses the chosen policy
of no known matching ID for nonnull keys. A nullable left key requires an additional
application policy. DISTINCT and nullable UNIQUE also treat NULL according to their
own rules, not a slogan about equality. The unit's actual SQLite3.53.1 output and
inspected primary docs are linked separately. Rebuild the truth table and derive
one anti-join result before running the engine.
