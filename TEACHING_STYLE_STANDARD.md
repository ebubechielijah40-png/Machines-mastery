# Teaching style standard

Every learner-facing unit should be understandable without prior exposure to the topic, while still reaching technical depth.

## Required explanation layers

1. **Problem first:** what real limitation/question made this idea necessary?
2. **Plain-language model:** explain without jargon.
3. **Concrete example:** use actual values, bytes, packets, records, voltages, sequences, or states.
4. **Mechanism:** trace internal transitions step by step.
5. **Formal model:** equations, algorithm, state machine, type/system rule, or circuit model.
6. **Implementation:** executable or simulatable version where feasible.
7. **Failure:** edge cases, counterexamples, malformed input, scale, noise, or adversarial conditions.
8. **Experiment:** prediction before observation; actual output kept separate from expectation.
9. **Production/physical reality:** what the teaching model omits.
10. **Transfer:** apply the idea to an unfamiliar system.

Terms must be defined at first use. Equations must define symbols and units. Diagrams must explain arrows/state. Code must explain why it works, not only what each line says.
