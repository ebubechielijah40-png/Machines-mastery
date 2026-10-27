# Query meaning, physical work and overlapping transactions

A recoverable file answers "which bytes survive a restart?" It does not answer
"what does this join mean?" or "which transaction may observe this change?"
This unit adds those two boundaries after [the transactional-log build](../../projects-guided/p07-storage-engine/README.md).
It supplies original bag operators, independently checked SQL examples, real
SQLite connection schedules and actual query-plan evidence. It does not replace
the log project or pretend that a Python hash join is SQLite's query executor.

## Entry bridge

Use [sets, logic and proof](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
[functions](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md), Python
lists/tuples, dictionaries and iteration. A row is a tuple of attributes; a schema
assigns their names and intended domains. This lab uses finite synthetic numbers,
strings and None. It has no physical units or sensor-measurement claim.
Python3.10+ with standard-library sqlite3 is sufficient; the actual environment
is recorded in [raw results](evidence/results.json). Use a writable local
filesystem for WAL; an in-memory database cannot substitute for this WAL schedule.

## 1. Selection and projection: meaning before access path

Consider readings `(device,value)`:

| Row | device | value |
| --- | --- | ---: |
| r1 | A |2 |
| r2 | A |NULL |
| r3 | A |4 |
| r4 | B |NULL |
| r5 |NULL |9 |

Selection keeps rows satisfying a predicate; projection chooses attributes.
In set relational algebra, a relation contains no duplicate tuples. SQL commonly
uses **bags**: selecting only device produces A,A,A,B,NULL unless DISTINCT is
requested. Our `project` deliberately preserves every occurrence; `distinct`
removes duplicate output tuples, including one shared NULL bucket. Ordering
without an ORDER BY clause is not a result contract. Tests compare bags using
multiplicity counts, not an incidental loop order. [S1,§2/4]

For this example:

```sql
SELECT device FROM reading WHERE device='A';
SELECT DISTINCT device FROM reading;
SELECT device,COUNT(*),COUNT(value),SUM(value),AVG(value)
FROM reading GROUP BY device;
```

The first query returns three A rows; DISTINCT gives three categories A,B,NULL.
For A, row count is3, non-NULL-value count2, sum6 and mean3. For B, count(*)=1,
count(value)=0 and sum/mean are NULL. Assigning an absent measurement the numeric
value0 changes the mean to2 for A. That is a modeling decision, not a harmless
storage conversion. For no input rows, grouped output has no groups; a global
aggregate has its separately specified single output row. [S1,§2.4;S3]

`grouped_numeric` stores one count and list of numeric values per grouping key.
It is a clear learning implementation, not a memory-efficient streaming
aggregator. An alternative can retain count/sum only when the aggregate permits
it. Floating summation remains approximate; this lab makes no extreme-range
accuracy claim.

## 2. Why SQL needs a third logical value

NULL represents an absent/unknown value in these examples. `NULL=NULL` is NULL,
not true. An equality to an unknown value cannot establish equality. WHERE
keeps only true, so both false and unknown remove the row. `IS NULL` tests the
missing-value marker directly. [S1,§2.3;S2,§2]

Use U for unknown. The implementation's three-valued operators follow:

| a | b | a AND b | a OR b |
| --- | --- | --- | --- |
| T | T | T | T |
| T | F | F | T |
| T | U | U | T |
| F | F | F | F |
| F | U | F | U |
| U | U | U | U |

The remaining rows follow symmetry; NOT U=U. False AND unknown is false because
no possible resolution of the unknown makes both operands true. True OR unknown
is true for the same reason. The tests exhaust all nine binary input pairs
against real SQLite. Python's `bool(None)` and short-circuit operators are not
an implementation of this algebra. Our select function insists on exactly
True/False/None so accidental numeric truthiness is visible.

A dangerous anti-join shortcut is `5 NOT IN (1,NULL)`: 5=1 is false, but its
comparison with NULL is unknown, so membership remains unknown and negation
remains unknown. A WHERE clause drops it. `NOT EXISTS` with an explicit equality
asks a different question: whether any row definitely matches. State what the
application should do with missing keys before choosing either form. [S2,§8/10]

## 3. Joins derive from pairings, including duplicates

Let left contain `(1,'a'),(1,'b'),(NULL,'unknown')` and right contain
`(1,2),(1,3),(1,4),(NULL,9)`. A nested equijoin enumerates3×4=12 pairs, keeping
only pairs whose key equality is true. The two key1 rows pair with each of three
key1 rows, producing six outputs. NULL does not match NULL under `=`. Returning
only one payload per key loses five valid outputs.

Our [nested_join](relations.py) is the direct specification. Every qualifying
pair is appended exactly once: soundness follows from its equality check;
completeness follows because both loops enumerate every pair. No matching
pair can be skipped, and there is one loop visit per occurrence pair.

The hash variant builds key→**list of right rows**, excluding NULL keys. For
each left row it appends every row in that key's bucket. Under the declared
comparison domain, a qualifying right row is in exactly that bucket, so the
same soundness/completeness argument applies. The tests compare both against
SQLite on30 fixed-seed small random bags with duplicates and missing keys.
Our Python equality does not reproduce SQL affinity/collation conversion;
differential fixtures use homogeneous integer keys. No parser, full optimizer,
outer hash join or general SQL conformance is supplied.

For n left and m right rows, nested checks are exactly nm, plus output work.
Expected hash work is O(n+m+k) with ordinary hash behavior and k output rows;
right-side storage is O(m), output storage O(k). If all keys match, k=nm and
no algorithm that materializes every result can avoid that output cost. A
hash table's expected lookup cost is an assumption, not a worst-case guarantee.
The teaching input limit5000 rows per side still permits large outputs; this
is not a public resource-isolated service.

Outer joins add an unmatched row with missing right attributes. Moving a
right-side filter from ON to WHERE can delete it. With devices1,2 and a single
reading(1,2):

```sql
SELECT d.id,r.v FROM d LEFT JOIN r
  ON d.id=r.device AND r.v>1 ORDER BY d.id;
SELECT d.id,r.v FROM d LEFT JOIN r
  ON d.id=r.device WHERE r.v>1 ORDER BY d.id;
```

The first preserves `(2,NULL)`; the second drops it because NULL>1 is unknown.
This counterexample is executed in the tests. [S1,§2.3]

## 4. One logical query can admit different physical work

The [plan experiment](experiment.py) creates1000 rows with100 device IDs and
queries device7. The predicate selects10 rows. An index stores an alternate
lookup structure maintained as data changes; it does not alter the predicate.
The run records a scan before index creation and an indexed search afterward,
with identical ordered results. These are actual plans on the recorded SQLite
version, not promises about every dataset or release. [S4,§1.1]

A simple reasoning model helps an optimizer choose: estimated scan work is n
row visits; an access path may require a lookup plus the selected rows; a join
estimate needs key multiplicities. Guessing every value is equally frequent
can badly underestimate a hot key's output. Estimates are not measurements.
SQLite's inspected documentation describes its joins as nested scans; our hash
operator is a separate educational alternative. We do not claim the plan here
switches SQLite to our Python hash algorithm. [S4,§1.1]

Inspect diagnostic EXPLAIN output by eye, preserve the correctness result, and
benchmark separately if timing is the research question. Its text format can
change across releases. A plan saying SEARCH does not establish a speedup.
The existing [timing lab](../../production-systems-engineering/labs/sqlite-index/README.md)
is the next controlled measurement stage.

## 5. Transactions are schedules over observations and updates

A transaction groups an intended multi-statement operation. Consider moving10
units from account1 to account2, initially100 each. The desired invariant is a
total200 and nonnegative balances. Debiting and crediting as separate externally
visible commits can expose a temporary total190. Atomic visibility and correct
application logic must both hold. A transaction can atomically store the wrong
amount, so declaring BEGIN/COMMIT does not prove the invariant.

[The executed schedule](experiment.py) uses two separate connections A/B,
WAL mode and explicit statements with Python autocommit between transactions:

| Event | A observes/does | B observes/does |
| --- | --- | --- |
|1 | BEGIN; SELECT establishes(100,100) snapshot | idle |
|2 | reads(100,100) | BEGIN IMMEDIATE; debit/credit10 |
|3 | still reads(100,100) | COMMIT(90,110) |
|4 | same snapshot reads(100,100); write upgrade fails | idle |
|5 | ROLLBACK; new read sees(90,110) | idle |

The local run reports SQLITE_BUSY_SNAPSHOT for the stale read-to-write upgrade.
Starting a fresh transaction is required; blindly retrying the same stale
transaction is not recovery. A separate BEGIN IMMEDIATE reservation causes a
second writer's immediate attempt to fail busy with timeout0. This observed
local schedule agrees with the inspected SQLite WAL/single-writer behavior;
it is not a general proof for other engines or isolation configurations. [S5]

A different failure is **application stale read/replace**: A reads100, B reads100,
A writes90, B writes80, each as a separate autocommit statement. The result80
loses A's debit; combining both intended debits would yield70. This does not
contradict SQL serializability because the application split each logical
operation across independent transactions. Relative updates
`SET balance=balance-?` produce70 in the tested schedule. More complex checks
still need an appropriate transaction/retry protocol.

Constraints supply another boundary. The test schema separately declares a
key, NOT NULL, foreign key and nonnegative CHECK; foreign-key enforcement is
explicitly enabled per connection. A NULL value can satisfy SQLite's CHECK
without satisfying NOT NULL, so these are not interchangeable. Failed business
rules need a declared rollback path. Tests execute rejection and rollback cases.
[S6,§3.7/3.8;S7,§2]

## 6. Build, test and assess

From repository root:

```sh
python3 -m unittest discover -s 07-databases-data-systems/query-isolation -v
python3 07-databases-data-systems/query-isolation/experiment.py
```

Attempt [exercises](EXERCISES.md) before [hints](HINTS.md) and
[solutions](SOLUTIONS.md). Rebuild selection, bag projection, both joins and the
snapshot schedule from blank files. Deliver a hand trace, independent tests,
actual JSON, an application invariant and a failed/repair schedule. Rubric:
semantics25%, correctness argument25%, implementation/tests20%, experimental
evidence/limits20%, reconstruction10%.

The [experiment record](EXPERIMENTS.md) distinguishes operation counts, query
plans and connection observations. [Source scopes](SOURCES.md) identify exact
vendor pages inspected. Local runs do not prove crash durability, distributed
consensus, storage correctness on power loss, production performance or complete
relational/database education. B-trees/pages, cost models, full isolation-anomaly
families and pipelines still require further instruction/builds.
