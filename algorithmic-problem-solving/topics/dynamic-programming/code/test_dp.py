"""Independent finite search oracles; not a reimplementation of table recurrences."""
import itertools as it
import random
import unittest
from collections import deque
from functools import lru_cache
import dp


def subsets(n):
    for mask in range(1 << n): yield tuple(i for i in range(n) if mask >> i & 1)


def subsequences(s):
    return {''.join(s[i] for i in indices) for indices in subsets(len(s))}


def strings(maximum=4):
    return [''.join(xs) for n in range(maximum+1) for xs in it.product('ab',repeat=n)]


class DynamicTests(unittest.TestCase):
    def test_coin_objectives_against_bfs_and_count_vectors(self):
        for coins in ([1],[2],[1,3,4],[2,5],[]):
            for target in range(17):
                queue=deque([(0,())]); seen={0}; answer=None
                while queue:
                    amount,witness=queue.popleft()
                    if amount == target:answer=witness;break
                    for coin in coins:
                        new=amount+coin
                        if new<=target and new not in seen:seen.add(new);queue.append((new,witness+(coin,)))
                got=dp.min_coins(coins,target)
                self.assertEqual(None if got is None else len(got),None if answer is None else len(answer))
                if got is not None:self.assertEqual(sum(got),target);self.assertTrue(set(got)<=set(coins))
                counts=it.product(*(range(target//c+1) for c in coins))
                expected=sum(sum(c*n for c,n in zip(coins,ns))==target for ns in counts)
                self.assertEqual(dp.coin_combinations(coins,target),expected)
        self.assertEqual(len(dp.min_coins([1,3,4],6)),2)  # largest-first gives3 coins.

    def test_knapsack_and_subset_all_small_instances(self):
        rng=random.Random(2127)
        for _ in range(220):
            n=rng.randrange(8);weights=[rng.randrange(1,6) for _ in range(n)];values=[rng.randrange(-4,10) for _ in range(n)];capacity=rng.randrange(12)
            valid=[s for s in subsets(n) if sum(weights[i] for i in s)<=capacity]
            optimum=max(sum(values[i] for i in s) for s in valid)
            score,chosen=dp.knapsack(weights,values,capacity)
            self.assertEqual(score,optimum);self.assertEqual(len(set(chosen)),len(chosen));self.assertLessEqual(sum(weights[i] for i in chosen),capacity);self.assertEqual(sum(values[i] for i in chosen),score)
            nums=[rng.randrange(5) for _ in range(n)];target=rng.randrange(13)
            options=[s for s in subsets(n) if sum(nums[i] for i in s)==target];got=dp.subset_sum(nums,target)
            self.assertEqual(got is None,not options)
            if got is not None:self.assertEqual(len(set(got)),len(got));self.assertEqual(sum(nums[i] for i in got),target)

    def test_nonadjacent_and_lis_against_all_subsets(self):
        for n in range(7):
            for xs in it.product((-1,0,2),repeat=n):
                independent=[s for s in subsets(n) if all(b-a>1 for a,b in zip(s,s[1:]))]
                score,chosen=dp.nonadjacent(xs)
                self.assertEqual(score,max(sum(xs[i] for i in s) for s in independent));self.assertEqual(score,sum(xs[i] for i in chosen));self.assertTrue(all(b-a>1 for a,b in zip(chosen,chosen[1:])))
                increasing=[s for s in subsets(n) if all(xs[a]<xs[b] for a,b in zip(s,s[1:]))];got=dp.lis(xs)
                self.assertEqual(len(got),max(map(len,increasing)));self.assertEqual(tuple(sorted(got)),got);self.assertTrue(all(xs[a]<xs[b] for a,b in zip(got,got[1:])))

    def test_lcs_exhaustive_subsequence_intersection(self):
        all_strings=strings(4)
        for a in all_strings:
            for b in all_strings:
                common=subsequences(a)&subsequences(b);got=dp.lcs(a,b)
                self.assertIn(got,common);self.assertEqual(len(got),max(map(len,common)))

    def test_edit_distance_against_breadth_first_mutations(self):
        # BFS explores actual strings rather than prefix-state equations.
        for a in strings(2):
            distance={a:0};queue=deque([a])
            while queue:
                s=queue.popleft()
                if distance[s]>=3:continue
                choices={s[:i]+s[i+1:] for i in range(len(s))}
                choices|={s[:i]+x+s[i+1:] for i in range(len(s)) for x in 'ab'}
                if len(s)<3:choices|={s[:i]+x+s[i:] for i in range(len(s)+1) for x in 'ab'}
                for t in choices:
                    if t not in distance:distance[t]=distance[s]+1;queue.append(t)
            for b in strings(2):self.assertEqual(dp.edit_distance(a,b),distance[b])

    def test_grid_paths_and_cost_enumerate_complete_routes(self):
        rng=random.Random(118)
        for rows in range(1,4):
            for cols in range(1,4):
                routes=[]
                for down_positions in it.combinations(range(rows+cols-2),rows-1):
                    r=c=0;path=[(0,0)]
                    for step in range(rows+cols-2):
                        if step in down_positions:r+=1
                        else:c+=1
                        path.append((r,c))
                    routes.append(tuple(path))
                for _ in range(12):
                    blocked=[[rng.choice([False,False,True]) for _ in range(cols)] for _ in range(rows)]
                    self.assertEqual(dp.grid_paths(blocked),sum(not any(blocked[r][c] for r,c in path) for path in routes))
                    costs=[[rng.randrange(-3,6) for _ in range(cols)] for _ in range(rows)];score,path=dp.grid_cost(costs)
                    self.assertIn(path,routes);self.assertEqual(score,min(sum(costs[r][c] for r,c in p) for p in routes))
                    self.assertEqual(score,sum(costs[r][c] for r,c in path))

    def test_weighted_jobs_against_compatible_subsets(self):
        rng=random.Random(818)
        for _ in range(220):
            jobs=[]
            for _ in range(rng.randrange(8)):
                start=rng.randrange(-2,6);jobs.append((start,start+rng.randrange(1,5),rng.randrange(-3,10)))
            options=[]
            for s in subsets(len(jobs)):
                ordered=sorted(s,key=lambda i:jobs[i][0])
                if all(jobs[a][1]<=jobs[b][0] for a,b in zip(ordered,ordered[1:])):options.append(s)
            score,chosen=dp.weighted_intervals(jobs)
            self.assertEqual(score,max(sum(jobs[i][2] for i in s) for s in options));self.assertEqual(score,sum(jobs[i][2] for i in chosen));self.assertEqual(len(chosen),len(set(chosen)))
            self.assertTrue(all(jobs[a][1]<=jobs[b][0] for a,b in zip(chosen,chosen[1:])))

    def test_matrix_chain_all_binary_parenthesizations(self):
        def trees(ds):
            if len(ds)==2:return [(0,f'A{ds[0][0]}',ds[0][1],ds[1][1])]
        # Trees carry row/column counts; no optimal subproblem memoization.
        def enumerate_trees(dims,i,j):
            if j==i+1:return [(0,f'A{i}',dims[i],dims[j])]
            out=[]
            for k in range(i+1,j):
                for lc,ls,lr,lcol in enumerate_trees(dims,i,k):
                    for rc,rs,rr,rcol in enumerate_trees(dims,k,j):out.append((lc+rc+lr*lcol*rcol,f'({ls}*{rs})',lr,rcol))
            return out
        rng=random.Random(91)
        for n in range(1,7):
            for _ in range(20):
                dims=[rng.randrange(1,9) for _ in range(n+1)];all_trees=enumerate_trees(dims,0,n);score,tree=dp.matrix_chain(dims)
                self.assertEqual(score,min(t[0] for t in all_trees));self.assertIn((score,tree,dims[0],dims[-1]),all_trees)

    def test_text_layout_and_palindrome_cuts_enumerate_boundaries(self):
        for s in strings(6):
            options=[]
            for boundaries in subsets(max(0,len(s)-1)):
                breaks=(0,)+tuple(i+1 for i in boundaries)+(len(s),)
                pieces=[(a,b) for a,b in zip(breaks,breaks[1:]) if a<b]
                if all(s[a:b]==s[a:b][::-1] for a,b in pieces):options.append(pieces)
            cuts,pieces=dp.palindrome_cuts(s);self.assertEqual(cuts,min(max(0,len(p)-1) for p in options));self.assertEqual(''.join(s[a:b] for a,b in pieces),s);self.assertTrue(all(s[a:b]==s[a:b][::-1] for a,b in pieces))
        rng=random.Random(8)
        for _ in range(180):
            lengths=[rng.randrange(1,5) for _ in range(rng.randrange(8))];width=rng.randrange(1,10);options=[]
            for boundaries in subsets(max(0,len(lengths)-1)):
                breaks=(0,)+tuple(i+1 for i in boundaries)+(len(lengths),);pieces=[(a,b) for a,b in zip(breaks,breaks[1:]) if a<b]
                used=[sum(lengths[a:b])+b-a-1 for a,b in pieces]
                if all(n<=width for n in used):options.append((sum((width-n)**2 for n in used[:-1]),tuple(pieces)))
            got=dp.justify(lengths,width)
            self.assertEqual(got is None,not options)
            if got is not None:self.assertEqual(got[0],min(v[0] for v in options));self.assertIn(got,options)

    def test_bounded_routes_against_walk_enumeration(self):
        rng=random.Random(907)
        for _ in range(220):
            n=rng.randrange(1,5);edges=[(u,v,rng.randrange(-3,6)) for u in range(n) for v in range(n) if rng.random()<.35];hops=rng.randrange(5);s=rng.randrange(n);t=rng.randrange(n)
            frontier=[(s,0,(s,))];answers=[]
            for k in range(hops+1):
                answers.extend((cost,path) for v,cost,path in frontier if v==t)
                frontier=[(v,cost+w,path+(v,)) for x,cost,path in frontier for u,v,w in edges if u==x]
            got=dp.bounded_route(n,edges,s,t,hops);self.assertEqual(got is None,not answers)
            if got is not None:self.assertEqual(got[0],min(x[0] for x in answers));self.assertIn(got,answers)

    def test_assignment_against_permutations(self):
        rng=random.Random(440)
        for n in range(7):
            for _ in range(20):
                costs=[[rng.randrange(-4,11) for _ in range(n)] for _ in range(n)];score,chosen=dp.assignment(costs)
                self.assertEqual(sorted(chosen),list(range(n)));self.assertEqual(score,sum(costs[i][j] for i,j in enumerate(chosen)));self.assertEqual(score,min(sum(costs[i][j] for i,j in enumerate(p)) for p in it.permutations(range(n))))

    def test_finite_string_counts(self):
        for n in range(13):self.assertEqual(dp.binary_no_adjacent(n),sum('11' not in ''.join(xs) for xs in it.product('01',repeat=n)))
        for text in strings(5):
            for pattern in strings(3):self.assertEqual(dp.subsequence_count(text,pattern),sum(''.join(text[i] for i in s)==pattern for s in subsets(len(text))))

    def test_boolean_counts_against_enumerated_syntax_trees(self):
        def results(values,ops):
            if len(values)==1:return [values[0]]
            out=[]
            for k,op in enumerate(ops):
                for a in results(values[:k+1],ops[:k]):
                    for b in results(values[k+1:],ops[k+1:]):out.append((a and b) if op=='&' else ((a or b) if op=='|' else (a!=b)))
            return out
        rng=random.Random(808)
        for n in range(1,7):
            for _ in range(30):
                values=[rng.choice([False,True]) for _ in range(n)];ops=[rng.choice(['&','|','^']) for _ in range(n-1)];self.assertEqual(dp.boolean_parenthesizations(values,ops),sum(results(values,ops)))

    def test_egg_coverage_against_floor_minimax(self):
        @lru_cache(None)
        def minimax(e,f):
            if f==0:return 0
            if e==1:return f
            return 1+min(max(minimax(e-1,k-1),minimax(e,f-k)) for k in range(1,f+1))
        for e in range(1,6):
            for f in range(31):self.assertEqual(dp.egg_drop(e,f),minimax(e,f))

    def test_boundaries_and_rejected_inputs(self):
        self.assertEqual(dp.min_coins([],0),());self.assertIsNone(dp.min_coins([],1));self.assertEqual(dp.coin_combinations([],0),1);self.assertEqual(dp.knapsack([],[],5),(0,()));self.assertEqual(dp.subset_sum([0,0],0),());self.assertEqual(dp.nonadjacent([-4]),(0,()));self.assertEqual(dp.nonadjacent([4]),(4,(0,)));self.assertEqual(dp.lis([]),());self.assertEqual(dp.grid_paths([]),0);self.assertIsNone(dp.grid_cost([[]]));self.assertEqual(dp.assignment([]),(0,()));self.assertEqual(dp.palindrome_cuts(''),(0,()))
        bad=[lambda:dp.min_coins([0],4),lambda:dp.coin_combinations([1,1],3),lambda:dp.knapsack([1],[1,2],3),lambda:dp.subset_sum([-1],2),lambda:dp.grid_paths([[1]]),lambda:dp.grid_cost([[1],[]]),lambda:dp.weighted_intervals([(3,3,1)]),lambda:dp.matrix_chain([2]),lambda:dp.justify([0],4),lambda:dp.bounded_route(2,[(0,2,1)],0,1,2),lambda:dp.assignment([[1,2]]),lambda:dp.assignment([[0]*17 for _ in range(17)]),lambda:dp.binary_no_adjacent(True),lambda:dp.boolean_parenthesizations([True],['&']),lambda:dp.egg_drop(0,1)]
        for call in bad:
            with self.assertRaises(ValueError):call()


if __name__=='__main__':unittest.main(verbosity=2)
