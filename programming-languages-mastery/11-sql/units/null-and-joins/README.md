# SQL: unknown values, relational filtering and outer joins

A query can run successfully and still answer the wrong question. This unit
reconstructs why NULL comparison, anti-joins, aggregation and outer-join filters
produce surprising results. It uses SQLite through Python's standard library,
with entirely synthetic in-memory tables. No server, credentials or external data
are required. Prerequisites: [sets, logic and functions](../../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
the ability to read a row table. The SELECT/FROM/WHERE slice below introduces
the query notation used here. [SOURCES](SOURCES.md)
records verified SQLite semantics and the exact local dialect boundary.

## Read a query as a row transformation

A table contains rows with named columns. `SELECT id FROM customers WHERE id>1`
means consider rows from customers, keep those for which id>1 is true, and return
their id column. `SELECT *` returns all columns; it does not mean remove duplicate
rows. `AS c` or a trailing `c` gives a table a short alias, so `c.id` selects its
id column. `ORDER BY c.id` makes the requested result ordering explicit. Without
that clause, an incidental row order is not a portable result guarantee.

`INSERT INTO notes(text) VALUES (?)` adds one row; the Python API binds the
question-mark placeholder to a separate value. It does not paste that value
into SQL syntax. A join combines related rows, while a group aggregate summarizes
the resulting row population. The following worked cases derive those operations
before interpreting their unknown-value boundaries. This is a query subset,
not a complete SQL syntax, schema or transaction course.

## A missing measurement is not a zero measurement

Store customers `(1,Ada),(2,Ben),(3,Cia)` and orders
`(10,1,5),(11,1,NULL),(12,2,0)`, with columns `(order_id,customer_id,amount)`.
Order11 exists but its amount is missing; order12 has a known zero; Cia has no
order at all. Collapsing those states into0 loses information needed for billing,
measurement uncertainty and data quality. NULL is a SQL marker whose behavior
is defined by each operator, not a hidden ordinary numeric value.

For an ordinary equality comparison, `NULL=5` and `NULL=NULL` yield unknown,
represented as SQL NULL. Equality cannot establish whether two unknown amounts
are equal. `amount=NULL` therefore selects no orders: WHERE retains only true,
not false or unknown. `amount IS NULL` asks a different presence question and
selects order11. In SQLite the more general `IS` comparison has dialect-specific
forms; use the explicit NULL-presence predicate here and check other engines.

Three-valued Boolean logic extends reasoning about uncertainty. False AND unknown
is false, because no completion can make both operands true. True OR unknown is
true, because no completion can make both false. True AND unknown, false OR
unknown and NOT unknown stay unknown. This derives the truth table rather than
trying to force unknown into a two-valued Python truth test.

| a | b | a AND b | a OR b |
|---|---|---|---|
| false | false | false | false |
| false | true | false | true |
| false | unknown | false | unknown |
| true | false | false | true |
| true | true | true | true |
| true | unknown | unknown | true |
| unknown | false | false | unknown |
| unknown | true | unknown | true |
| unknown | unknown | unknown | unknown |

## Anti-joins need a declared unknown policy

Suppose blocked contains customer2 and a NULL customer ID. For customer1,
`1 NOT IN (2,NULL)` means the relevant comparisons cannot establish nonmembership:
1 differs from2, but comparison with the unknown entry is unknown. NOT preserves
that unknown. WHERE excludes it. Customer2 is excluded as a known member, and
customer3 is also unknown, leaving no customers.

If the requirement is "customers for whom no known equal blocked ID exists", use:

```sql
SELECT c.id
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1 FROM blocked AS b WHERE b.customer_id=c.id
)
ORDER BY c.id;
```

For customer1 or3 no equality is true, so the subquery returns no matching row;
NOT EXISTS is true and returns1,3. This is the selected semantics for nonnull
customer keys, not a universal equivalence between NOT IN and NOT EXISTS.
A NULL left key would need an explicitly chosen policy. The test enumerates64
three-entry blocked lists over1,2,3,NULL and compares against a nonnull set
nonmembership definition. An empty right-hand set is another boundary: in SQLite,
NULL NOT IN that empty set is true. Guessing from the nonempty unknown case fails.

## Follow the relational stages by hand

A LEFT JOIN first decides which right rows match the ON predicate. For each
left row with no match, it adds one result containing NULL right columns. A
WHERE predicate is then applied to this conceptual joined result. This explains
semantics; the optimizer may physically execute a different equivalent plan.

```sql
SELECT c.id,o.id,o.amount
FROM customers c LEFT JOIN orders o
  ON o.customer_id=c.id AND o.amount>0
ORDER BY c.id,o.id;
```

Ada matches order10. Order11's unknown amount does not satisfy >0. Ben's zero
amount also does not match, so Ben receives one NULL-extended row. Cia has no
candidate and receives one too. Output is `(1,10,5),(2,NULL,NULL),(3,NULL,NULL)`.

Move `o.amount>0` from ON to WHERE after joining on ID alone: Ada's known positive
row survives, order11 is unknown and excluded, Ben's zero is false and excluded,
Cia's NULL-extended amount is unknown and excluded. Only `(1,10,5)` remains.
A LEFT JOIN keyword alone does not promise preservation after a rejecting WHERE.
The change answers a different question, not merely a syntactic preference.

## Aggregates count different populations

On the ID-only left join, group by customer ID. `COUNT(*)` counts joined rows,
including a NULL-extended row. `COUNT(o.id)` counts actual matching orders, because
order IDs are nonnull. `COUNT(o.amount)` counts measured amounts. `SUM(o.amount)`
adds known amounts and returns NULL if no nonnull input exists.

| Customer | COUNT(*) | COUNT(o.id) | COUNT(o.amount) | SUM(o.amount) |
|---|---:|---:|---:|---:|
| Ada | 2 | 2 | 1 | 5 |
| Ben | 1 | 1 | 1 | 0 |
| Cia | 1 | 0 | 0 | NULL |

This is why counting all rows overstates Cia's order count. COALESCE(sum,0) can
be a deliberate presentation policy, but should not erase the distinction between
no measured input and an actual zero. On no input rows, SQLite returns count0,
sumNULL and its dialect-specific total0.0. DISTINCT treats NULLs as one duplicate
class, while a nullable UNIQUE column accepts more than one NULL in this tested
SQLite behavior. "NULL never equals anything" alone cannot derive every operator.

## Bind data across the language boundary

`db.execute('INSERT INTO notes(text) VALUES (?)',(value,))` sends SQL structure
separately from a bound value. The experiment stores the literal string
`x'); DROP TABLE customers;--` as one note and confirms all three customers remain.
It never executes a destructive concatenated variant. Quoting or shell escaping
is not SQL parameter binding. Placeholders represent values, not arbitrary table
or column identifiers; dynamic identifiers need a separate restricted design.

## Execute and investigate

```sh
python3 -m unittest discover -s programming-languages-mastery/11-sql/units/null-and-joins -v
python3 programming-languages-mastery/11-sql/units/null-and-joins/lab.py
```

[tests.txt](tests.txt) records seven passing methods, including all nine Boolean
pairs and64 anti-join datasets. [observed.json](observed.json) records actual
Python3.12.14/SQLite3.53.1, inputs, truth table and outputs above. Hypothesis:
changing filter placement or unknown policy changes preserved rows despite the
same original data. Controls: tables/connection/dialect; independent variables:
predicate/operator location; measured outcome: exact ordered result rows. This
is semantic evidence, not latency, index or production transaction benchmarking.

The known-input truth model and row-by-row derivations independently explain the
observations. Alternative engines/types/collations may differ, and mistaken input
meaning can defeat a correct query. Next add an all-NULL amount group, duplicate
orders and a NULL left key with a written desired policy. Use EXPLAIN QUERY PLAN
and larger synthetic cardinalities for a separate performance experiment; never
infer physical nested-loop execution from the conceptual join explanation alone.

Attempt [EXERCISES](EXERCISES.md), then [HINTS](HINTS.md) and [SOLUTIONS](SOLUTIONS.md).
Transactions, schemas/migrations, query engine internals and distributed databases
remain outside this developed SQL-semantics unit.
