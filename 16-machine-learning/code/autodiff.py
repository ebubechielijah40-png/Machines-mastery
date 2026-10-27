"""Original scalar reverse-mode engine for bounded teaching builds.

Each backward call resets reachable graph gradients. accumulate=True preserves
only prior *leaf* gradients; internal adjoints never leak across traversals.
Parameters are mutable scalar Values; rebuild a forward graph after updates.
"""
import math


def _number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError('scalar values must be finite')
    return value


class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = _number(data)
        self.grad = 0.0
        self._prev = tuple(_children)
        self._op = _op
        self._backward = lambda: None

    @staticmethod
    def wrap(other):
        return other if isinstance(other, Value) else Value(other)

    def __add__(self, other):
        other = self.wrap(other)
        out = Value(self.data + other.data, (self, other), '+')
        def backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = backward
        return out
    __radd__ = __add__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -self.wrap(other)

    def __rsub__(self, other):
        return self.wrap(other) + -self

    def __mul__(self, other):
        other = self.wrap(other)
        left, right = self.data, other.data
        out = Value(left * right, (self, other), '*')
        def backward():
            self.grad += right * out.grad
            other.grad += left * out.grad
        out._backward = backward
        return out
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, Value):
            raise TypeError('power must be a constant scalar')
        power = _number(power)
        base = self.data
        if base == 0 and power < 1 and power != 0 or base < 0 and not power.is_integer():
            raise ValueError('power outside this real scalar domain')
        out = Value(base ** power, (self,), '**')
        local = 0.0 if power == 0 else power * base ** (power - 1)
        def backward():
            self.grad += local * out.grad
        out._backward = backward
        return out

    def __truediv__(self, other):
        return self * self.wrap(other) ** -1

    def __rtruediv__(self, other):
        return self.wrap(other) * self ** -1

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')
        def backward():
            self.grad += (1-t*t) * out.grad
        out._backward = backward
        return out

    def exp(self):
        out = Value(math.exp(self.data), (self,), 'exp')
        def backward():
            self.grad += out.data * out.grad
        out._backward = backward
        return out

    def log(self):
        if self.data <= 0:
            raise ValueError('log requires positive scalar')
        base = self.data
        out = Value(math.log(base), (self,), 'log')
        def backward():
            self.grad += out.grad / base
        out._backward = backward
        return out

    def backward(self, *, seed=1.0, accumulate=False):
        """Reverse one DAG. Default replaces all reachable adjoints.

        Explicit accumulate=True adds this pass to prior leaf adjoints only.
        Iterative postorder avoids recursive traversal depth limits.
        """
        seed = _number(seed)
        topo, seen, stack = [], set(), [(self, False)]
        while stack:
            v, ready = stack.pop()
            if ready:
                topo.append(v)
            elif v not in seen:
                seen.add(v)
                stack.append((v, True))
                stack.extend((c, False) for c in reversed(v._prev))
        old = {v: v.grad for v in topo if not v._prev} if accumulate else {}
        for v in topo:
            v.grad = 0.0
        self.grad = seed
        for v in reversed(topo):
            v._backward()
        for v, grad in old.items():
            v.grad += grad
        return self
