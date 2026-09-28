import sqlite3, random, time

def build(n=10000,seed=1):
    con=sqlite3.connect(':memory:'); con.execute('create table events(id integer primary key, user_id integer, kind text, value real)')
    rng=random.Random(seed); kinds=['view','click','buy']
    con.executemany('insert into events(user_id,kind,value) values(?,?,?)',((rng.randrange(max(1,n//100)),rng.choice(kinds),rng.random()) for _ in range(n)))
    con.commit(); return con

def plan(con,sql,args=()): return list(con.execute('explain query plan '+sql,args))
def timed(con,sql,args=(),repeat=5):
    times=[]; result=None
    for _ in range(repeat):
        t=time.perf_counter(); result=list(con.execute(sql,args)); times.append(time.perf_counter()-t)
    return min(times),result
