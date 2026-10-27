"""Controlled child: own synthetic producer or deliberate process-only kill."""
import os
import signal
import sys
from protected_demo import resources,observation

if __name__=='__main__':
    _,_,ledger=resources(sys.argv[1])
    if sys.argv[2]=='append':
        producer=sys.argv[3]
        for seq in range(1,7):ledger.append(observation(seq,25000+seq,producer))
    elif sys.argv[2]=='kill':
        stage=sys.argv[3]
        def fault(actual):
            if stage==actual:os.kill(os.getpid(),signal.SIGKILL)
        ledger.append(observation(1),fault=fault)
    else:raise ValueError('unknown controlled child mode')
