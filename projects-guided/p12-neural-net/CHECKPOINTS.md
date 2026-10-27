# Checkpoints with falsifiable acceptance conditions

1. **Values and invariants.** At x=3, u=x*x+1=10 and L=u*u=100. Leaves have no
   operation parents; every operation retains the information its local derivative
   needs. Parameters must be finite. Explain why final answers alone lose dependencies.
2. **Shared paths.** Implement x*x so both operands contribute. d(x*x)/dx=2x.
   At x=0 it is0. For a constant exponent0, document the API's constant-one rule
   and zero derivative; reject unsupported real derivative domains explicitly.
3. **Traversal and repeatability.** Seed the scalar output with1. Consumers are
   visited before their operands during reverse traversal. Two default backward
   calls on the same graph agree. Explicit microbatch accumulation adds leaf
   gradients while clearing intermediate values. Test different scalar roots.
4. **Independent oracle.** Central differences rebuild the numerical forward
   evaluation at w+h and w-h. Use h near1e-5, then vary h; cancellation and
   truncation can both matter. Do not compare an implementation to itself.
5. **Nonlinear model.** For two inputs and h hidden units, count3h hidden-layer
   parameters and h+1 output parameters:4h+1 total. At h=4 this is17. Explain
   each affine sum, tanh and shared parameter before training.
6. **Optimization.** Use all four XOR rows, mean squared error, seed7 and SGD.1.
   Rebuild the loss graph after every update. Save initial/final loss and every
   prediction; all four rows are training data, so a successful fit is not an
   independent generalization result.
7. **Failure and transfer.** Replace a local += with assignment and construct a
   branching counterexample. Change hidden width or labels, predict the effect
   and rerun. Keep expected predictions separate from observations.
8. **Reconstruction.** With references closed, implement an equivalent learner,
   derive gradients, and explain failed settings. Progress to shifted next-token
   prediction only when the scalar parameter-to-objective path is clear.
