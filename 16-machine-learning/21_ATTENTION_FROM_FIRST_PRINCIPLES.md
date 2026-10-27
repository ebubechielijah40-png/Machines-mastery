# Why a language model needs attention: a worked reconstruction

**Status:** original learner-facing explanation with runnable reference implementation. Not a reproduction of an entire source book or an exhaustive account of Transformer variants.

## 1. The problem before the formula

Consider the sentence `The robot picked up the battery because it was empty.` To predict subsequent words, a model may need information about different earlier words, depending on context. A fixed-window or single compressed summary limits how directly one position can access another. Attention allows each query position to compute a *content-dependent weighted mixture* of representations at other positions. In a causal language model it may only inspect current and previous tokens, never future tokens.

The mechanism is not human attention, consciousness, or a database lookup. It is a differentiable numerical operation. The model must learn projection matrices and many other parameters through training; an untrained attention layer does not automatically understand pronouns or semantics.

## 2. Required mathematics (with numbers)

A vector is an ordered list of numbers. The **dot product** multiplies matching entries and sums: `[1,2] · [3,4] = 1×3 + 2×4 = 11`. It measures algebraic alignment, but raw size also affects the score; it is not automatically cosine similarity. A matrix multiplication can make a new vector whose entries are learned weighted combinations of old entries. A *probability distribution* consists of nonnegative weights summing to one.

`softmax([a,b]) = [exp(a)/(exp(a)+exp(b)), exp(b)/(exp(a)+exp(b))]`. A stable implementation subtracts the maximum score from every input first; doing so leaves the ratios unchanged. For scores `[0, ln(3)]`, softmax is `[1/4, 3/4]`. This conversion produces weights, not verified probabilities of factual truth.

## 3. The full operation

Let token vectors be rows of a matrix `X` (sequence length `n`, model width `d_model`). Multiply by learned projection matrices: `Q = X W_Q`, `K = X W_K`, `V = X W_V`. For a single head, `Q` and `K` have width `d_k`; `V` has width `d_v`.

Score query position `i` against key position `j` with `s_ij = (q_i · k_j)/sqrt(d_k)`. In causal self-attention, forbid `j > i` before softmax, typically with a conceptual `-infinity` mask. The remaining softmax values `a_ij` sum to one for each row. Output `o_i = sum_{j<=i} a_ij v_j`.

```text
Token vectors X
    │
    ├── W_Q ── Q ──┐
    ├── W_K ── K ──┴─ dot-product scores ─ causal mask ─ softmax ─┐
    └── W_V ── V ───────────────────────────────────────────────────┤
                                                                    ↓
                                                       weighted sum of V
                                                                    ↓
                                                           token outputs
```

## 4. Derive the two-token example by hand

Take `x0 = [1,0]`, `x1=[0,1]`. Use identity matrices for all three projections and temporarily omit scaling to keep arithmetic clear. The first position can attend only to itself. Thus `a_00=1`, `o0=[1,0]`. The second query `[0,1]` gets scores `s_10=0` and `s_11=1`. Their weights are `1/(1+e)` and `e/(1+e)`; approximately `0.269` and `0.731`. Hence `o1 = 0.269[1,0] + 0.731[0,1] = [0.269,0.731]`.

Now restore scaling for `d_k=2`: the second score becomes `1/sqrt(2)`, so the self-weight becomes approximately `0.670`, not `0.731`. This is a deliberate change in the sharpness of the distribution. For larger head width, the dot-product variance can grow under common initialization assumptions; scaling helps control that growth. The assumptions matter: scaling does not guarantee stable training in every architecture.

## 5. What does the mask actually enforce?

Suppose tokens are `A B C`. Output `o_A` may depend on `A`, but not on `B` or `C`. `o_B` may depend on `A` and `B`, not `C`. `o_C` may depend on all three. Changing the future token must not change earlier outputs **for this isolated causal layer**, given the same earlier input vectors. A causal mask implements this property. If code calculates attention over all keys and only zeroes future probabilities *after* softmax without renormalizing, it is wrong: forbidden positions have already taken some probability mass.

## 6. Why values differ from keys

Keys determine relevance scores with queries; values are the payloads mixed into the output. Make `W_V` the zero matrix: all outputs become zero even when the softmax scores are highly nonuniform. Conversely, setting keys all to zero makes permitted positions equally weighted, but does not force values to zero. This separation permits a learned routing mechanism and a separately learned representation of transmitted content.

