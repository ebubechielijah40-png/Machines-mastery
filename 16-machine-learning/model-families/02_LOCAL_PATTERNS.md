# A local detector reused across positions

A flattened linear classifier assigns a separate weight to every location.
If a useful adjacent pattern moves to a new location, those weights provide no
guarantee that the same detector moves with it. A convolutional family ties
local weights across positions. We derive that restriction before interpreting
what it can and cannot learn.

## First compute a patch operation

For input X and kernel K, cross-correlation at output(i,j) is
ΣᵤΣᵥ K[u,v]X[i+u,j+v]. Mathematical convolution reverses kernel coordinates;
this implementation deliberately uses cross-correlation. There is no reversal
hidden behind the function name.

Take

\[
 X=\begin{bmatrix}2&1&0\\3&-1&4\\0&2&5\end{bmatrix},\qquad
 K=\begin{bmatrix}1&-2\\0&3\end{bmatrix}.
\]

The upper-left output is2×1+1×(−2)+3×0+(−1)×3=−3. The other patch products are
1×1+0×(−2)+(−1)×0+4×3=13;
3×1+(−1)×(−2)+0×0+2×3=11;
and(−1)×1+4×(−2)+2×0+5×3=6. The output is therefore [[−3,13],[11,6]].
All four products matter; an asymmetric kernel reveals accidental reversal that
an all-ones kernel cannot detect.

With input height H, kernel height k, p explicit zero-padding on both sides,
stride s and no dilation, valid top-left coordinates are0,s,2s,…≤H+2p−k.
Counting them gives floor((H+2p−k)/s)+1. The width uses the same argument.
`correlate2d` rejects a kernel that does not fit instead of returning a misleading
empty feature map. Its tests use an independently padded matrix and exact
Fraction patch sums across128 shape/padding/stride cases.

Zero-padding inserts a boundary assumption. Circular padding instead wraps
indices modulo the input length. They model different worlds: the ends of an
ordinary photograph are not usually adjacent. We choose a ring below because
its shift property can be proved exactly without pretending boundaries disappear.

## The trained ring classifier

For n scalar inputs xᵢ on a ring, filter f has k shared weights w_fj and bias a_f.
Define

\[
 u_{fi}=a_f+\sum_{j=0}^{k-1}w_{fj}x_{(i+j)\bmod n},\quad
 h_{fi}=\tanh(u_{fi}),\quad
 z=b+\sum_f v_f q_f.
\]

The pooled q_f is either the mean of all h_fi or their maximum. Apply the binary
likelihood from [the preceding chapter](01_BINARY_LEARNING.md) to z. Parameters
are F(k+2)+1: Fk kernel weights, F biases, F readout weights and one output bias.
The trained example uses F=1,k=2, hence5 parameters. A flattened length12 logistic
model uses13. Fewer parameters are not automatically better; the meaningful
restriction is shared behavior at every location.

For x=(1,2,3), w=(1,2), a=0, the first preactivation is1×1+2×2=5, the next is
1×2+2×3=8 and the wrapped last is1×3+2×1=5. Apply tanh to obtain the feature map.
Without the nonlinear detector, composing shared linear correlation, mean pooling
and linear readout would remain a restricted linear function. It could not
manufacture arbitrary interactions just by adding more linear layers.

The receptive field of one activation is its k input indices. Two consecutive
stride1 widthk layers without dilation have receptive width2k−1, because the
second output combines k neighboring first-layer windows. With varying strides,
track both receptive width r and input jump j: initially r=j=1; a widthk layer
updates r←r+(k−1)j and j←sj. Circular wrapping can cause repeated physical input
indices when the receptive width reaches the ring length.

## Prove the actual symmetry

Define shift T_s x by (T_s x)ᵢ=x_(i+s mod n). Substitution into the kernel sum
shows h_fi(T_s x)=h_f,i+s(x). This is equivariance: the feature map shifts along
with the input. It is not yet invariance of individual feature coordinates.
A mean or maximum over all ring coordinates is unchanged by reindexing a finite
sum or maximum, so q_f(T_s x)=q_f(x), hence z(T_s x)=z(x). This final model is
exactly invariant to those circular shifts in real arithmetic. Float sums may
introduce tiny roundoff for mean pooling; tests use appropriate tolerances.

A local pooled window, a strided subsample, fixed coordinates or ordinary finite
boundaries need separate analysis. Equivariance does not imply robustness to
rotation, reflection, lighting, arbitrary crop or an adversarial input. Global
pooling also discards location information: it is unsuitable if the desired
output is the feature's precise position.

## Derive the reverse pass

Let d=σ(z)−y. For mean pooling,

\[
 \partial_b\ell=d,\quad
 \partial_{v_f}\ell=dq_f,\quad
 \delta_{fi}=\frac{d v_f}{n}(1-h_{fi}^2),
\]
\[
 \partial_{a_f}\ell=\sum_i\delta_{fi},\qquad
 \partial_{w_{fj}}\ell=\sum_i\delta_{fi}x_{(i+j)\bmod n}.
\]

The sum over positions is essential: the same parameter participates in many
operations. Updating once per location with partially changed weights would
execute a different algorithm. Compute all derivatives from the same forward
parameters, then update together.

For max pooling, replace1/n by an indicator for the selected maximizing index.
At a unique maximum this is the ordinary derivative. At a tie the maximum is
not generally differentiable; the code selects the first maximizing index as a
specified subgradient. Finite differences must use a test point away from a tie.
The ring classification data often contain repeated identical maximizing patches;
the tied patches have the same parameter derivative there, but that does not
make all max functions differentiable.

## What the controlled task establishes

Training rings contain exactly two ones. Label1 places them adjacent; label0
separates them by5 on a length12 ring. Train positions0,1,2 and evaluate positions
3…11. Sharing and global pooling guarantee that moving either complete pattern
does not change this CNN's score. The flattened baseline has no such guarantee.
This compares a structural assumption, not two systems equally optimized for a
natural-image benchmark. Test additional counts or noncircular boundaries
separately; success on these two motifs does not mean the detector understands
objects or all notions of adjacency.

A forward pass costs O(Fnk) operations and O(Fn) cached activations. The manual
reverse pass has the same order; parameters use O(Fk) storage. Scalar Python is
inspectable but slow compared with vectorized kernels. Real CNN operation adds
channels, batches, padding/dilation conventions, normalization, optimized layouts,
accelerator precision, data augmentation and deployment contracts. These are
unfinished extensions; this unit does not claim to reproduce LeNet or AlexNet.
