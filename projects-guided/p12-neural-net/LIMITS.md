# Scope and failure boundaries

The scalar engine is an educational real-valued graph with finite Python floats.
It does not implement tensors, GPU kernels, arbitrary numeric ranges, distributed
execution or general differentiation through mutation/control flow. Captured
forward operands make local derivatives repeatable; they do not make an old
forward graph represent newly updated parameters. Rebuild after each update.

The MLP fits a complete four-row synthetic truth table. A seed and successful
loss trace do not guarantee all widths, initializations or learning rates work.
Saturation can shrink gradients. Finite differences check only chosen points
and become unreliable at poor step sizes or unsupported derivative domains.

The connected decoder has one small block, a three-symbol experiment vocabulary
and four-token context. Its shifted-pattern failure and contaminated evaluation
are documented rather than hidden. It establishes no natural-language competence,
physical intelligence, factual reliability, alignment or large-model capability.
Tokenizer identity, training split and model state jointly determine an experiment.

No service, authorization, concurrent training, checkpoint authenticity, resource
scheduling or hardware fault recovery is supplied. A prepared reference is useful
for review and comparison; learning still requires unaided derivation/build/transfer.
