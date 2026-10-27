# Machine Learning, Generative AI, and Agent Systems

This track is about understanding learning machines from the numbers upward. The destination is not “call an API.” It is the ability to explain, implement, test, train, serve, break, and evaluate progressively more capable models—from linear regression to a small Transformer and a tool-using agent.

## Executable progression now supplied

The [scalar-to-trained-decoder build](training/README.md) connects graph derivatives,
XOR optimization, tokenization, embeddings, multi-head causal attention, a full
small next-token training loop, generation and controlled evaluation. It includes
actual synthetic training output and independent gradient tests. Its narrow
capability does not complete every later field in this route.

## Route

1. [Mathematical bridge](01_MATH_BRIDGE.md)
2. [Classical machine learning](02_CLASSICAL_ML.md)
3. [Automatic differentiation and backpropagation](03_AUTODIFF_BACKPROP.md)
4. [Optimization](04_OPTIMIZATION.md)
5. [Neural networks](05_NEURAL_NETWORKS.md)
6. [Convolutional networks](06_CNNS.md)
7. [Sequence models](07_SEQUENCE_MODELS.md)
8. [Attention](08_ATTENTION.md)
9. [Transformers](09_TRANSFORMERS.md)
10. [Tokenization and embeddings](10_TOKENIZATION_EMBEDDINGS.md)
11. [Language modeling](11_LANGUAGE_MODELING.md)
12. [Generative models](12_GENERATIVE_MODELS.md)
13. [LLM training and scaling](13_LLM_TRAINING_SCALING.md)
14. [Inference and serving](14_INFERENCE_SERVING.md)
15. [Fine-tuning and alignment](15_FINETUNING_ALIGNMENT.md)
16. [Retrieval-augmented generation](16_RAG.md)
17. [Agents and tool use](17_AGENTS.md)
18. [Evaluation, reliability, and security](18_EVALUATION_SECURITY.md)
19. [Production AI systems](19_PRODUCTION_AI.md)
20. [Projects and mastery gates](20_PROJECTS.md)

The central chain is:

```text
numbers → parameters → differentiable computation → loss → gradients
→ optimization → representation learning → attention → Transformer
→ next-token prediction → generation → retrieval/tools → agent loop
```

Every layer should be understood as a mechanism, not a brand name.

## Developed model-family progression

After calculus and probability, derive [binary learning → local kernels → recurrent state → explicit probability generation](model-families/README.md). Continue through checked autodiff and the trained decoder. Preserve shortcut, distractor, initialization and generation-memory failures; modern generative families and large-scale training remain further work.
