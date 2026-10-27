# Attempt before consulting hints or solutions

Use the numbered chapter containing each topic. Retain intermediate equations,
units, input assumptions and independent checks. The later questions require
transfer; repeating a definition does not satisfy them.

## A — Algebra and functions

1. A record contains a 12-byte header and 4 bytes per sensor. With a 60-byte
   limit, derive the permitted nonnegative sensor counts. What changes for a
   strict limit of less than 60 bytes?
2. Add 3/8 and 5/12 without using decimal approximations. Explain the common
   denominator. A time rises from 8 ms to 10 ms and returns: find both relative
   percentage changes.
3. Solve −3x+5≤14. Explain the inequality direction and check two boundary-side
   values by substitution.
4. Derive the affine calibration through (raw,temperature)=(50,10°C),(250,60°C).
   Predict the reading at raw 130. What does a third reference at (130,34°C)
   establish, and what does it leave ambiguous?
5. With f(x)=2x+1 and g(x)=x², compute both composition orders at x=−2.
   Why does squaring over all real inputs lack an inverse function?
6. Rebuild `page_count` for n≥0 and p>0. Check n=0,1,p−1,p,p+1. Explain a
   fixed-width overflow risk in `(n+p-1)//p`.
7. Explain why exp(−t/τ) has a valid dimensionless argument when t=300 ms and
   τ=0.2 s. Compute the argument and show why treating 300/0.2 as the ratio
   would be wrong.
8. Reconstruct a small byte-budget and calibration program from memory. Reject
   negative counts and an equal pair of raw calibration inputs. Give an example
   where the fitted line is algebraically correct yet physically implausible.

## D — Discrete reasoning

1. Negate “every accepted message has a valid signature.” Distinguish its
   converse from its contrapositive. Which direction would establish that a
   valid signature is sufficient for acceptance?
2. Prove that the square of an odd integer is odd. Explain why checking the
   first million odd integers is a different kind of evidence.
3. Prove by induction that the first n odd positive integers sum to n²,
   including the empty sum at n=0.
4. Trace extended Euclid for 84 and 30. Produce integers s,t such that
   84s+30t=gcd(84,30), then explain the loop invariant and termination measure.
5. Compute 3¹³ modulo 17 by square-and-multiply. State an invariant that covers
   every iteration; include exponent zero and modulus one in your contract.
6. Count the edges of a complete simple undirected graph on 8 vertices and
   compare a directed graph without self-loops. What representation work does
   an adjacency matrix require to scan all potential neighbors?
7. Refute “A has a lower timestamp than B, so A caused B” with two independent
   processes. Distinguish a total sorting rule from a causal partial order.
8. From memory, implement the integer mechanisms and tests using a specification
   other than the same formula. Explain one property that exhaustive bounded
   tests establish and one unbounded claim requiring a proof.

## G — Coordinates, angles and complex numbers

1. Derive the distance relation from the four-triangle area construction.
   Find the distance between positions (−2,1)m and (1,5)m. Why must you use
   displacement rather than either position's distance from the origin?
2. Convert 135 degrees to radians and a quarter-turn to degrees. Explain the
   distinction between sin(90 radians) and sin(90 degrees). Find both coordinates
   of a unit direction at angleπ/4 without a trigonometry table.
3. Expand (2+3i)(−1+2i) and verify its squared modulus by real arithmetic.
   Explain why multiplying by i is a quarter-turn while multiplying by2
   changes the length.
4. Derive the reciprocal of3−4i, then verify the product is1. What changes
   when the number is zero? Distinguish conjugation, reciprocal and modulus.
5. Derive the two real coordinate equations for multiplication by cosφ+i sinφ.
   Prove squared norm preservation by expansion. Rotate(2,−1)m byπ/2 and
   state the result under the opposite positive-angle convention.
6. Reconstruct the complex arithmetic and phase experiment without the reference.
   Sum the fourth roots of unity and their squared moduli separately. Explain
   why amplitude cancellation does not mean individual nonnegative magnitudes
   cancel. What extra probability rule is needed before treating the numbers
   as a quantum state?

## L — Linear maps

1. T(e₁)=(1,2,0), T(e₂)=(−1,0,3). Construct T's matrix and compute T(4,2).
   State the input and output dimensions.
2. Use A=[[2,1],[0,3]], B=[[1,0],[−1,1]], x=(2,1). Compute Ax, B(Ax), BA
   and AB. Show exactly where changing the order changes the state.
3. Solve 0x+2y=6, 3x+4y=15 with an explicit row swap. Then give one system
   with no solution and one with infinitely many solutions.
4. For A=[[1,1],[1,1+δ]], x=(1,1), perturb only the second component of b=Ax
   by ε. Derive the changed solution, not just a residual. Evaluate δ=10⁻⁶,
   ε=10⁻⁷ and interpret the units and modeling assumptions.
5. Compute the Hermitian squared norm of z=(1,i). What does an unconjugated
   dot product return, and why is it unsuitable as a squared norm?
6. Fit y≈c+mt through (0,1),(1,2),(2,2) by deriving the normal equations.
   Verify both residual orthogonality equations after solving them.
7. Let basis columns form P=[[1,1],[0,1]], coordinates c=(2,3), and physical
   map T=diag(2,1). Find standard coordinates x, transformed x, and transformed
   basis coordinates. Explain P⁻¹TP without treating a basis change as motion.
8. Rebuild products and a small pivoting solver. Design independent tests for
   a rectangular product, a tiny uniformly scaled nonsingular system and a
   rank-deficient system. Explain why a rejected tolerance is not an exact
   singularity proof.

## C — Calculus and optimization

1. Derive the derivative of x² from its first-order expansion. Explain why |x|
   has no derivative at zero, despite being continuous there.
2. For u=3x+1, v=u², loss=(v−4)² at x=1, calculate every value and every local
   derivative. Explain why both uses of u in u*u contribute.
3. Derive ∇(½||Ax−b||²)=Aᵀ(Ax−b) by perturbing x. Why does a transpose appear
   rather than an inverse?
4. Derive the stable positive learning-rate range for ½λ(x−x*)². Describe
   monotone convergence, alternating convergence, a nondecaying boundary and
   divergence. Handle λ=0 separately.
5. For A=diag(1,2), b=0, x₀=(1,1), calculate the first three states for α=0.4
   and α=0.6. Which coordinate determines the stricter shared bound?
6. Derive the right-rectangle sum for t² on [0,1] and its limit. Implement the
   trapezoid approximation, halve the step and compare error ratios. What
   information about behavior between samples is still unavailable?
7. Derive Euler's update for dx/dt=−kx, including dimensions of k and the
   multiplier stability condition. Give an update that decays with alternating
   sign despite the exact positive solution staying positive.
8. Without a reference, reconstruct the gradient computation and stability
   experiment. Transfer it to L=½(10x−1)². Explain why rescaling a feature
   can require a new step and why decreasing training loss alone is insufficient
   evidence of useful generalization.

Use [hints](HINTS.md) after a sustained attempt. Compare reasoning against
[solutions](SOLUTIONS.md) only afterwards. No answer file records learner success.
