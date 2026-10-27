"""Original bounded graph mechanisms. See ../LESSON.md and ../PROBLEMS.md.

Vertices are integer IDs 0..n-1; duplicate adjacency entries are rejected.
Weights/capacities are integers, avoiding implicit floating comparison policies.
Algorithms do not mutate caller inputs. Python recursion is used only in the
explicitly bounded low-link/matching references; see their limits below.
"""
from collections import deque
import heapq
import math


def _vertex(v,n):
    if type(v) is not int or not 0 <= v < n:
        raise ValueError('vertex must be an integer in 0..n-1')


def graph(adj, undirected=False):
    g=tuple(tuple(row) for row in adj); n=len(g)
    for row in g:
        for v in row: _vertex(v,n)
    neighbor_sets=[set(row) for row in g]
    for u,row in enumerate(g):
        if len(set(row)) != len(row): raise ValueError('duplicate edge')
        if undirected and (u in row or any(u not in neighbor_sets[v] for v in row)):
            raise ValueError('need simple symmetric undirected adjacency')
    return g


def weighted(adj,nonnegative=False,binary=False):
    g=tuple(tuple(row) for row in adj);n=len(g)
    for row in g:
        seen=set()
        for edge in row:
            if not isinstance(edge,(tuple,list)) or len(edge)!=2:raise ValueError('edge is (vertex,integer weight)')
            v,w=edge;_vertex(v,n)
            if type(w) is not int or (nonnegative and w<0) or (binary and w not in (0,1)):
                raise ValueError('unsupported weight')
            if v in seen: raise ValueError('parallel destinations not represented')
            seen.add(v)
    return g


def bfs(adj,sources):
    g=graph(adj); n=len(g);d=[None]*n;p=[None]*n;q=deque()
    for s in sources:
        _vertex(s,n)
        if d[s] is None:d[s]=0;q.append(s)
    while q:
        u=q.popleft()
        for v in g[u]:
            if d[v] is None:d[v]=d[u]+1;p[v]=u;q.append(v)
    return d,p


