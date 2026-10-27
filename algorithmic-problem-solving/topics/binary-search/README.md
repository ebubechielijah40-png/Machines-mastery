# Binary Search — problem-solving model

## Why this pattern exists
This topic addresses problems that need **find a boundary in monotonic state**. Do not memorize a syntax pattern; identify the property that makes this representation or algorithm appropriate.

## Core invariant
Loop invariant over candidate interval. The invariant is what must remain true after every iteration/operation. If you cannot state it, you do not yet understand the solution.

## Derivation workflow
1. Write the brute-force search space and its cost.
2. Identify repeated work or structure.
3. Choose the minimum state needed to avoid that repeated work.
4. State the invariant before coding.
5. Prove termination/correctness on a tiny case.
6. Derive time and space complexity from counted operations, not memory.
7. Test empty, singleton, duplicate, extreme, adversarial, and large inputs.

## Real systems
Applications include indexes, capacity thresholds, version search. The production version may care about cache locality, allocation, concurrency, input distribution and constant factors in addition to asymptotic complexity.

## Experimental task
Implement a naive and improved solution for one representative problem. Generate increasing input sizes, measure runtime and memory, and compare empirical growth to the predicted complexity. Explain where constant factors or hardware effects make small-n results differ from asymptotics.

## Mastery gate
Solve the topic's problem set without opening solutions first. For at least three problems, give a correctness argument and design a changed constraint that breaks your original solution.
