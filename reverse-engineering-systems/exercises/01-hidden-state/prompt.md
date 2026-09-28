# Discover a machine from its interface

PREPARED; learner NOT STARTED. Required: [state reasoning](../../../foundations/mathematics/state-and-logic/README.md) and [counting](../../../foundations/mathematics/counting-and-units/README.md). No physics, electronics, chemistry or statistics is needed for this deterministic synthetic interface. Programming is optional during discovery; implementing a replica requires a language you can use and the local foundations first.

You have commands reset, up, down and peek; each valid command returns a nonnegative integer. Invalid commands return ERROR. You are not given update rules, a state diagram or implementation. Query the oracle through [the runner](README.md). You may assume the interface is deterministic within one process, not that each command is stateless. Do not assume two outputs imply the same internal state without testing histories.

Before your first query, propose at least three models. Use at most 20 discovery commands, writing each prediction before execution. Spend queries on disagreement between models. Record command, history, predicted outputs under each model, actual result and revised confidence. A new session may be used as a controlled reset of the entire process; count these resets in your log.

Deliver: a behavioral model, state diagram or table, unresolved alternatives, a distinguishing sequence for every eliminated model, an independent replica with matching command/error behavior, and withheld tests selected before revealing the source. Explain why matching observations cannot prove identical internal implementation.

Five easy tasks: distinguish input/output; identify session boundary; record one reset; repeat peek; distinguish observation from interpretation. Three intermediate tasks: test history dependence; identify a boundary rule; test invalid-command state effects. Hard task: construct the smallest behavioral-state model justified by distinguishing future sequences. Experiment: use a predicted disagreement to reject a model, then revise. Transfer: a related oracle may return a pre-update value or use a different reset state; design probes rather than reusing an assumption.

Only after your saved attempt use [hints](hints/README.md), then retry. The reveal is linked there, not included in this prompt. Evaluation rewards evidence and model revision, not guessing quickly.
