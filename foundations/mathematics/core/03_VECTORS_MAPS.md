# Vectors, linear maps, equations and sensitivity

Prerequisites: [algebra/functions](01_ALGEBRA_FUNCTIONS.md), finite sums,
[proofs](02_PROOFS_DISCRETE.md) and [coordinates/complex numbers](GEOMETRY_COMPLEX.md).
Matrix conventions here are explicit: a vector
is a column; a matrix has one row per output and one column per input. Some
ML code stores row vectors instead. Transposing a convention without changing
the equations is a shape bug, not a new mathematical result.

## 1. Why one number is insufficient

A moving machine has horizontal and vertical position. A vector x=(x₁,x₂)
records both in a declared order. Exchanging coordinates changes the state.
Adding vectors componentwise combines displacements: (2,1)+(−1,3)=(1,4)m.
Multiplying by a scalar rescales each component. An absolute position needs an
origin; a displacement does not change when that origin is translated.

A vector can also record temperature, pressure and voltage. These coordinates
have different units. Adding entries together without unit-compatible weights
is then not a physical measurement. A model `y=aᵀx` can still be valid if each
coefficient supplies the unit conversion needed to make every term a y-unit.
Calling all features “numbers” does not settle their semantics or calibration.

The real inner product is xᵀy=Σx_i y_i. It measures alignment relative to a
chosen coordinate metric. For (2,1) and(1,−2), the inner product is0: the
directions are perpendicular in the ordinary Euclidean plane. The Euclidean
norm is√(xᵀx), so||(3,4)||=5. A norm is a magnitude; its square has squared
units. For a complex vector use x†y=Σconjugate(x_i)y_i so x†x is real
nonnegative. Without conjugation, (i)ᵀ(i)=−1 would be an impossible squared
norm. The quantum statevector lesson uses precisely this distinction.

## 2. A matrix records what happens to the basis directions

Let e₁=(1,0),e₂=(0,1). Every x can be written x₁e₁+x₂e₂. If a map T is
linear, T(x)=x₁T(e₁)+x₂T(e₂). Place T(e₁) and T(e₂) as columns of A;
the expression is now Ax. This derives matrix-vector multiplication from
linearity instead of presenting a row-column ritual without a purpose.

Constructed map A=[[2,1],[0,3]] sends e₁ to(2,0),e₂ to(1,3). Therefore
for x=(2,1), Ax=2(2,0)+1(1,3)=(5,3). By rows, the same result is
(2*2+1*1,0*2+3*1). The two readings are the same linear combination.
For an m×n matrix, n inputs produce m outputs. A2×3 sensor mixing map
accepts three scalar inputs; it cannot multiply a length-two input.

An affine map Ax+b also shifts the origin. In image coordinates that can
represent a translation; it is not linear unless b=0. Homogeneous coordinates
can encode the affine operation as a larger linear map on restricted vectors
(x,1), but the added coordinate is part of the model, not a free physical axis.

## 3. Composition determines the multiplication order

Let B=[[1,0],[−1,1]]. Applying A then B to x gives B(Ax). Expanding output i:
Σ_k B_ik(Σ_j A_kj x_j)=Σ_j(Σ_k B_ik A_kj)x_j. Define the coefficient
in parentheses as (BA)_ij. Thus matrix multiplication represents composition.
This agrees with the inspected composition section of source VMLS; the present
numbers and derivation are original.

For these maps BA=[[2,1],[−2,2]], so BA(2,1)=(5,−2). In contrast
AB=[[1,1],[−3,3]], so AB(2,1)=(3,−3). Matrix multiplication generally does
not commute. Associativity follows from reassociating finite sums: C(BA)=(CB)A
when dimensions match. This explains why compiler/ML optimizations may change
parenthesization under exact arithmetic, but rounding can change final bits.

The identity I leaves coordinates unchanged because its columns are basis
vectors. The transpose Aᵀ exchanges rows and columns. It is not generally an
inverse: for diag(2,3), AᵀA=diag(4,9), not I. An inverse exists only when a
square map is one-to-one and onto. Orthogonal real or unitary complex matrices
are special: AᵀA=I or A†A=I, so transpose/adjoint supplies the inverse.

## 4. Solving equations means undoing a transformation

System3x+2y=7, x−2y=−3 can be eliminated without guessing. Add the equations:
4x=4, so x=1; substitute into the second:1−2y=−3, so y=2. Row replacement
by a row plus a multiple of another preserves the solution set because the
operation is reversible. Swapping rows also preserves it.

