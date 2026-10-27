# Prerequisites and bridges

All tracks require Python lists, dictionaries, loops, functions, exceptions and tests. Explain the difference between a specification and the code being tested. Run a script from the repository root and find its raw output before attempting a benchmark.

For causal clocks, read [sets, relations and invariants](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md). Entry check: given A→B and B→C, list the transitive pair A→C; explain why an unrelated D remains incomparable. No physical-clock synchronization formula is needed.

For Fourier factorization, read [vectors and inner products](../../foundations/mathematics/core/03_VECTORS_MAPS.md), then this bridge. Define i²=−1, conjugate(a+bi)=a−bi, and magnitude²=a²+b². Complex multiplication rotates and scales: `(a+bi)(c+di)=(ac−bd)+(ad+bc)i`. Euler's identity `exp(iθ)=cosθ+i sinθ` locates a unit vector at angle θ. For N=4, positive-sign roots are 1,i,−1,−i. Their sum is zero because horizontal and vertical components cancel. General roots satisfy w^N=1 and, for w≠1, `(1−w)(1+w+...+w^(N−1))=1−w^N=0`. This finite sum is the cancellation behind orthogonal Fourier coefficients. Entry check: `(1+i)(1−i)=2`; then derive the four-point transform in F1.

For task publication, distinguish a logical shard ID from an attempt ID. Entry check: two attempts each reporting 3 for the same shard contribute 3, not 6, if the shard is represented once. An empty published result is a completed task; a failed attempt that never publishes is different.

For the privacy extension, start with [probability and inference](../../foundations/statistics/probability-inference/README.md), then the [privacy dossier](../../research-paper-reconstruction/domains/privacy/01_dwork_differential_privacy_2006.md). A density is not the probability of one exact continuous output; interval probability is a density integral. Entry check: integrate `(1/(2b)) exp(−|z|/b)` over the real line to obtain one. No private records are needed.

If an entry check fails, do the bridge by hand and explain the result before continuing. A passed reference suite does not substitute for the prerequisites.
