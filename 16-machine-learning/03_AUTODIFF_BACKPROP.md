# 03 — Automatic differentiation and backpropagation

Backpropagation is not “the neural-network algorithm.” It is an efficient way to compute derivatives of a composed computation by repeatedly applying the chain rule from outputs back to inputs.

## Computational graph

For

`a = x*w`
`b = a + c`
`L = b^2`

we can draw nodes for primitive operations. The forward pass stores values. The reverse pass starts with `dL/dL = 1` and propagates local derivatives backward.

At `L=b^2`, `dL/db=2b`. At `b=a+c`, `db/da=1`. Therefore `dL/da=(dL/db)*(db/da)`. At `a=xw`, `da/dw=x`, so `dL/dw=(dL/da)*x`.

The reason reverse mode is powerful for neural networks is dimensionality: one scalar loss depends on millions of parameters. Reverse mode computes all parameter gradients in work proportional to a small multiple of the forward computation.

## Accumulation matters

If a value influences the loss through two paths, its derivative is the sum of contributions from both paths. A toy autodiff engine that overwrites gradients instead of accumulating them is wrong for branched graphs.

## Numerical gradient checking

For parameter `w`, finite difference estimates

`(L(w+h)-L(w-h))/(2h)`.

This is slower and numerically imperfect but useful for checking analytic/autodiff gradients on small models.

## Failure modes

- vanishing gradients: repeated local derivatives below 1 shrink signals;
- exploding gradients: repeated amplification creates unstable updates;
- nondifferentiable points: frameworks choose subgradient conventions for some operations;
- stale graph/state: mutating values between forward and backward can invalidate reasoning;
- numerical precision: underflow/overflow can break mathematically sound expressions.

## Build

Implement `Value` objects with `data`, `grad`, parent references, and a local backward closure. Support `+`, `*`, power, `tanh` or ReLU. Topologically sort the graph, seed the final gradient with 1, and execute reverse callbacks.

## Experiments

1. Compare autodiff gradients with finite differences for random tiny expressions.
2. Create a branched graph and intentionally replace `+=` with `=` in gradient accumulation; find the failure.
3. Stack repeated sigmoid/tanh operations and measure gradient magnitude with depth.
4. Compare ReLU and tanh gradient behavior on the same deep toy network.

## Executable contract and an important repaired edge

The supplied [scalar engine](code/autodiff.py) uses a topological traversal and
captures local operands at forward time. For `u=x*x+1; L=u*u` at x=3, the reverse
pass gives `dL/dx=2*10*2*3=120`. Default `L.backward()` resets every reachable
adjoint, so repeating it gives120 again. Explicit `accumulate=True` adds only
the new leaf gradients to prior leaf gradients; intermediate adjoints still
reset. Leaving old intermediate values in place would silently corrupt later
passes. Update parameters only after the pass and rebuild the next forward graph.

[The complete training lesson](training/README.md) derives this example,
nonlinear XOR, embedding lookup, causal attention, stable cross-entropy and SGD.
[Tests](code/test_autodiff.py) compare an independent finite-difference expression,
shared branches, repeated/different roots, forward operand capture, invalid
domains and a graph deeper than Python's recursion limit. Run from repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/code -p test_autodiff.py -v
python3 -m unittest discover -s 16-machine-learning/training -v
```

These checks support the stated scalar API. They are not proof that arbitrary
nondifferentiable programs, extreme numeric ranges or every possible graph is
handled. See separate [exercises](training/EXERCISES.md), [hints](training/HINTS.md)
and [solutions](training/SOLUTIONS.md) before using the reference.
