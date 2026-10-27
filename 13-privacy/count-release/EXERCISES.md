# Exercises: privacy count release

1. For D=[1,0,1], list all possible counts of its add/remove-one-row neighbors. Prove the count sensitivity is one without assuming the dataset size is public.
2. One person may contribute up to four bits. Derive the noise scale needed for person-level ε=.2, and explain why row-level calibration would be inadequate.
3. Work out F and its inverse on both sides of zero. Evaluate quantiles at u=.25,.5,.75 with b=3. What happens at exactly zero and one?
4. For neighboring counts 10 and 11, calculate the log likelihood ratio at t=-20,10.5,30 with b=2. Give an output region showing the ε=.5 promise fails for b=.5.
5. You have a declared budget ε=1. Compare one ε=1 release with ten ε=.1 releases averaged. Derive each noise variance under independent ideal Laplace noise.
6. Demonstrate why known/reused random seeds invalidate the intended privacy interpretation while leaving many utility statistics unchanged. What part of the mathematical proof no longer applies?
7. Decide whether clipping to [0,100] is justified if 100 is a fixed public capacity. Contrast clipping to [0,len(private_rows)].
8. Reconstruction: implement sensitivity-one inverse-CDF sampling and an integer budget gate from memory. State exactly which results are mathematically proved and which are merely observed by finite tests.
9. Transfer: a person can ask through two service accounts, restart the process or submit the same underlying population as a new list. Identify why this accountant cannot enforce the intended total disclosure limit.
