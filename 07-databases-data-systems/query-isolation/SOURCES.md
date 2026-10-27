# Inspected primary source scopes

Inspected2026-10-23. Original prose, code, numeric fixtures, correctness arguments,
exercises and local experiments are supplied here. No vendor prose, figures or
sample databases are reproduced. Live documentation is version-sensitive; local
SQLite/Python versions are recorded with the experiment. General SQL portability
is not inferred from one engine.

| ID | Source | Sections inspected / claim scope |
| --- | --- | --- |
| S1 | [SQLite SELECT](https://www.sqlite.org/lang_select.html) | §2.1 pairings, §2.3 WHERE/outer filter, §2.4 grouping, §2.6 DISTINCT and §4 ordering; result semantics, not physical execution order |
| S2 | [SQLite expressions](https://www.sqlite.org/lang_expr.html) | §2 NULL operators, §8 IN/NOT IN truth matrix, §10 EXISTS |
| S3 | [SQLite aggregate functions](https://www.sqlite.org/lang_aggfunc.html) | count,avg,sum descriptions; NULL/numeric aggregate behavior; no percentile/version-feature claims used |
| S4 | [SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) | §1 diagnostic-format warning; §1.1 scan/search/index and nested scans |
| S5 | [Isolation in SQLite](https://www.sqlite.org/isolation.html) | Separate connections, WAL snapshots, stale upgrade, BEGIN IMMEDIATE and same-connection caveats |
| S6 | [SQLite CREATE TABLE](https://www.sqlite.org/lang_createtable.html) | §3.7 CHECK and §3.8 NOT NULL, plus declared key/constraint vocabulary |
| S7 | [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) | §1 relationship semantics and §2 explicitly enabling/checking per connection |

The pure Python hash/nested operators are original narrow models, not SQLite
source reconstructions. Their complexity/correctness statements follow from the
shown loops and declared hashing assumption. Test comparisons and actual schedules
supply implementation evidence independently of documentation inspection. No
crash durability, power-loss simulation, production timing or formal engine
verification is claimed.
