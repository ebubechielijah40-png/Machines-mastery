# Progressive hints

Use one hint, return to the exercise, and retain your attempt before opening [solutions](SOLUTIONS.md).

| Exercise | First hint | Stronger hint |
|---|---|---|
| L1 | list local edges before message edges | the five-event chain has 5×4/2 ordered pairs; u contributes none |
| L2 | check the send→receive edge directly | both events can receive the same value if strict increment is omitted |
| L3 | a trace asserts identities and endpoints, not just times | a send can be real even if no receive appears in the observed prefix |
| L4 | separate sorting known events from knowing that the prefix is complete | absence of an earlier request in a log is not evidence it cannot arrive |
| L5 | search paths in one function and update per-process counters in the other | compare relation pairs only after both outputs have been computed |
| F1 | roots for length four are 1,i,−1,−i | even input `[1,3]` and odd input `[2,4]` produce two length-two sums |
| F2 | every stage processes n/2 butterflies | there are log2(n) stages; one butterfly has one value multiplication and two additions |
| F3 | use an input whose frequency has a known index | choose x[j]=exp(−2πij/n) for the positive-sign target |
| F4 | polynomial degrees add | the last coefficient belongs at index two, not zero |
| F5 | doubling adds a stage and doubles values per stage | root generation and interpreter/allocation overhead are absent from the value count |
| M1 | key winners by logical task, not attempt | a duplicate attempt does not introduce a new summand |
| M2 | distinguish no dictionary entry from an entry containing an empty map | accepted data must be an owned snapshot |
| M3 | averages discard denominators | merge totals and counts before dividing once |
| M4 | locate the notification relative to output acceptance | durable deduplication must cover the same logical operation across retries and restart |
| D1 | normalizers cancel in the density ratio | log ratio is `(abs(y−1)−abs(y))/b` |
| D2 | use b=Δ/ε and integrate each half-line | the tail probability outside ±t is exp(−t/b) |
| D3 | count how many bins change | an added person changes one coordinate; a moved person changes two |
| D4 | solve the CDF separately on each side of zero | a logarithm reaches negative infinity at a uniform endpoint |
| R1–R4 | name who produced the evidence and under what model | a source report, local observation and universal deployment claim need different support |
