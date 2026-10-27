# Learning-machine exercises

Attempt before opening HINTS/SOLUTIONS. Retain original calculations and code.

1. Differentiate `(x*x+1)^2` at x=3 by local graph edges, accounting for both
   appearances of x. What changes when backward seed is2?
2. A four-element vector has entries[2,2,2,2]. Compute the normalized vector
   with ε=10^-5. Why does this not divide by zero?
3. Multiply one-hot[0,1,0] by rows[[1,2],[3,4],[5,6]]. Which row receives
   gradient when the output is summed?
4. With d=8 and heads2, list query/key/value/head-concatenation/output shapes
   for three input tokens. Count permitted score pairs across both heads.
5. For logits[ln2,ln3] and target1, compute probabilities, loss and both gradients.
6. Rebuild the XOR MLP. Prove why composing affine layers without nonlinearities
   cannot solve the four signed rows, then test one failed linear baseline.
7. Add independent finite differences for three embedding/position coordinates
   and one attention projection parameter. Vary h across three orders of magnitude.
8. Encode an unfamiliar Unicode string with character and byte-pair tokenizers.
   Compare roundtrip, unknown behavior and count; do not call count model quality.
9. Explain why two calls to backward on one graph must clear internal adjoints
   even when the caller wishes to accumulate leaf gradients across microbatches.
10. A causal mask passes a future-mutation test, but a training script uses each
    current input token as its own label. What task is being optimized? Design a
    test that catches it without requiring model training.
11. Challenge: derive the derivative of mean loss with respect to a shared
    embedding row used at multiple positions. Explain why separate copies of
    numeric rows would produce an incorrect parameter-update interface.
12. Experiment: reproduce the clean/contaminated/high-rate protocols. State what
    is controlled, save actual output, and explain why a lower contaminated
    held-set score does not improve the evidence of generalization.
13. Reconstruction/transfer: close the code and build a two-head decoder with
    vocabulary4,width4,context3. Supply a hand CE oracle, causal/gradient tests,
    tokenizer identity, actual training log and one transfer distribution that
    fails. Explain which behavior would require a larger model versus better data.
