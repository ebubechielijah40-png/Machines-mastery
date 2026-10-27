"""Independent bounded oracles: enumerate paths, cuts, trees and assignments."""
import itertools
import math
import unittest
import graph_algorithms as a


def directed(n,mask):
    g=[[] for _ in range(n)];pairs=[(u,v) for u in range(n) for v in range(n) if u!=v]
    for i,(u,v) in enumerate(pairs):
        if mask>>i&1:g[u].append(v)
    return g


def paths(g,s,t,seen=None):
    seen={s} if seen is None else seen
    if s==t:yield [s]
    for v in g[s]:
        if v not in seen:
            for tail in paths(g,v,t,seen|{v}):yield [s]+tail


def weight_oracle(g,s):
    n=len(g);d=[[math.inf]*n for _ in range(n)]
    for u in range(n):d[u][u]=0
    for u,row in enumerate(g):
        for v,w in row:d[u][v]=min(d[u][v],w)
    for k in range(n):
        for u in range(n):
            for v in range(n):d[u][v]=min(d[u][v],d[u][k]+d[k][v])
    return [-math.inf if any(d[s][k]<math.inf and d[k][k]<0 and d[k][v]<math.inf for k in range(n)) else d[s][v] for v in range(n)]


def ug(n,edges):
    g=[[] for _ in range(n)]
    for u,v in edges:g[u].append(v);g[v].append(u)
    return g


def component_count_without(n,edges,removed_vertex=None,removed_edge=None):
    # Partition refinement, no DFS/low-link code from implementation.
    groups=[{v} for v in range(n) if v!=removed_vertex]
    for edge in edges:
        u,v=edge
        if removed_vertex in edge or edge==removed_edge:continue
        i=next(i for i,c in enumerate(groups) if u in c)
        j=next(i for i,c in enumerate(groups) if v in c)
        if i!=j:
            groups[i]|=groups[j];groups.pop(j)
    return len(groups)


