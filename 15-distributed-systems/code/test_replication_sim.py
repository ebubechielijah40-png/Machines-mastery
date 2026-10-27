from replication_sim import *
def run():
    r=Replica('a'); ev=('e1','x',1)
    assert r.apply(*ev) is True and r.apply(*ev) is False and r.data['x']==1
    a=Replica('a'); b=Replica('b'); events=[('e1','x',1),('e2','y',2)]
    deliver(a,events); deliver(b,reversed(events)); assert a.data==b.data
    # Arrival-order writes can diverge despite event-ID deduplication.
    a=Replica('a'); b=Replica('b'); conflicts=[('c1','x',1),('c2','x',2)]
    deliver(a,conflicts); deliver(b,reversed(conflicts))
    assert a.data=={'x':2} and b.data=={'x':1}
    print('replication sim: PASS')
if __name__=='__main__': run()
