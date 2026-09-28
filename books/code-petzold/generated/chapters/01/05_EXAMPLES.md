# Original worked examples

[DERIVED] All values are predictions under the exact lab model, not measured flashlight performance. Use [mechanism](04_MECHANISMS.md) and [formal reasoning](06_FORMALISMS.md).

## Equal marks, unequal duration

E has one ON interval of τ. T has one ON interval of 3τ. Each has one mark; T takes three times as long for a single-character frame. A has ON τ, OFF τ, ON 3τ, totaling 5τ. ET has ON τ, OFF 3τ, ON 3τ, totaling 7τ. Removing the gaps hides the distinction between A and ET; retaining them distinguishes both meaning and duration.

## Same pattern, different word structure

EA: ON τ, OFF 3τ, ON τ, OFF τ, ON 3τ; total 9τ.

E A: ON τ, OFF 6τ, ON τ, OFF τ, ON 3τ; total 12τ.

Only the boundary changes. Word gaps replace character gaps; they are not added on top of them. Adding both would give 15τ, a different protocol.

## Unknown scale

Observed frame: ON 3 milliseconds and end-of-frame. With τ = 1 millisecond it is T. With τ = 3 milliseconds it is E. Both are valid under different agreed scales. One sample cannot choose between those hypotheses.

## Boundary and invalid cases

An empty frame decodes to empty text by explicit contract. A single dot followed by EOF decodes to E. ON τ, OFF τ with EOF is invalid in our event interface because the frame ends in a gap. A physical recording that ends in silence would first need segmentation into this interface; do not infer that silence in nature is invalid.

ON τ, OFF τ, ON τ, EOF gives `..`, which is outside this restricted table. Reject it rather than extending the alphabet silently. The rejection is about our four-letter lab, not all Morse code.

## Test before the answer

Write out N E with τ = 2. Predict the full event list and total duration, then check your work using [answer notes](ANSWERS.md). Preserve your first prediction.
