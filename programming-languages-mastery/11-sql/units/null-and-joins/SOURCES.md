# SQL primary source verification

Inspected 2026-10-23. The explanations, tables, schema, queries, model functions
and tests are original work. Local output uses Python3.12.14 and SQLite3.53.1;
that version is not inferred from the continuously updated website.

| SQLite/PSF primary source | Inspected scope | Supported claim and boundary |
|---|---|---|
| [SQLite expressions](https://www.sqlite.org/lang_expr.html) | §2 NULL/AND/OR/IS, §4 bound parameters, §8 IN/NOT IN matrix, §10 EXISTS | Three-valued operators, empty sets and existence; explicitly SQLite dialect. |
| [SQLite SELECT](https://www.sqlite.org/lang_select.html) | §2 conceptual processing; §2.1 LEFT extension; §2.3 WHERE; §2.6 DISTINCT | Filter placement and conceptual row pipeline, not a physical optimizer plan. |
| [SQLite aggregates](https://www.sqlite.org/lang_aggfunc.html) | count and sum/total descriptions | Counts of rows/non-NULL and empty-input sums. No newer percentile feature is used. |
| [SQLite NULL handling](https://www.sqlite.org/nulls.html) | NULL comparison tests and nullable UNIQUE/DISTINCT description | Background; historical cross-engine table is not current verification of other engines. |
| [PSF sqlite3](https://docs.python.org/3.12/library/sqlite3.html) | Tutorial parameter binding and connect(':memory:') | Python host interface; not a proof of transaction/concurrency behavior. |

SQLite documentation/source carries its public-domain dedication and item-specific
notices; Python documentation has PSF terms. No substantial source passages/code
are copied or bundled here. Actual experiment/test results are retained separately.
No other database engine, production workload, isolation level or index performance
was independently verified in this unit.
