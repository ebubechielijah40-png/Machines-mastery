# Checkable query reasoning

1. Results are NULL,1,0,1,NULL respectively in SQLite. WHERE retains the1 cases.
   A Python None-to-false conversion would incorrectly turn NOT unknown into true.
2. Customer4 has count(o.id)=1,count(o.amount)=0,sumNULL. Cia has0,0,NULL. Replacing
   every missing amount by0 before counting removes the distinction.
3. Without NULL, known nonmembers survive both forms; with an empty right set all
   known keys survive. A nullable left key is not known equal to a blocked NULL
   under ordinary equality, so NOT EXISTS may retain it while nonempty NOT IN
   yields unknown. Decide whether NULL means invalid key, unknown or a match class.
4. `SELECT c.id,count(o.id) FROM customers c LEFT JOIN orders o ON
   o.customer_id=c.id AND o.amount>0 GROUP BY c.id ORDER BY c.id` returns all
   customers and counts actual positive matches. A later WHERE removes rows
   whose only right-side values are NULL/zero instead of retaining their zero count.
5. One customer with no right match gives count(*)=1,count(right.id)=0. A matching
   right row with nullable ID could also be omitted by count(right.id), so require
   a nonnull identifier (here INTEGER PRIMARY KEY) to identify actual orders.
6. An independent implementation should perform pair generation, ON truth test,
   unmatched left extension, WHERE truth test and group accumulation explicitly.
   It need not mimic SQLite's physical plan; agreement checks chosen semantics on
   bounded datasets. Null key policy and performance remain separate questions.
