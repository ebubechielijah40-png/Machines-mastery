# Learning systems: fit, differentiate, predict and evaluate

This chapter connects developed numerical mechanisms to an actually trained
small causal decoder and a bounded retrieval/tool controller. It is not a
complete ML/AI coursebook: CNNs/RNNs, broad generative modeling, distributed
training, alignment, quantization and learned-agent production behavior remain
substantial unfinished scope.

## Begin with a declared fitting problem

Use [vectors/maps](../foundations/mathematics/core/03_VECTORS_MAPS.md) to construct
Ax and the residual r=Ax−b. The [calculus chapter](../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md)
derives the squared-loss gradient Aᵀr and shows why a correct direction can
still diverge with an excessive step. For a diagonal curvature4, fixed descent
requires α<.5. Data scaling changes the stability constraint; a library optimizer
does not remove it.

The [automatic differentiation](../16-machine-learning/03_AUTODIFF_BACKPROP.md)
implementation builds a scalar computation graph, propagates local derivatives
and accumulates shared paths. Finite-difference checks supply an independent
numerical diagnostic. Repeated backward behavior and leaf accumulation are
explicit contracts, not accidental leftover gradient state.

## Turn a numerical graph into a prediction mechanism

[Attention](../16-machine-learning/labs/DERIVATION.md) derives scores, masking,
softmax and local reverse derivatives before abstractions. The
[training unit](../16-machine-learning/training/README.md) then implements token
and position embeddings, a two-head causal block, residual paths, normalization,
feedforward computation, vocabulary logits, shifted next-token targets and SGD.
It actually trains548 parameters on a synthetic three-symbol pattern. Causal
masking prevents future input tokens influencing an earlier output; it does not
prevent leakage introduced by a bad train/evaluation split.

Cross-entropy uses log-softmax with a maximum shift to avoid raw exponential
overflow. A decreasing training NLL is evidence of fitting that objective,
not broad language competence. Held pattern phases, reversed patterns, a
contaminated evaluation and an excessive learning rate expose different failure
questions. Character and byte-pair tokenizers have explicit vocabularies and
boundaries; a model checkpoint does not silently include tokenizer state.

## Retrieval and actions introduce new contracts

The [retrieval/tool unit](../16-machine-learning/retrieval-agents/README.md)
builds a lexical index, constrained arithmetic executor and deterministic bounded
controller. Recall measures whether labeled evidence was retrieved; it does not
certify answer truth. Retrieved prose is data rather than a capability to call
a shell. The baseline is not an LLM planner or full generative RAG reproduction.
Its missing learned policy, authenticated identities and production memory limits
remain explicit.

Exit: derive a local gradient, reconstruct a causal attention result, train and
save the tiny model, freeze an independent evaluation, then reproduce a retrieval
miss and denied action. Explain exactly which observation supports each claim.
A short impressive generated sequence cannot substitute for that evidence.
