# Checkable solutions

1.ρ=[[.8,−.4i],[.4i,.2]], trace1, determinant0, purity1.
2.Z probabilities(.8,.2) for both. The stated U yields(.9,.1) for the pure state
and(.5,.5) for the mixture; UρU† gives the same result as vector evolution.
3.x†ρx=a|x0+(c/a)x1|²+(b−|c|²/a)|x1|². For a0, positivity requires c0 and b≥0.
Matrix[[.5,1],[1,.5]] has determinant−.75 and negative eigenvalue−.5.
4.Phase-flip diagonal unchanged, off-diagonal(1−2p)c. Purity.68+.32(1−2p)².
At p1, Z is known rather than uncertain; a pure input stays pure.
5.K0†K0=diag(1,1−γ),K1†K1=diag(0,γ); sumI. Output entries are
(a+γb,√(1−γ)c;√(1−γ)c*,(1−γ)b). I/2 at γ1 becomes|0⟩⟨0|, purity.5→1.
6.Equal superposition encoding has two terms,000/111. The tensor cube has eight
equal terms and different measurement correlations. The encoding is a linear
isometry of a two-dimensional input, not a map to three independent copies.
7.For mask000,001,010,100 syndromes are00,10,11,01 respectively; correction is
I,X0,X1,X2. α/β does not affect syndrome because complementary basis words have
the same parity.
8.Weights0/1 recover correctly; weights2/3 become logical X. Thus
p_L=3p²(1−p)+p³=3p²−2p³. Its difference from p factors−p(2p−1)(p−1): improvement
for0<p<.5, equality at0,.5,1, degradation for.5<p<1.
9.Z sends(000+111)/√2 to(000−111)/√2; syndrome00, no correction, squared overlap0.
The code does not protect arbitrary single-qubit errors or all quantum information.
10.XXX has syndrome00 and a logical X effect, so p_L=p. Matching marginal error
rates is insufficient to infer the independent-error polynomial.
11.Combined logical error q=p_L(1−r)+(1−p_L)r=p_L+r−2p_Lr. Compare q<p for the
chosen p/r; for p_L<.5, it requires r<(p−p_L)/(1−2p_L). Example p.1 gives
r<(.1−.028)/.944≈.0762712. Physical gate faults need a richer model.
12.Reconstruction acceptance: explicit shape/Hermiticity/trace/PSD checks,
independent complex matrix products, completeness validation, exact parity
projectors, normalized branch probabilities, and recovery of an unequal complex
superposition for all single X errors. The phase counterexample must still fail.
