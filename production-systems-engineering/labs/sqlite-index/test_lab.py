from lab import *
def run():
    c=build(1000)
    sql='select * from events where user_id=?'
    before=' '.join(str(x) for row in plan(c,sql,(3,)) for x in row)
    c.execute('create index ix_events_user on events(user_id)')
    after=' '.join(str(x) for row in plan(c,sql,(3,)) for x in row)
    assert 'ix_events_user' in after
    t,res=timed(c,sql,(3,),2); assert all(r[1]==3 for r in res)
    print('sqlite index lab: PASS')
if __name__=='__main__': run()
