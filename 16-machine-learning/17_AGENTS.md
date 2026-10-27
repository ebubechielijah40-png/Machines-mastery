# 17 — Agents and tool use

An agent is best treated as a control loop around a model, not as mystical autonomy.

```text
observe state
→ decide next action
→ call tool / mutate environment
→ receive result
→ update working state
→ repeat until stop condition
```

## Components

- **policy/model** chooses actions or intermediate reasoning representations;
- **tools** expose constrained actions such as search, code execution, database queries, or APIs;
- **state/memory** stores observations and task progress;
- **planner** may decompose goals into subgoals;
- **executor** validates and invokes actions;
- **verifier** checks whether claimed progress matches environment state;
- **stop policy** prevents endless loops.

## Tool calling

Tool schemas are interfaces. The model proposes structured arguments; the runtime validates and executes them. Never treat model-generated arguments as trusted input. Apply authorization, schema validation, rate limits, and least privilege.

## Memory

Working memory, episodic logs, retrieval memory, and durable user/profile memory solve different problems. More memory is not always better: stale, poisoned, irrelevant, or sensitive context can make the system worse.

## Agent failure modes

- loops without progress;
- claiming an action succeeded without checking;
- planning with stale state;
- tool injection / malicious retrieved instructions;
- privilege escalation through overpowered tools;
- compounding small errors over long horizons;
- irreversible actions without confirmation.

## Build

Construct a local file-organizing agent with a tiny explicit state machine. Start without an LLM: deterministic planner + tools. Then replace one decision component with a model. Add a verifier that checks filesystem state after every action. Inject failures and measure recovery.

## Multi-agent systems

Multiple agents add communication protocols, duplicated work, conflict resolution, shared-state consistency, and attribution. They do not automatically increase intelligence. Compare one-agent and multi-agent designs on the same task before claiming benefit.

## Executable constrained controller

[Build the local evidence agent](retrieval-agents/README.md) before attaching a
learned policy. Its executor accepts only search, bounded arithmetic and finish,
checks exact argument fields, and records actions/observations under a finite
step budget. The arithmetic tool walks a restricted syntax tree; it never calls
`eval`. A retrieved string that asks for a shell command remains document text.
Unknown shell actions are rejected by the executor rather than interpreted.

Tests inject malformed proposals, misleading evidence, a missing finish step,
unknown vocabulary and independent session labels. Labels separate local histories
without authenticating a user; total session storage is not globally bounded.
These bounded results verify this deterministic controller, not LLM prompt
injection resistance or successful autonomous planning. Source scope, actual
results, exercises, hints and solutions live beside its implementation.
