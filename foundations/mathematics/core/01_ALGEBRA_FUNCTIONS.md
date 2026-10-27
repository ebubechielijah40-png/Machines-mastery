# From quantities to equations and functions

Prerequisite: [counting and units](../counting-and-units/README.md). This chapter
supplies the algebra used by the following proof, linear-map and calculus chapters.
All examples and derivations are original. External source scopes are in
[SOURCES](SOURCES.md); this is not a chapter reconstruction of an unseen book.

## 1. A machine budget is already an equation

A sampler emits one12-byte header and4 bytes per sensor. For n sensors its record
size is `s=12+4n` bytes. With n=5, substitution gives12+20=32 bytes. If a record
must fit at most60 bytes, solve `12+4n<=60`: subtract12 from both sides, then
divide by positive4, giving n<=12. A nonnegative integer n in0..12 fits.

Why those steps? Equality means two expressions denote the same quantity.
Adding or subtracting the same quantity preserves equality. Multiplying or
dividing both sides by the same nonzero number preserves equality; multiplying
an inequality by a negative number reverses its direction. For example2<3 but
−2>−3. The relation12+4n<=60 describes a set of permitted inputs rather than a
single answer. The register's capacity imposes a constraint; it does not choose n.

A symbol is a name for a declared quantity. It may be a variable to solve for,
a controllable input, a fixed parameter or an unknown measured value. The same
letter cannot switch roles silently. Bytes per sensor multiplied by sensors is
bytes. Adding bytes to seconds is undefined in this budget, irrespective of
whether a programming language permits adding the corresponding bare numbers.

## 2. Signed values and fractions

Negative numbers encode a direction or a difference relative to a reference.
A balance change of−3 followed by+5 gives+2; neither number is a count of
negative physical objects. Addition has inverses: x+(−x)=0. Distributivity
explains the negative-times-negative rule: `0=(-a)(b-b)=(-a)b+(-a)(-b)`, so
`(-a)(-b)` must cancel−ab and therefore equals ab.

A fraction a/b, b nonzero, is the number whose product with b is a.
`a/b+c/d=(ad+bc)/(bd)` follows by expressing both fractions in the same unit
1/(bd). For example1/4+1/6=(3+2)/12=5/12. Adding denominators would give2/10,
which is a different quantity. `a/b * c/d=ac/(bd)` because multiplying the
result by bd recovers ac. To divide by c/d, multiply by d/c, provided c is
nonzero. Division by zero has no reciprocal:0 times anything is0, so it cannot
recover a nonzero numerator. Even0/0 is not unique.

A ratio compares quantities in compatible units. A record taking0.8ms under a
2ms budget uses0.4 of the budget. A proportion0.4 means40%; increasing a time
from10 to12ms is a20% increase, while returning12 to10 is a16⅔% decrease.
The reference denominator changed. Logs and performance claims must state it.

## 3. Powers, roots and logarithms have domains

For a positive integer k, x^k multiplies k copies of x. To preserve
`x^(a+b)=x^a*x^b` for nonzero x, define x^0=1 and x^(−k)=1/x^k. A root solves
a power equation. A nonnegative real x has a unique nonnegative square root;
the equation y²=9 has two real solutions±3, while the symbol√9 selects+3.

Exponential growth counts repeated multiplication. Doubling each step gives
1,2,4,8,...,2^k. A logarithm reverses that question: `log2(8)=3` asks how many
doublings give8. Logs require a positive real argument and a positive base other
than1. Counting halving steps in binary search yields a logarithm because
after k halvings the interval is approximately n/2^k. Setting that near1 gives
k approximately log2(n). This is a derivation about interval shrinkage, not a
universal runtime prediction.

An exponent in a physical formula must be dimensionless. If a response uses
`exp(-t/τ)`, both t and τ must have the same time unit. The exponential does
not accept an unexplained number of seconds as its argument. Unit conversions
occur before numeric evaluation.

## 4. Integer division is a contract

Fitting n bytes in pages of p bytes requires the smallest integer k with
kp>=n, namely ceil(n/p). For n>=0 and integer p>0, `(n+p-1)//p` implements it
with mathematical integers. At n=0, zero pages suffice; at n=p, one page
suffices. Using `n//p+1` unnecessarily allocates a page at exact multiples.

Euclidean division writes n=qp+r with0<=r<p for p>0. Python's `//` floors, so
−7//3=−3 and remainder2, because−7=(−3)*3+2. C integer division truncates
toward zero, giving quotient−2 and remainder−1 for the corresponding signed
values. Language semantics, integer width and overflow must be stated before
transferring a formula. `(n+p-1)` can overflow in a fixed-width machine even
when mathematical integers have no upper bound. A safer bounded implementation
can use `n//p + int(n%p != 0)` with an explicit nonnegative input contract.

## 5. Functions are mappings, not necessarily formulas

A function f:D→C assigns every allowed input in its domain D exactly one output
in its codomain C. A lookup table is a function when each key has one declared
value. A procedure that reads mutable external state is not a function of its
explicit arguments alone; state must be included in the input model.

For f(x)=2x+1, f(3)=7. If g(x)=x², composition means `(g∘f)(x)=g(f(x))`:
at3 it is49. Reversing order gives f(g(3))=19. Interfaces compose only when the
first output fits the second domain; a byte parser's arbitrary output cannot
be treated as a physically valid temperature without an interpretation step.

An inverse f⁻¹ reverses the mapping only if f is one-to-one on the chosen
domain and onto its declared target. The square function on all reals has no
single inverse because+2 and−2 both map to4. Restricting to nonnegative inputs
makes√x an inverse. A set of solution candidates is different from an inverse
function. A transpose is also not generally a matrix inverse, as chapter3 shows.

## 6. Linear, affine and nonlinear models

Linearity means `f(ax+by)=a f(x)+b f(y)` for all permitted combinations.
In particular f(0)=0. The mapping2x is linear;2x+1 is affine because it adds
an offset; x² is nonlinear because `(x+y)²` adds a2xy term. A straight line
with a nonzero intercept is therefore not a linear map in this precise sense.

Calibration example: raw sensor r maps to temperature T=a r+b. Two hypothetical
reference observations (r,T)=(100,20°C),(300,60°C) give
`200a=40`, so a=0.2°C/count and b=0°C in this constructed case. A third point
tests the affine assumption; it is not needed merely to solve two unknowns.
If the third observation is (200,43°C), an exact fit through all three is
impossible. Noise, drift, reference error or nonlinearity are competing models.
Least squares later supplies a declared compromise, not a proof that one model
is physically true.

A piecewise rule is often more realistic. A scheduler's waiting time can be
zero until a queue forms, then grow with load. A controller may clip its output
at an actuator limit. Differentiating the unclipped equation does not remove
the clipping boundary. Always state the domain, threshold behavior and units.

## 7. Build, check and transfer

Work by hand before implementation: calculate page counts for n=0,1,p−1,p,p+1;
substitute the calibrated reference points; compare both composition orders.
Write a function that rejects negative byte counts and nonpositive page sizes.
Compare every n from0 to100 against the defining inequality `(k−1)p<n<=kp`
for n>0, and k=0 for n=0. This verifies the contract independently of the
division formula.

The [separate exercises](EXERCISES.md) include algebra tasks A1–A8;
[hints](HINTS.md) and [solutions](SOLUTIONS.md) follow only after an attempt.
Rebuild the budget/calibration/page-count reasoning without these equations,
then explain which assumptions change when bytes become fixed-width integers.
Continue to [proofs and discrete models](02_PROOFS_DISCRETE.md).
