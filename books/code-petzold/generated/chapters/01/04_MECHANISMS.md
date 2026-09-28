# Decoder mechanism

[EXPLANATION] This is an original model, not an algorithm attributed to Petzold. Source premises: C-CODE-01/02; model reasoning: C-CODE-07.

```text
allowed text -> lookup -> timed ON/OFF events -> duration classification
            -> unfinished mark buffer -> boundary -> character lookup -> output
```

## Interface and state

Use E `.`, T `-`, A `.-`, N `-.`. A frame is either empty or alternates ON then OFF, beginning and ending ON. ON durations are 1τ or 3τ; OFF durations are 1τ, 3τ or 6τ. No leading/trailing spaces or repeated spaces are accepted. EOF is an explicit frame boundary. Durations and τ are positive integers in the reference implementation, expressed in the same unspecified time unit.

| Event | State change | Reason |
| --- | --- | --- |
| ON 1τ | Append `.` to buffer | Classified dot |
| ON 3τ | Append `-` to buffer | Classified dash |
| OFF 1τ | Retain buffer | Another mark in same character |
| OFF 3τ | Look up buffer, emit character, clear buffer | Character boundary |
| OFF 6τ | Look up buffer, emit character then space, clear buffer | Word boundary |
| EOF after ON | Look up and clear buffer | Explicit end-of-frame contract |

Invalid level order or duration rejects the frame. An unknown completed pattern rejects the frame. The function returns a complete result only if the whole frame is valid, rather than exposing partial output as confirmed text.

## Trace: AN

Let τ = 2. Input: ON 2, OFF 2, ON 6, OFF 6, ON 6, OFF 2, ON 2, EOF.

| After event | Buffer | Completed output |
| --- | --- | --- |
| ON 2 | `.` | empty |
| OFF 2 | `.` | empty |
| ON 6 | `.-` | empty |
| OFF 6 | empty | A |
| ON 6 | `-` | A |
| OFF 2 | `-` | A |
| ON 2 | `-.` | A |
| EOF | empty | AN |

The OFF 6 above means three time units, not a word gap: τ is 2. Confusing raw durations with ratios breaks the trace.

## Perturb the mechanism

Change only the first OFF 2 to OFF 6. Predict the result before tracing: the first dot now closes E; the following dash closes T. The frame becomes ETN without a syntax error. Alternatively, change the first ON 2 to ON 4: its ratio is neither 1 nor 3, so this ideal decoder rejects it. These are distinct failures: valid-but-wrong text versus an invalid frame.

A physical receiver must produce event durations from samples before this mechanism runs. Missed edges, saturation and timing uncertainty belong to that additional stage. Our function is not a hardware driver and its tests do not establish physical reliability.
