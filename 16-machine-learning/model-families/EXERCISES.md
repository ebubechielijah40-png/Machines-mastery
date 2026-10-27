# Twenty-four reconstruction and transfer tasks

Attempt before [hints](HINTS.md) or [solutions](SOLUTIONS.md). Record assumptions,
intermediate numbers and a falsifiable prediction. Each numbered task has a
corresponding solution. A green reference test is not a completed learner task.

1. Derive binary negative log likelihood from a Bernoulli conditional model.
2. For x=(2,−1),y=1 and zero parameters, calculate a logistic gradient and a rate.1 update.
3. Add λ=.2 with w=(1,−2); separate data and penalty gradients. Why exclude bias?
4. Implement stable loss at logits±1000. Explain why `log(sigmoid(z))` can fail.
5. Fit a two-column scaler on rows(1,4),(3,4). Transform(5,4). Explain why the held row cannot participate in fitting.
6. Construct equal-accuracy probability forecasts with different NLL and Brier scores. Predict a shortcut reversal before running it.
7. Compute a valid 2D correlation of image[[1,2,3],[4,5,6]] and kernel[[1,−1]],stride1.
8. Derive output width from input width W,kernel K,padding P,stride S. Explain when there is no output.
9. Derive one circular filter's kernel, bias and output gradients under mean pooling.
10. Prove circular shift invariance with global mean or max pooling. State the assumptions that fail with zero padding.
11. At a tie in max pooling, explain the reference's first-winner derivative and why central differences need care.
12. Build correlation with an independently indexed exact rational oracle. Design a nonlinear local-pattern case a linear model cannot express across all rotations.
13. Trace `(u,r,b,v,c)=(1,.5,0,2,0)` on(1,0),y=1.
14. Derive all five parameter derivatives and both input derivatives for task13.
15. Show the linear recurrence sensitivity after T steps for r=.5,1,1.5.
16. Explain why |r|>1 does not prove exploding sensitivity in the tanh recurrence.
17. Given g=(3,4),cap2,rate.1, calculate the clipped update. Can clipping restore a zero gradient?
18. Train the first-sign task, then declare and execute a distractor test. Reconstruct the reverse loop without looking at the reference.
19. Fit alphabet(a,b) to documents['ab','a',''] with α1. Calculate the entire table and probability of 'ab' including termination.
20. Derive token-weighted NLL for documents of different lengths. Explain a generator's `terminated=False` result.
21. Prove that a bigram cannot condition its closing a/b choice after x on a distant first character.
22. Compute responsibilities for x=0 and1 with means−1,+1,unit variances,equal weights. Derive a complete EM step on points−1,+1.
23. Derive the variance floor update and explain symmetric initialization, label permutation and density collapse on repeated data.
24. Reconstruct count fitting, mixture posterior, EM and sampling. Design held-data and sampling tests that can reject a plausible-looking but wrong generator.
