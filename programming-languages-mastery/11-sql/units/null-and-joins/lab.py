"""Controlled SQLite NULL and relational-pipeline experiments, entirely in memory."""
from contextlib import closing
import itertools,json,platform,sqlite3,sys

SCHEMA="""
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, amount INTEGER);
CREATE TABLE blocked(customer_id INTEGER);
CREATE TABLE notes(text TEXT NOT NULL);
CREATE TABLE unique_values(value INTEGER UNIQUE);
"""
QUERIES={
 'equals_null':'SELECT id FROM orders WHERE amount=NULL ORDER BY id',
 'is_null':'SELECT id FROM orders WHERE amount IS NULL ORDER BY id',
 'not_in':'SELECT id FROM customers WHERE id NOT IN (SELECT customer_id FROM blocked) ORDER BY id',
 'not_exists':'SELECT c.id FROM customers c WHERE NOT EXISTS (SELECT 1 FROM blocked b WHERE b.customer_id=c.id) ORDER BY c.id',
 'left_filter_on':'SELECT c.id,o.id,o.amount FROM customers c LEFT JOIN orders o ON o.customer_id=c.id AND o.amount>0 ORDER BY c.id,o.id',
 'left_filter_where':'SELECT c.id,o.id,o.amount FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.amount>0 ORDER BY c.id,o.id',
 'counts':'SELECT c.id,count(*),count(o.id),count(o.amount),sum(o.amount) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id GROUP BY c.id ORDER BY c.id',
 'empty_aggregate':'SELECT count(*),count(amount),sum(amount),total(amount) FROM orders WHERE 0',
 'distinct_nulls':'SELECT DISTINCT value FROM unique_values ORDER BY value',
 'empty_not_in':'SELECT NULL NOT IN (SELECT customer_id FROM blocked WHERE 0)',
}

def database():
    db=sqlite3.connect(':memory:');db.executescript(SCHEMA)
    db.executemany('INSERT INTO customers VALUES (?,?)',[(1,'Ada'),(2,'Ben'),(3,'Cia')])
    db.executemany('INSERT INTO orders VALUES (?,?,?)',[(10,1,5),(11,1,None),(12,2,0)])
    db.executemany('INSERT INTO blocked VALUES (?)',[(2,),(None,)])
    db.executemany('INSERT INTO unique_values VALUES (?)',[(None,),(None,),(1,)])
    return db

def truth_rows(db):
    return [{'a':a,'b':b,'and':db.execute('SELECT ? AND ?',(a,b)).fetchone()[0],
             'or':db.execute('SELECT ? OR ?',(a,b)).fetchone()[0],
             'not_a':db.execute('SELECT NOT ?',(a,)).fetchone()[0]}
            for a,b in itertools.product((0,1,None),repeat=2)]

def observe():
    with closing(database()) as db:
        rows={name:db.execute(query).fetchall() for name,query in QUERIES.items()}
        payload="x'); DROP TABLE customers;--"
        db.execute('INSERT INTO notes(text) VALUES (?)',(payload,))
        rows['bound_data']=db.execute('SELECT text FROM notes').fetchall()
        rows['customers_after_bind']=db.execute('SELECT count(*) FROM customers').fetchone()[0]
        try:db.execute('INSERT INTO unique_values VALUES (1)')
        except sqlite3.IntegrityError:rows['duplicate_nonnull_rejected']=True
        else:rows['duplicate_nonnull_rejected']=False
        return {'environment':{'python':sys.version,'platform':platform.platform(),'sqlite_runtime':sqlite3.sqlite_version},'synthetic_inputs':{'customers':[[1,'Ada'],[2,'Ben'],[3,'Cia']],'orders':[[10,1,5],[11,1,None],[12,2,0]],'blocked':[2,None]},'truth':truth_rows(db),'observations':rows,'scope':'SQLite in-memory semantic lab, not cross-engine or production transaction verification'}

if __name__=='__main__':print(json.dumps(observe(),indent=2))
