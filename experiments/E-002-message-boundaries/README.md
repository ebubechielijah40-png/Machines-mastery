# E-002 — Message boundaries

Status: PLANNED. Observed result: **NOT YET OBSERVED**. Project J-01, phase P01, resource R-CODE, Chapter 1 PDF 6–10. No learner execution is recorded.

## Question and hypothesis

Can changing only a gap change decoded text while preserving every ON interval? Prediction under the ideal model: A becomes ET when its internal gap changes from τ to 3τ. Deleting all gaps makes the two inputs indistinguishable. This is a model prediction, not an observation.

## Variables and controls

Independent variable: the gap between the same dot and dash (τ, 3τ, or removed). Dependent variables: decoded text, acceptance/rejection and total ideal duration. Hold the table, τ, ON intervals and explicit frame boundary fixed. Control frame: A at τ=1. Use the same decoding procedure for all cases. No physical apparatus or human timing claims are involved.

## Procedure

1. Save a dated prediction for A and ET before decoding. State the table and time-unit convention.
2. Draw the control frame: ON 1, OFF 1, ON 3, EOF. Trace the buffer and output at every event.
3. Change only OFF 1 to OFF 3. Trace again without changing the table or ON intervals.
4. Delete the gap from each written representation. List both possible original texts; do not treat the resulting marks as a valid alternating event-list frame.
5. Repeat with N versus TE. Record results before opening reference answers.
6. Optionally check with the reference decoder after preserving your own traces. Record exact commands and environment if used.

## Raw record and analysis

Create an original non-private trace under this experiment's `raw/` directory when executed; include prediction time, actual sequence, intermediate states, result and corrections. No raw file is prefilled. Compare observed traces to predictions, explain disagreement and test alternatives such as wrong τ or wrong mapping. An accidental table change is a confound. Conclude only about this model and these inputs; no estimate of real communication error rate follows.

Update the catalog to OBSERVED only with real raw evidence and a separate learner review if appropriate. Reference software validation is not E-002 execution. Follow-up: alter the receiver's τ while keeping the event list fixed, then explain which assumption failed.