## 7. Model-level context

A decoder Transformer typically includes token embeddings; positional information (without it, attention alone is permutation-equivariant); multi-head self-attention; residual connections; normalization; and feedforward/MLP transformations. Multiple heads are not necessarily semantic labels such as "grammar" or "facts". They are parameterized projections whose behavior depends on training. Layers are stacked and trained using a loss function, commonly next-token cross-entropy. The loss sends gradients through attention and projection matrices via backpropagation.

At training time, a known token sequence permits many prefix predictions to be computed in parallel under the causal mask. During *autoregressive generation*, the next token is unknown until generated, so decoding proceeds sequentially across token positions; a KV cache avoids recomputing some previous key/value projections. Cache memory usually grows with active sequence length, layer count, head layout and batch size, though specific architectures such as grouped-query attention change constants.

## 8. Complexity, production and constraints

Dense full attention computes roughly `n×n` pairwise interactions for sequence length `n`, giving quadratic interaction count. The head-width factors and fused kernels determine actual memory and runtime. A simple implementation materializing all scores costs quadratic memory; some optimized exact kernels avoid materializing the full attention matrix and can reduce memory, without removing the quadratic number of pairwise interactions. Different architectures may have different costs.

Production challenges include padding masks, batching, variable-length sequences, KV-cache eviction/position accounting, latency at long contexts, quantization error, numerical stability and prompt-injection risks in surrounding applications. Attention itself does not enforce honesty, knowledge provenance, access control, or safe tool use.

## 9. Counterexample and debugging

**Broken implementation:** compute `softmax` over all `n` scores, then set masked weights to zero. For `[0,0,20]` with token `2` in the future, most mass goes to position `2` and is then discarded, leaving the row sum near zero instead of one. The fix is to exclude future scores (or set them to negative infinity) **before** softmax.

**Broken mathematical intuition:** assume a large attention weight means the model believes a statement is true. No: the weight is an internal routing coefficient. An output might be misleading even when a weight is large.

## 10. Assignments and checkpoints

- **Basic:** calculate dot products `[1,0]·[0,1]` and `[2,1]·[3,-1]`; explain the scalar results.
- **Basic:** calculate softmax for two equal scores without a calculator.
- **Basic:** show a three-position causal mask as allowed/forbidden pairs.
- **Applied:** derive the two-token attention output above and compare it with the executable implementation.
- **Applied:** change `W_K` so that the first token gets more weight from the second query; show the scores.
- **Applied:** explain why changing `W_V` cannot change the *attention weights* in an isolated layer but can change outputs.
- **Reasoning:** predict whether changing a future token can affect `o0`, then test it.
- **Reasoning:** explain why softmax should be numerically stabilized.
- **Challenge:** implement multi-head attention with concatenation and projection, preserving correct masking; write shape and no-lookahead tests.
- **Experiment:** vary sequence length and measure cost; report timings without assuming they match asymptotic trends for tiny cases.
- **Transfer:** design attention over a stream of sensor readings where causal leakage would be unacceptable. Define the information boundary and tests.

**Solutions / self-check:** first three: `0`, `5`; equal softmax outputs each `0.5`; allowed keys for queries `0,1,2` are `[0]`, `[0,1]`, `[0,1,2]`. See code and tests for applied checks. For remaining problems, show your derivation and use the tests as evidence; open a solution only after an attempt.

## 11. What the experiment can and cannot prove

Unit tests verify local implementation properties on selected small inputs, including row normalization and causal nonleakage. They cannot establish that an entire deployed model is free from information leakage, that a training run converges, or that attention "understands" language. Comparing measured runtime on one computer does not prove a universal performance claim. Deliberately distinguish mathematical derivation, test evidence, and external research results.

## 12. Attribution and source trail

This is an original instructional derivation of standard scaled dot-product attention. Its historical research source is Vaswani et al., *Attention Is All You Need* (2017), arXiv:1706.03762. Check the paper when you need the authors' exact architecture, experiments and comparisons; do not attribute this educational toy code to their original implementation. Additional concepts in this unit (KV caching and serving concerns) reflect subsequent engineering practice, not experiments reproduced here.

**Continue:** [Run the lab](labs/README.md), then attempt a from-memory implementation and compare numerical outputs.
