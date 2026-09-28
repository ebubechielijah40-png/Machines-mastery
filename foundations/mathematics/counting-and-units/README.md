# Counting, quantities and units

PREPARED; learner NOT STARTED. Unit F-COUNT. Original explanation and derivation; see [foundation policy](../../README.md).

A duration needs both a number and an agreed unit. Imagine three adjacent marks on paper: counting gives 3; measuring each interval with the same small unit lets you compare their lengths. A millisecond is one thousandth of a second, so 300 milliseconds is 300/1000 = 0.3 seconds. Changing the unit changes the number, not the interval.

An integer counts complete steps. Zero means none, not missing evidence. Addition combines counts: 2+3=5. Multiplication repeats equal groups: 3 groups of 2 contain 6. Division asks how many equal groups fit: 6/2=3. A fraction 1/2 means one of two equal parts; a denominator of zero does not define a share. If lengths have unlike units, convert before adding. For intervals 2 ms and 3 ms, the combined duration is 5 ms; adding 2 ms to 3 seconds as “5” loses meaning.

A variable is a name for a chosen quantity. Let τ mean one agreed interval, not a mysterious constant. If τ=2 ms, 3τ=6 ms. If τ doubles, every fixed multiple doubles. For two intervals t and τ measured in the same unit, t/τ counts how many unit intervals fit and has no physical unit. The Code decoder uses that ratio to distinguish durations.

```text
one interval: |--|     three equal intervals: |--|--|--|
```

Edge: an empty sequence has zero events, while an unknown duration has no established value. Wrong: “three intervals must take three seconds.” Correct: it takes three times the declared interval. Transfer: a camera frame numbered 3 is a count, not a time; you also need a rate or individual timestamps. No physical measurement is claimed by these drawings.

Study [problems](problems/README.md), then [hints](hints/README.md) after an attempt. [Solutions](solutions/README.md) are separate. Complete the [experiment](experiments/README.md) and transfer before returning to the dependent unit.
