# State, functions and transition tables

PREPARED; learner NOT STARTED. Unit F-STATE. Original explanation and derivation; see [foundation policy](../../README.md).

A machine may react differently to the same button because earlier actions matter. We call the retained distinction state. Write q for state, u for input and q_next=T(q,u) for the transition rule. A function assigns one result to every allowed input tuple. The subscript “next” distinguishes a later value from the current one; it is not multiplication. A table can specify the function without an equation.

Consider an explicitly invented two-position marker. On input toggle it swaps positions; on hold it stays. With states 0 and 1, toggle gives 0→1 and 1→0; hold gives 0→0 and 1→1. The four pairs exhaust this model. An output may show current q or the new q; the interface must specify which. Two states are behaviorally distinguishable when some future input sequence produces different observable outputs.

```text
current q + chosen input -> transition rule -> next q
       |                                  |
       +----------- observation ----------+
```

A Boolean is a two-valued proposition, false/true. AND is true only if both propositions are true, OR if either is true, NOT reverses the value. A condition selects a rule; it does not automatically supply a physical gate. Priority matters: “if reset, zero; else if enable, toggle; else hold” makes reset win when both are true. Swapping the first two cases changes the machine.

An invariant is a property preserved by every allowed transition. For the two-position model, q belongs to {0,1}: it holds initially and each table row preserves it. This two-step argument is induction over executed steps. A time trace adds ordering, but logical steps alone specify no seconds. A continuous signal can change between observations; our table does not model that.

Wrong: passing one input proves absence of state. Correct: repeat it after different histories. Edge: initial q unknown means both outcomes remain possible until a reset or observation distinguishes them. Transfer: a file cursor can make repeated reads differ although the requested length is unchanged.

Study [problems](problems/README.md), then [hints](hints/README.md) after an attempt. [Solutions](solutions/README.md) are separate. Complete the [experiment](experiments/README.md) and transfer before returning to the dependent unit.
