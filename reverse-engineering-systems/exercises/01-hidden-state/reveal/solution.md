# Reveal: bounded state with saturating transitions

The reference stores one of four positions, initially zero. Up adds one unless already three; down subtracts one unless already zero; reset sets zero; peek leaves it unchanged. Invalid input reports ERROR and preserves state. Valid commands report the post-command state. Exact command spelling matters; the runner removes the newline, not arbitrary surrounding spaces.

Competing models include unbounded addition, modulo-four wrapping and bounded saturation. From reset, four up commands distinguish their fourth outputs: 4, 0 and 3 respectively. A down from reset distinguishes unsigned wrapping from lower saturation. Invalid input between two peeks tests error atomicity. These are proposed discriminating tests; the learner must preserve their actual queries and results.

The four states are behaviorally distinct because peek produces different outputs. A transition table with four rows per command is a functional replica, shown in [replica.py](replica.py); the branch-based oracle is [machine.py](machine.py). Agreement does not prove either is the unique original architecture: many representations implement the same observable machine. Correctness of the table follows by comparing each allowed state/command pair; induction over history then extends agreement to arbitrary finite histories under the deterministic interface contract. ERROR preserves both states.

State is logically two bits, though Python object overhead is larger and unmeasured here. Each query uses bounded work in this four-state model. Timing and allocation differences between the replicas are not part of the contract. An alternative that logs commands externally may match values but introduces additional state not observable through this interface.

Debugging exercise: replace upper saturation with wraparound and rerun the distinguishing sequence. Reconstruction drill: close this directory and recover the state table from your evidence alone. Transfer requires a fresh related oracle prepared by an assessor; none is falsely claimed to exist.
