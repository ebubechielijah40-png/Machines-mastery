# 18 — Evaluation, reliability, and security

Evaluation is an experimental-design problem. A single benchmark score compresses choices about task distribution, labels, contamination, judge reliability, sampling settings, and aggregation.

## Evaluation layers

1. unit behavior: does the component obey local invariants?
2. capability: can the system perform a defined task?
3. robustness: what happens under perturbation/shift?
4. calibration: do stated probabilities/confidence align with frequencies?
5. safety/security: can untrusted input alter control flow or leak data?
6. operations: does the service meet latency/error/cost objectives?

## Prompt injection

If retrieved or user-controlled text can influence an agent's tool policy, data and instructions occupy the same channel. Treat external content as untrusted data, enforce tool authorization outside the model, and constrain actions at the runtime boundary.

## Data poisoning

Training/fine-tuning/retrieval corpora are inputs to system behavior. Attackers or accidents can insert examples that create targeted or broad failures. Provenance, validation, deduplication, anomaly analysis, and post-training evaluation matter.

## Model extraction/privacy

APIs can leak information through outputs, timing, memorized training examples, or overly detailed errors. Security analysis therefore spans model, serving layer, logging, access control, and data lifecycle.

## Test assignment

Design a red-team suite for the local RAG/agent project. Include prompt injection, malformed tool arguments, inaccessible files, poisoned documents, infinite-loop pressure, and contradictory evidence. Report failures separately from mitigations.
