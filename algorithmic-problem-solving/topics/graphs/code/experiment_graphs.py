"""Synthetic representation/growth investigation; measurements emitted, never guessed."""
import json,platform,sys,time,statistics,math
from graph_algorithms import bfs,dijkstra,bellman_ford,critical_path

def main():
    rows=[]
    for n in [48,96,192,384]:
        for kind in ['chain','dense-dag']:
            g=([[u+1] if u+1<n else [] for u in range(n)] if kind=='chain' else [list(range(u+1,n)) for u in range(n)])
            times=[]
            for _ in range(5):
                start=time.perf_counter();d,_=bfs(g,[0]);times.append(time.perf_counter()-start)
            rows.append(dict(vertices=n,kind=kind,adjacency_entries=sum(map(len,g)),distance_last=d[-1],median_seconds=statistics.median(times),trials_seconds=times))
    print(json.dumps(dict(environment=dict(python=sys.version,platform=platform.platform()),kind='deterministic synthetic graph inputs; elapsed times observed',growth=rows,weighted_counterexample=dict(graph=[[(1,7),(2,2)],[],[(1,1)]],distance=dijkstra([[(1,7),(2,2)],[],[(1,1)]],0)),negative_cycle=[x if math.isfinite(x) else ('-inf' if x<0 else '+inf') for x in bellman_ford([[(1,1)],[(2,-3)],[(1,1)],[]],0)],unlimited_worker_finish=critical_path([[1,2],[3],[3],[]],[2,3,7,1])),indent=2,allow_nan=False))
if __name__=='__main__':main()
