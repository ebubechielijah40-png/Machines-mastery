"""Trusted test child; kill only this directly created process at named hooks."""
import os
import signal
import sys
from store import Store
from stream import consume


if __name__=='__main__':
    directory,action,target=sys.argv[1:]
    def phase(stage):
        if stage==target:os.kill(os.getpid(),signal.SIGKILL)
    store=Store(directory)
    if action=='checkpoint':store.checkpoint(collect=True,phase=phase)
    elif action=='commit':store.commit([('put',1,'new'),('put',2,'new')],phase=phase)
    elif action=='consume':consume(store,'source-A',[(1,0,4),(2,1,7),(3,0,-1)],phase=phase)
    else:raise ValueError('unknown controlled child action')
