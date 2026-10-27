# Reference reasoning, after independent work

These answers are model solutions, not evidence of learner competence. Reproduce
the argument with different numbers after comparing your first attempt.

## A — Algebra

1. `12+4n≤60` gives n≤12. Together with the count contract this permits
   n=0,…,12. A strict `<60` gives n<12, hence n=0,…,11. Rounding the real
   inequality before stating the integer domain risks accepting n=12 incorrectly.
2. The least common denominator is 24: 9/24+10/24=19/24. Increasing 8→10 ms
   is 2/8=25%; decreasing 10→8 is −2/10=−20%. An absolute change can have
   equal magnitude while its relative percentage differs.
3. Subtract 5: −3x≤9. Divide by −3 and reverse direction: x≥−3. At x=−3
   the left side is14; x=−4 gives17 and fails; x=−2 gives11 and passes.
4. `200a=50°C`, so a=0.25°C/count and b=−2.5°C. At130 the model predicts30°C.
   A reference34°C disagrees by4°C. The three values cannot all be exact under
   this affine model, but noise, drift, reference bias and nonlinearity remain
   possible explanations. Two fitting equations do not validate their model.
5. f(−2)=−3, so g(f(−2))=9. g(−2)=4, so f(g(−2))=9 also in this particular
   case. Equal results at one input do not make compositions identical: at3
   the results are49 and19. Squaring is many-to-one over the reals, so4 does
   not select a unique inverse value unless the domain is restricted.
6. If n=qp+r, a full q pages covers n exactly when r=0; otherwise q+1 pages
   is minimal. The values for p>1 are0,1,1,1,2 respectively. At p=1 the listed
   n values overlap, and the same formula still gives n. In a fixed-width type,
   n+p−1 can overflow even if the true result fits. `n//p+int(n%p!=0)` avoids
   that intermediate under the nonnegative contract.
7. t=0.3 s, τ=0.2 s, so −t/τ=−1.5. Using300/0.2 combines milliseconds with
   seconds without conversion and is off by1000. The response itself is
   exp(−1.5), a dimensionless multiplier of an appropriately unitful amplitude.
8. Solve slope from differences, reject equal raw inputs before division,
   and check the fitted references independently. A line extrapolated from
   two room-temperature readings might predict an impossible actuator range
   or be invalid after sensor saturation. Algebra cannot certify that domain.

## D — Discrete models

1. Negation: there exists an accepted message without a valid signature.
   Original implication: accepted⇒valid. Converse: valid⇒accepted. Contrapositive:
   not valid⇒not accepted. Only the converse states sufficiency. Authorization,
   expiry and replay checks can make a valid signature insufficient.
2. An arbitrary odd integer is2k+1. Its square is2(2k²+2k)+1, which has the
   definition of odd. The integer k was unrestricted. A finite check covers
   only its tested domain, although it can refute a broken implementation.
3. At n=0 the empty sum and0² agree. If the sum of the first n odd numbers
   is n², adding2n+1 gives(n+1)². Both the initial case and induction step
   are necessary; the step alone would allow incorrectly shifted formulas.
4. Remainders84,30,24,6,0 satisfy24=84−2·30 and6=30−24=−84+3·30.
   Thus(s,t)=(−1,3). At each step both remainder rows remain integer linear
   combinations of the original inputs, while the common-divisor set is
   unchanged. The nonnegative second remainder strictly decreases. At zero,
   the other row is the gcd; for(0,0), the implementation explicitly returns0.
5. Modulo17,3²=9,3⁴=13,3⁸=16. Since13=8+4+1, the answer is16·13·3 mod17=12.
   Initially result=1 mod m. Every update preserves result·base^remaining
   modulo m. Halving remaining terminates. For exponent0 the answer is1 mod m;
   at m=1 every result is0. Negative exponents are excluded by this API.
6. Undirected edges:8·7/2=28. Directed edges:8·7=56. A straightforward matrix
   scan examines8² entries, including diagonal positions even when loops are
   disallowed. An adjacency-list scan instead visits existing edges plus vertices.
7. Process A can advance its local counter to1 and process B to2 without any
   message. Their events are concurrent even though1<2. A timestamp plus a
   process-ID tie-breaker gives a total sort, but does not create a causal edge.
8. For a positive page demand, test(k−1)p<n≤kp; for Euclid, check Bézout plus
   a separate gcd oracle. Exhaustion over the chosen finite grid establishes
   those properties on that grid for the tested execution. The invariant and
   decreasing remainder justify all mathematical integer inputs, conditional
   on the algorithm matching its proof and sufficient resources.

## G — Coordinates and complex arithmetic

1. The outer area is(a+b)², four triangles total2ab and the inner area is h².
   Subtracting2ab yields h²=a²+b². The displacement is(3,4)m and length5 m.
   Translating the origin changes both positions but leaves their difference,
   so distance between them must be calculated from that difference.
2. 135 degrees is3π/4 radians; a quarter-turn is90 degrees. Python's90
   argument is not a quarter-turn until multiplied byπ/180. Atπ/4, x=y>0
   and x²+y²=1, so both equal1/√2.
3. The product is−8+i with squared modulus65. Independently |2+3i|²=13
   and|−1+2i|²=5, giving65. Multiplication by i sends(x,y) to(−y,x),
   preserving squared length; multiplication by2 gives(2x,2y), quadrupling
   squared length and doubling length.
4. The reciprocal is(3+4i)/25, since(3−4i)(3+4i)=25. The zero number has
   no reciprocal. Conjugate3+4i is a complex number, reciprocal(3+4i)/25
   undoes multiplication, and modulus5 is the nonnegative distance.