def reachable(adj,source):
    g=graph(adj);_vertex(source,len(g));seen={source};stack=[source]
    while stack:
        for v in g[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    return seen


def shortest_path(adj,source,target):
    g=graph(adj);_vertex(target,len(g));d,p=bfs(g,[source])
    if d[target] is None:return None
    result=[target]
    while result[-1]!=source:result.append(p[result[-1]])
    return list(reversed(result))


def multi_source_distances(adj,sources):
    return bfs(adj,sources)[0]


def components(adj):
    g=graph(adj,True);seen=set();result=[]
    for u in range(len(g)):
        if u not in seen:
            component={u};seen.add(u);stack=[u]
            while stack:
                for v in g[stack.pop()]:
                    if v not in seen:seen.add(v);component.add(v);stack.append(v)
            result.append(component)
    return result


def bipartition(adj):
    g=graph(adj,True);colors=[None]*len(g)
    for root in range(len(g)):
        if colors[root] is not None:continue
        colors[root]=0;q=deque([root])
        while q:
            u=q.popleft()
            for v in g[u]:
                if colors[v] is None:colors[v]=1-colors[u];q.append(v)
                elif colors[v]==colors[u]:return None
    return colors


def topological_order(adj):
    g=graph(adj);degree=[0]*len(g)
    for row in g:
        for v in row:degree[v]+=1
    q=deque(i for i,d in enumerate(degree) if d==0);result=[]
    while q:
        u=q.popleft();result.append(u)
        for v in g[u]:
            degree[v]-=1
            if degree[v]==0:q.append(v)
    if len(result)!=len(g):raise ValueError('directed cycle')
    return result


def directed_cycle(adj):
    g=graph(adj);color=[0]*len(g);parent=[None]*len(g)
    for root in range(len(g)):
        if color[root]:continue
        color[root]=1;stack=[(root,iter(g[root]))]
        while stack:
            u,it=stack[-1]
            try:v=next(it)
            except StopIteration:color[u]=2;stack.pop();continue
            if color[v]==0:
                parent[v]=u;color[v]=1;stack.append((v,iter(g[v])))
            elif color[v]==1:
                chain=[u]
                while chain[-1]!=v:chain.append(parent[chain[-1]])
                return list(reversed(chain))+[v]
    return None


def strongly_connected(adj):
    g=graph(adj);seen=set();finish=[]
    for root in range(len(g)):
        if root in seen:continue
        seen.add(root);stack=[(root,iter(g[root]))]
        while stack:
            u,it=stack[-1]
            try:v=next(it)
            except StopIteration:finish.append(u);stack.pop();continue
            if v not in seen:seen.add(v);stack.append((v,iter(g[v])))
    rev=[[] for _ in g]
    for u,row in enumerate(g):
        for v in row:rev[v].append(u)
    seen.clear();result=[]
    for root in reversed(finish):
        if root in seen:continue
        comp=set();stack=[root];seen.add(root)
        while stack:
            u=stack.pop();comp.add(u)
            for v in rev[u]:
                if v not in seen:seen.add(v);stack.append(v)
        result.append(comp)
    return result


def dijkstra(adj,source):
    g=weighted(adj,nonnegative=True);_vertex(source,len(g));d=[math.inf]*len(g);d[source]=0;heap=[(0,source)]
    while heap:
        distance,u=heapq.heappop(heap)
        if distance!=d[u]:continue
        for v,w in g[u]:
            candidate=distance+w
            if candidate<d[v]:d[v]=candidate;heapq.heappush(heap,(candidate,v))
    return d


def bellman_ford(adj,source):
    g=weighted(adj);n=len(g);_vertex(source,n);d=[math.inf]*n;d[source]=0
    # Copies make pass k exactly minimum distance using at most k edges.
    for _ in range(n-1):
        previous=d;d=previous.copy()
        for u,row in enumerate(g):
            for v,w in row:
                if previous[u]!=math.inf:d[v]=min(d[v],previous[u]+w)
        if d==previous:break
    affected=set()
    for u,row in enumerate(g):
        for v,w in row:
            if d[u]!=math.inf and d[u]+w<d[v]:affected.add(v)
    q=deque(affected)
    while q:
        for v,_ in g[q.popleft()]:
            if v not in affected:affected.add(v);q.append(v)
    for v in affected:d[v]=-math.inf
    return d


def zero_one_distances(adj,source):
    g=weighted(adj,binary=True);_vertex(source,len(g));d=[math.inf]*len(g);d[source]=0;q=deque([(0,source)])
    while q:
        distance,u=q.popleft()
        if distance!=d[u]:continue
        for v,w in g[u]:
            if distance+w<d[v]:
                d[v]=distance+w
                (q.appendleft if w==0 else q.append)((d[v],v))
    return d


def dag_path_count(adj,source,target):
    g=graph(adj);_vertex(source,len(g));_vertex(target,len(g));order=topological_order(g);count=[0]*len(g);count[source]=1
    for u in order:
        for v in g[u]:count[v]+=count[u]
    return count[target]


def dag_shortest_paths(adj,source):
    g=weighted(adj);_vertex(source,len(g));order=topological_order([[v for v,_ in row] for row in g]);d=[math.inf]*len(g);d[source]=0
    for u in order:
        if d[u]==math.inf:continue
        for v,w in g[u]:d[v]=min(d[v],d[u]+w)
    return d


def critical_path(adj,durations):
    g=graph(adj);times=tuple(durations)
    if len(times)!=len(g) or any(type(t) is not int or t<0 for t in times):raise ValueError('one nonnegative integer duration per vertex')
    start=[0]*len(g)
    for u in topological_order(g):
        for v in g[u]:start[v]=max(start[v],start[u]+times[u])
    return [start[u]+times[u] for u in range(len(g))]


def _lowlink(adj):
    g=graph(adj,True)
    if len(g)>500:raise ValueError('recursive reference limited to 500 vertices')
    discovery=[-1]*len(g);low=[0]*len(g);clock=0;cuts=set();bridge=[]
    def visit(u,parent):
        nonlocal clock
        discovery[u]=low[u]=clock;clock+=1;children=0
        for v in g[u]:
            if v==parent:continue
            if discovery[v]<0:
                children+=1;visit(v,u);low[u]=min(low[u],low[v])
                if low[v]>discovery[u]:bridge.append(tuple(sorted((u,v))))
                if parent is not None and low[v]>=discovery[u]:cuts.add(u)
            else:low[u]=min(low[u],discovery[v])
        if parent is None and children>1:cuts.add(u)
    for u in range(len(g)):
        if discovery[u]<0:visit(u,None)
    return sorted(bridge),cuts


def bridges(adj):return _lowlink(adj)[0]
def articulation_points(adj):return _lowlink(adj)[1]


def minimum_spanning_forest(n,edges):
    if type(n) is not int or n<0:raise ValueError('n must be nonnegative integer')
    checked=[];seen=set()
    for u,v,w in edges:
        _vertex(u,n);_vertex(v,n)
        if type(w) is not int or u==v:raise ValueError('integer weights, no loops')
        pair=tuple(sorted((u,v)))
        if pair in seen:raise ValueError('parallel undirected edge')
        seen.add(pair);checked.append((w,*pair))
    parent=list(range(n));rank=[0]*n
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    result=[];total=0
    for w,u,v in sorted(checked):
        a,b=find(u),find(v)
        if a==b:continue
        if rank[a]<rank[b]:a,b=b,a
        parent[b]=a
        if rank[a]==rank[b]:rank[a]+=1
        result.append((u,v,w));total+=w
    return total,result


def maximum_flow(capacity,source,sink):
    """Return max value and source-side residual cut; integer dense Edmonds–Karp.

    O(V^3 E) upper bound here includes dense row scans; not sparse O(V E²).
    Caller chooses small locally controlled inputs; no untrusted-size endpoint.
    """
    c=tuple(tuple(row) for row in capacity);n=len(c);_vertex(source,n);_vertex(sink,n)
    if source==sink:raise ValueError('source and sink differ')
    if any(len(row)!=n or any(type(x) is not int or x<0 for x in row) for row in c):raise ValueError('square nonnegative integer capacity matrix')
    residual=[list(row) for row in c];value=0
    while True:
        p=[None]*n;p[source]=source;q=deque([source])
        while q and p[sink] is None:
            u=q.popleft()
            for v,r in enumerate(residual[u]):
                if r>0 and p[v] is None:p[v]=u;q.append(v)
        if p[sink] is None:
            return value,{u for u,x in enumerate(p) if x is not None}
        amount=math.inf;v=sink
        while v!=source:amount=min(amount,residual[p[v]][v]);v=p[v]
        v=sink
        while v!=source:
            u=p[v];residual[u][v]-=amount;residual[v][u]+=amount;v=u
        value+=amount


def bipartite_matching(adj,right_size):
    if type(right_size) is not int or right_size<0:raise ValueError('right_size must be nonnegative integer')
    g=tuple(tuple(row) for row in adj)
    if len(g)>500:raise ValueError('recursive reference limited to 500 left vertices')
    for row in g:
        for v in row:_vertex(v,right_size)
        if len(set(row))!=len(row):raise ValueError('duplicate preference')
    owner=[None]*right_size
    def augment(u,seen):
        for v in g[u]:
            if v in seen:continue
            seen.add(v)
            if owner[v] is None or augment(owner[v],seen):owner[v]=u;return True
        return False
    for u in range(len(g)):augment(u,set())
    return {u:v for v,u in enumerate(owner) if u is not None}


def transitive_closure(adj):
    g=graph(adj);n=len(g);r=[[i==j for j in range(n)] for i in range(n)]
    for u,row in enumerate(g):
        for v in row:r[u][v]=True
    for k in range(n):
        for i in range(n):
            for j in range(n):r[i][j]=r[i][j] or (r[i][k] and r[k][j])
    return r