class GraphTests(unittest.TestCase):
    def test_reachability_shortest_closure_all_four_vertex_digraphs(self):
        for mask in range(1<<12):
            g=directed(4,mask);closure=a.transitive_closure(g)
            for s in range(4):
                reached=a.reachable(g,s)
                for t in range(4):
                    candidates=list(paths(g,s,t));length=min((len(p) for p in candidates),default=None)
                    got=a.shortest_path(g,s,t)
                    self.assertEqual(got is None,length is None)
                    if got is not None:self.assertEqual(len(got),length);self.assertIn(got,candidates)
                    self.assertEqual(t in reached,bool(candidates));self.assertEqual(closure[s][t],bool(candidates))

    def test_multi_source_is_minimum_over_sources_and_empty_sources(self):
        g=[[1],[2],[3],[]]
        self.assertEqual(a.multi_source_distances(g,[0,2,2]),[0,1,0,1])
        self.assertEqual(a.multi_source_distances(g,[]),[None]*4)
        for mask in range(64):
            g=directed(3,mask)
            for sources in [[],[0],[0,2]]:
                oracle=[]
                for t in range(3):
                    lengths=[len(p)-1 for s in sources for p in paths(g,s,t)]
                    oracle.append(min(lengths) if lengths else None)
                self.assertEqual(a.multi_source_distances(g,sources),oracle)

    def test_components_bipartition_and_cut_vertices_exhaustive(self):
        n=5;pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[e for i,e in enumerate(pairs) if mask>>i&1];g=ug(n,edges)
            baseline=component_count_without(n,edges)
            self.assertEqual(len(a.components(g)),baseline)
            got=a.bipartition(g)
            candidates=[c for c in itertools.product([0,1],repeat=n) if all(c[u]!=c[v] for u,v in edges)]
            self.assertEqual(got is None,not candidates)
            if got is not None:self.assertIn(tuple(got),candidates)
            self.assertEqual(a.bridges(g),[e for e in edges if component_count_without(n,edges,removed_edge=e)>baseline])
            self.assertEqual(a.articulation_points(g),{v for v in range(n) if component_count_without(n,edges,removed_vertex=v)>baseline})

    def test_topology_cycle_witness_and_scc_exhaustive(self):
        for mask in range(1<<12):
            g=directed(4,mask)
            orders=[p for p in itertools.permutations(range(4)) if all(p.index(u)<p.index(v) for u,row in enumerate(g) for v in row)]
            cycle=a.directed_cycle(g)
            if orders:self.assertIn(tuple(a.topological_order(g)),orders);self.assertIsNone(cycle)
            else:
                with self.assertRaises(ValueError):a.topological_order(g)
                self.assertEqual(cycle[0],cycle[-1]);self.assertTrue(all(v in g[u] for u,v in zip(cycle,cycle[1:])))
                self.assertEqual(len(cycle)-1,len(set(cycle[:-1])))
            comps=a.strongly_connected(g)
            self.assertEqual(set.union(set(),*comps),set(range(4)))
            self.assertEqual(sum(map(len,comps)),4)
            for u in range(4):
                for v in range(4):
                    mutual=bool(list(paths(g,u,v))) and bool(list(paths(g,v,u)))
                    self.assertEqual(any(u in c and v in c for c in comps),mutual)

    def test_weighted_algorithms_independent_floyd_warshall(self):
        pairs=[(u,v) for u in range(3) for v in range(3) if u!=v]
        for choices in itertools.product([None,-1,0,2],repeat=6):
            g=[[] for _ in range(3)]
            for (u,v),w in zip(pairs,choices):
                if w is not None:g[u].append((v,w))
            self.assertEqual(a.bellman_ford(g,0),weight_oracle(g,0))
            if all(w is None or w>=0 for w in choices):self.assertEqual(a.dijkstra(g,0),weight_oracle(g,0))
        for choices in itertools.product([None,0,1],repeat=6):
            g=[[] for _ in range(3)]
            for (u,v),w in zip(pairs,choices):
                if w is not None:g[u].append((v,w))
            self.assertEqual(a.zero_one_distances(g,0),weight_oracle(g,0))

    def test_dag_count_weighted_paths_and_job_schedule(self):
        g=[[1,2],[3],[3],[]]
        self.assertEqual(a.dag_path_count(g,0,3),2)
        self.assertEqual(a.dag_path_count(g,2,2),1)
        self.assertEqual(a.critical_path(g,[2,3,7,1]),[2,5,9,10])
        w=[[(1,3),(2,1)],[(3,-5)],[(3,2)],[]]
        self.assertEqual(a.dag_shortest_paths(w,0),[0,3,1,-2])
        for mask in range(64):
            # Only increasing endpoints => acyclic by construction.
            edges=[e for i,e in enumerate(itertools.combinations(range(4),2)) if mask>>i&1]
            g=[[] for _ in range(4)]
            for u,v in edges:g[u].append(v)
            self.assertEqual(a.dag_path_count(g,0,3),len(list(paths(g,0,3))))
            times=[1,2,3,4];ends=a.critical_path(g,times)
            for t in range(4):
                oracle=max(sum(times[v] for v in p) for s in range(4) for p in paths(g,s,t))
                self.assertEqual(ends[t],oracle)

    def test_minimum_spanning_tree_exhaustive_subsets(self):
        pairs=list(itertools.combinations(range(4),2))
        for weights in itertools.product([-1,0,2],repeat=6):
            edges=[(*e,w) for e,w in zip(pairs,weights)]
            candidates=[]
            for subset in itertools.combinations(edges,3):
                if component_count_without(4,[(u,v) for u,v,w in subset])==1:candidates.append(sum(w for u,v,w in subset))
            cost,chosen=a.minimum_spanning_forest(4,edges)
            self.assertEqual(cost,min(candidates));self.assertEqual(len(chosen),3)
        self.assertEqual(a.minimum_spanning_forest(3,[(0,1,2)])[0],2)

    def test_flow_equals_enumerated_cut_and_reported_cut_capacity(self):
        pairs=[(u,v) for u in range(4) for v in range(4) if u!=v]
        for mask in range(1<<12):
            c=[[0]*4 for _ in range(4)]
            for i,(u,v) in enumerate(pairs):c[u][v]=(mask>>i)&1
            cuts=[{0}|{v for i,v in enumerate([1,2]) if bits>>i&1} for bits in range(4)]
            capacity=lambda cut:sum(c[u][v] for u in cut for v in range(4) if v not in cut)
            value,cut=a.maximum_flow(c,0,3)
            self.assertEqual(value,min(map(capacity,cuts)));self.assertEqual(value,capacity(cut))
            self.assertIn(0,cut);self.assertNotIn(3,cut)

    def test_matching_exhaustive_assignment_oracle(self):
        for mask in range(512):
            g=[[v for v in range(3) if mask>>(u*3+v)&1] for u in range(3)]
            valid=[assignment for assignment in itertools.product([None,0,1,2],repeat=3)
                   if len([v for v in assignment if v is not None])==len({v for v in assignment if v is not None})
                   and all(v is None or v in g[u] for u,v in enumerate(assignment))]
            got=a.bipartite_matching(g,3)
            self.assertEqual(len(got),max(sum(v is not None for v in x) for x in valid))
            self.assertEqual(len(set(got.values())),len(got));self.assertTrue(all(v in g[u] for u,v in got.items()))

    def test_empty_self_loops_invalid_values_and_no_mutation(self):
        for f in [a.topological_order,a.components,a.strongly_connected,a.transitive_closure]:self.assertEqual(f([]),[])
        self.assertEqual(a.directed_cycle([[0]]),[0,0])
        self.assertEqual(a.bellman_ford([[(0,-1)]],0),[-math.inf])
        g=[[1],[]];saved=[r.copy() for r in g];a.shortest_path(g,0,1);self.assertEqual(g,saved)
        for call in [lambda:a.reachable([[]],True),lambda:a.graph([[1]]),lambda:a.graph([[0,0]]),lambda:a.components([[1],[]]),lambda:a.dijkstra([[(0,-1)]],0),lambda:a.zero_one_distances([[(0,2)]],0),lambda:a.critical_path([[]],[-1]),lambda:a.maximum_flow([[0]],0,0),lambda:a.bipartite_matching([[0]],0)]:
            with self.assertRaises(ValueError):call()


if __name__=='__main__':unittest.main(verbosity=2)