General Gaussian elimination repeats this idea. At column k choose a nonzero
pivot, swap it into row k, and subtract suitable multiples to zero entries
below it. Back substitution solves the resulting triangular system from the
last row upward. Inputs A,b are copied so the original evidence is preserved.
Partial pivoting chooses the largest available magnitude in that column to
avoid unnecessary division by a tiny candidate; it is not a universal stability
certificate. Row scaling puts each equation's largest coefficient near one.

Example requiring a swap:0x+2y=6,3x+4y=15. Dividing the first x coefficient
would fail. Swap rows, obtain y=3 from the second row, then x=1. The reference
solver implements this mechanism in scalar loops, not a hidden library solver.
Tests compare2×2 cases to independently derived rational Cramer's formulas.

Not every system has a unique answer. Rows(1,2),(2,4) with b=(3,6) repeat one
constraint and allow infinitely many points; b=(3,7) makes them inconsistent.
The solver rejects both as lacking a unique resolved solution. It does not
distinguish their geometry through a general rank-revealing factorization.
A tiny rejected pivot at a chosen tolerance is a numerical limitation, not a
proof of mathematical singularity. The exception text says so.

## 5. Small residual is different from small solution error

Consider x+y=2 and x+(1+δ)y=2+δ. Subtraction gives δy=δ, so x=y=1 for δ≠0.
Now perturb only the second recorded right side by ε. The solution becomes
y=1+ε/δ and x=1−ε/δ. If δ=10^-6 and ε=10^-7, the values shift by0.1
although the right-side change is very small. The two constraints are almost
parallel and barely distinguish one coordinate combination.

The residual r=Ax−b measures whether a candidate fits the recorded equations.
Sensitivity asks how the answer changes when those equations change. A tiny
residual can coexist with a large error relative to the unperturbed physical
answer. This is why more printed digits and passing a residual check cannot
establish a precise calibration. The experiment sweeps δ and preserves both
residual and solution changes. It is a software sensitivity study, not sensor
measurements.

In a square invertible model, Δx=A⁻¹Δb when A is fixed. A norm bound gives
||Δx||<=||A⁻¹|| ||Δb||. Relative bounds also involve||A||, leading to a
condition number. We do not compute a full singular-value condition estimate
in this small solver; the explicitly solved δ example demonstrates the
mechanism without pretending that a determinant is a universal condition metric.

## 6. Basis change is a coordinate change

If columns of P are a new independent basis, x=Pc translates new coordinates c
into old coordinates x. For P=[[1,1],[0,1]] and c=(2,3), x=(5,3). Recover c
by solving Pc=x, giving c=(2,3). A state has not moved physically merely
because its coordinate representation changed.

For a transformation T in old coordinates, new coordinates evolve by
`c_next=P⁻¹ T P c`. Multiplication order follows the actual interfaces:
new→old, transform, old→new. If P is singular, it is not a basis and that
inverse route fails. This same accounting appears in robot frames, Fourier
representations and quantum gate decompositions; each application must also
state its physical/model assumptions.

## 7. Fitting inconsistent observations

For observations at t=0,1,2 with recorded y=1,2,2, fit `a+b*t`. Define the
objective L=½Σ(a+b*t_i−y_i)², not “make it look close.” We can certify a
minimum without assuming calculus. If residual r=Ax−y is perpendicular to
every column of A, then changing x by h changes the squared residual to
`||r+Ah||²=||r||²+2hᵀAᵀr+||Ah||²`. The middle term vanishes and the last
is nonnegative. Thus no change can improve that candidate.

Here perpendicularity meansΣresidual=0 andΣt_i*residual=0, the inner products
with the constant and time columns. Thus3a+3b=5,3a+5b=6, so b=1/2,a=7/6.
Residuals are1/6,−1/3,1/6. They do not vanish, but both stated sums do, proving
this candidate minimizes the declared objective. The independent columns make
the minimizer unique: Ah=0 implies h=0 in this example.

The next chapter derives the gradient Aᵀ(Ax−y). In either formulation the
orthogonality equations are AᵀAx=Aᵀy. Explicitly forming
them can worsen conditioning because it multiplies the transformations.
Production numerical work often uses other factorizations. We have not supplied
a QR/SVD course or justified every data/noise model here. Least squares fits
the chosen objective; it does not establish causality, correct units or an
unbiased measurement process.

Run the core tests and [controlled experiment](EXPERIMENTS.md), attempt L1–L8
in the separated practice, then continue to [calculus and optimization](04_CALCULUS_OPTIMIZATION.md).
Reconstruction requires deriving multiplication order and elimination without
copying `linear.py`, not memorizing a successful output.
