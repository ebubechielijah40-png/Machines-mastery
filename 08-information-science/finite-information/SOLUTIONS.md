# Solutions

1. Values are 0,3, and `(.5*1)+(.25*2)+(.125*3)+(.125*3)=1.75` bits.
2. With rows X=0,1 and columns Y=0,1, use `[[3/8,3/8],[1/8,1/8]]`. Every nonzero cell equals its row marginal times column marginal; each log ratio is log2(1)=0. Entropy of the joint is the sum of marginal entropies.
3. r=.5 produces an independent fair output and zero mutual information. r=1 makes Y=1-X, with zero conditional uncertainty and one bit of mutual information. The second channel needs inversion rather than guessing.
4. Counting symbols within the fixed output may give a nonzero empirical byte entropy. Across query outputs there is only one possible string, hence zero whole-output entropy under that process. Neither frequency statistic establishes a secret unknown to an attacker or security of the generating mechanism.
5. The direct log-ratio formula and a literal diagonal/off-diagonal table distinguish errors in marginal extraction and conditional-entropy subtraction. Small floating deviations near zero require numerical tolerance; they do not imply a real negative information quantity.
