import itertools
import math
import unittest
from population import *
from phylogeny import *


class PopulationTests(unittest.TestCase):
    def test_transition_matches_explicit_four_draw_enumeration(self):
        for i in range(5):
            p=i/4;expected=[0.0]*5
            for draws in itertools.product((0,1),repeat=4):
                chance=math.prod(p if x else 1-p for x in draws)
                expected[sum(draws)]+=chance
            for x,y in zip(transition(4,i),expected):self.assertAlmostEqual(x,y)
        self.assertEqual(transition(4,2),[1/16,4/16,6/16,4/16,1/16])

    def test_neutral_mean_variance_and_diversity_identities(self):
        for m,start in [(4,1),(10,5),(20,3)]:
            p=start/m
            for t,dist in enumerate(evolve(m,start,20)):
                stats=summary(dist)
                self.assertAlmostEqual(stats['total_probability'],1)
                self.assertAlmostEqual(stats['mean_frequency'],p)
                self.assertAlmostEqual(stats['variance_frequency'],p*(1-p)*(1-(1-1/m)**t))
                self.assertAlmostEqual(stats['expected_heterozygosity'],2*p*(1-p)*(1-1/m)**t)

    def test_eventual_fixation_is_not_one_generation_probability(self):
        self.assertEqual(transition(4,2)[4],1/16)
        stats=summary(evolve(4,2,200)[-1])
        self.assertAlmostEqual(stats['fixation_probability'],.5,places=10)
        self.assertAlmostEqual(stats['loss_probability'],.5,places=10)

    def test_selection_is_fitness_weighted_then_sampled(self):
        self.assertAlmostEqual(selected_frequency(.25,1),.4)
        row=transition(10,5,.2)
        self.assertAlmostEqual(sum(i/10*p for i,p in enumerate(row)),6/11)
        for start in [0,10]:
            self.assertEqual(simulate(10,start,10,seed=4),[start]*11)

    def test_seeded_bernoulli_simulations_agree_with_exact_ensemble(self):
        m,start,t,reps=10,3,8,2000
        outcomes=[simulate(m,start,t,seed=i)[-1]/m for i in range(reps)]
        exact=summary(evolve(m,start,t)[-1])
        standard_error=math.sqrt(exact['variance_frequency']/reps)
        self.assertLess(abs(sum(outcomes)/reps-exact['mean_frequency']),6*standard_error)
        self.assertEqual(simulate(m,start,t,seed=17),simulate(m,start,t,seed=17))

    def test_likelihood_matches_direct_product_and_impossible_transition(self):
        path=[2,3,1,0]
        direct=math.prod(transition(4,a,.3)[b] for a,b in zip(path,path[1:]))
        self.assertAlmostEqual(log_likelihood(4,path,.3),math.log(direct))
        self.assertEqual(log_likelihood(4,[0,1]),-math.inf)
        self.assertEqual(log_likelihood(4,[4,4,4]),0)

    def test_population_invalid_boundaries(self):
        for args in [(1,0),(4,5),(4,True)]:
            with self.assertRaises(ValueError):transition(*args)
        for s in [-1,float('nan'),True]:
            with self.assertRaises(ValueError):selected_frequency(.5,s)
        with self.assertRaises(ValueError):evolve(200,100,10000)
        with self.assertRaises(ValueError):summary([.2,.2,.2])


class PhylogenyTests(unittest.TestCase):
    def test_jc_distance_from_independent_forward_model(self):
        for d in [0,.01,.1,.5,2,5]:
            p=.75*(1-math.exp(-4*d/3))
            self.assertAlmostEqual(jc_from_fraction(p),d)
        self.assertAlmostEqual(jc_distance('AAAA','AAAT'),-.75*math.log(2/3))
        for args in [('',''),('A','AA'),('A-','AA'),('AN','AA')]:
            with self.assertRaises(ValueError):jc_distance(*args)
        with self.assertRaises(ValueError):jc_from_fraction(.75)

    def test_ultrametric_matrix_is_exactly_reconstructed(self):
        labels=['A','B','C','D'];d=[[0,2,6,6],[2,0,6,6],[6,6,0,4],[6,6,4,0]]
        root,trace=upgma(labels,d)
        self.assertEqual([t['height'] for t in trace],[1,2,3])
        self.assertEqual(ultrametric_violation(labels,d),0)
        inferred=cophenetic(root)
        for i,j in itertools.combinations(range(4),2):self.assertEqual(inferred[(labels[i],labels[j])],d[i][j])

    def test_cluster_average_and_label_permutation(self):
        labels=['A','B','C'];d=[[0,2,4],[2,0,6],[4,6,0]]
        root,_=upgma(labels,d);self.assertEqual(root.height,2.5)
        order=[2,0,1]
        permuted,_=upgma([labels[i] for i in order],[[d[i][j] for j in order] for i in order])
        self.assertEqual(root.record(),permuted.record())

    def test_nonclock_tree_counterexample_is_not_silently_correct(self):
        labels=['A','B','C','D'];d=[[0,6,4,4],[6,0,8,8],[4,8,0,2],[4,8,2,0]]
        root,_=upgma(labels,d)
        self.assertNotIn(('A','B'),clades(root))
        self.assertIn(('A','C','D'),clades(root))
        self.assertGreater(ultrametric_violation(labels,d),0)
        inferred=cophenetic(root)
        self.assertNotEqual(inferred[('A','B')],6)

    def test_invalid_distance_boundary(self):
        for labels,d in [(['A','A'],[[0,1],[1,0]]),(['A','B'],[[0,1],[2,0]]),(['A','B'],[[0,-1],[-1,0]]),(['A','B'],[[1,1],[1,0]])]:
            with self.assertRaises(ValueError):upgma(labels,d)
        for bad in [[[0,1],[None,0]],[[0,1],[True,0]],[[0,10**1000],[10**1000,0]],[[0,1],None]]:
            with self.assertRaises(ValueError):upgma(['A','B'],bad)

if __name__=='__main__':unittest.main(verbosity=2)