5. Coordinates become(xcosφ−ysinφ,xsinφ+ycosφ). Their squared sum expands
   to x²(cos²φ+sin²φ)+y²(sin²φ+cos²φ), with cross terms canceling, so it is
   x²+y². Atπ/2,(2,−1) becomes(1,2)m. Taking positive angle clockwise
   instead gives(−1,−2)m for the same positive numeric angle.
6. The roots sum0, whereas their squared moduli sum4. A normalized state
   requires a chosen orthonormal basis and sum of squared amplitude magnitudes1;
   the Born measurement rule assigns those squared magnitudes as probabilities.
   A change of measurement basis first changes amplitudes through a unitary
   map. These additional quantum assumptions are taught in the statevector unit;
   complex arithmetic alone is not a physical probability law.

## L — Maps and equations

1. A=[[1,−1],[2,0],[0,3]]. A(4,2)=4(1,2,0)+2(−1,0,3)=(2,8,6).
   Two input coordinates produce three outputs; columns are input directions.
2. Ax=(5,3); B(Ax)=(5,−2). BA=[[2,1],[−2,2]], while AB=[[1,1],[−3,3]]
   gives(3,−3). B mixes A's outputs; A mixing B's outputs is a different system.
3. Swap rows to put3 in the first pivot. First obtain y=3 from2y=6, then
   x=(15−4·3)/3=1. Systems x+y=1,2x+2y=3 and x+y=1,2x+2y=2 respectively
   have no solution and infinitely many. A square shape alone proves neither
   uniqueness nor consistency.
4. Equations become x+y=2 and x+(1+δ)y=2+δ+ε. Subtracting yields
   δy=δ+ε, so y=1+ε/δ and x=1−ε/δ. With the stated values the solution
   is(0.9,1.1), despite only a10⁻⁷ change in one input. Units must be consistent
   with the matrix coefficients; arbitrary rescaling can change a numerical
   condition measure. A small residual under the perturbed equations does
   not establish closeness to the solution of the original measurements.
5. z†z=1+conjugate(i)i=2. zᵀz=1+i²=0 despite z being nonzero. A Hermitian
   inner product makes the associated norm consistent with nonzero states.
6. Residuals(c−1,c+m−2,c+2m−2) must have sum0 and time-weighted sum0.
   Hence3c+3m=5 and3c+5m=6. Subtracting gives m=1/2,c=7/6. Residuals are
   (1/6,−1/3,1/6): sum0 and0−1/3+2/6=0. Normal equations characterize this
   full-rank least-squares optimum. They can worsen conditioning numerically;
   this does not implement a general-purpose QR solver.
7. x=Pc=(5,3); Tx=(10,3). Solving Pc'=(10,3) gives c'=(7,3).
   P⁻¹TP=[[2,1],[0,1]], which maps(2,3) to(7,3). Merely replacing c with Pc
   changes the description of the same physical vector; applying T changes it.
8. Check a rectangular map by independent basis-column combinations. For
   diag(10⁻¹⁵⁰,2·10⁻¹⁵⁰) and b=(10⁻¹⁵⁰,4·10⁻¹⁵⁰), the result should be(1,2),
   so an absolute pivot cutoff would be misleading. For repeated rows there is
   no unique solution. A very small nonzero pivot might be rejected because
   the declared floating resolution is insufficient, not because an exact
   algebraic rank calculation proved singularity.

## C — Change, accumulation and optimization

1. (x+h)²=x²+2xh+h². Relative to h, the remainder is h and tends to0,
   giving derivative2x. At zero, |h|/h is+1 from the right and−1 from the left,
   so no single derivative describes both directions. Continuity is weaker.
2. Values are u=4,v=16,loss=144. Local derivatives are3,8,24; the product is576.
   For u*u the first operand contributes u and the second contributes u, so
   together they give2u. A graph that overwrites one path loses half the derivative.
3. With r=Ax−b, perturbation gives L(x+Δ)=L(x)+rᵀAΔ+½||AΔ||².
   The first-order coefficient is Aᵀr. A transpose maps output sensitivities
   back to input sensitivities; an inverse would try to reconstruct values,
   may not exist, and answers a different question.
4. e_next=(1−αλ)e. For λ>0, convergence requires0<α<2/λ. A multiplier in(0,1)
   shrinks without changing sign; in(−1,0) it alternates; at−1 it does not decay;
   below−1 it grows. At0 it reaches the minimum in one step. If λ=0 the loss
   is flat and every point is a minimizer; there is no unique attraction point.
5. For α=.4, x₁=(.6,−.6),x₂=(.36,.36),x₃=(.216,−.216).
   For α=.6, x₁=(.4,−1.4),x₂=(.16,1.96),x₃=(.064,−2.744).
   The second curvature4 imposes α<.5. Improving the first coordinate does
   not rescue a shared update that destabilizes the second.
6. Right rectangles sum n(n+1)(2n+1)/(6n³), tending to1/3.
   Trapezoids for this exact quadratic give1/3+1/(6n²), so halving the step
   reduces error by4 until rounding dominates. A different function that agrees
   at every sample could oscillate between them; finite samples do not rule it out.
7. x_next=x−hkx=(1−hk)x; k has units1/time. Bounded decay needs0<hk<2.
   At hk=1.5, positive x₀ alternates sign with magnitude shrinking by1/2;
   exact x₀exp(−kt) remains positive. Stability does not guarantee a physically
   admissible trajectory or high accuracy.
8. The new curvature is100 and optimum is.1, so the fixed positive step must
   satisfy α<.02. A step stable for curvature1 can now diverge. Evaluate
   held-out data, shifts and leakage separately; the objective's decrease only
   records fitting behavior under its particular data and model assumptions.
