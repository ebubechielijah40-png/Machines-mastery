# Build milestones and assessment

Create a separate learner module rather than editing the reference. Keep a
short design log recording predicted state, observed failure, and the repair.

| Gate | Build and learner task | Observable exit evidence |
| --- | --- | --- |
| A0 | Represent commands as lists of strings. Draw lexer states. | Correct hand trace retaining `''` and quoted `|` |
| A1 | Implement `parse` without subprocess imports. | Exact argument vectors and rejection tests for unfinished syntax |
| A2 | Launch one argv vector, capture bytes and status. | Zero exit, exit 7, missing program distinguished |
| A3 | Connect two processes before waiting. Close inherited parent pipe objects. | 200,000-byte producer reaches counting consumer and EOF |
| A4 | Preserve each stage's status and stderr separately. | Failing producer followed by successful consumer remains diagnosable |
| A5 | Apply one deadline and cleanup after partial launch. | Timeout and second-stage launch failure leave no live direct child |
| A6 | Add logical cwd and builtin cd. | Two Shell objects maintain different directories; host cwd unchanged |
| A7 | Rebuild without notes, then transfer to three stages. | Fresh implementation passes semantic, lifecycle, and transfer checks |

Do not begin A3 with a complete reference runner. First write the intentionally
broken order “launch producer, wait, launch consumer”; predict why it hangs;
run it only with a timeout and locally owned short-lived processes. Repair the
control order before expanding features.

Evaluate with this 20-point rubric: lexer semantics 4, ownership/lifecycle
explanation 4, independent failure tests 4, experiment interpretation 4, and
reconstruction/transfer 4. For each category award 0 for absent, 1 for recalled
terminology, 2 for working ordinary case, 3 for edge/failure explanation, and
4 for an independently tested transfer. Any live-child leak or incorrect
quoted-pipe handling blocks a passing build regardless of total score.
