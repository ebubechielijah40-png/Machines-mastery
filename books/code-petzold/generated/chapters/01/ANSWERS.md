# Answer notes — consult after saving your work

These are original reference answers, not learner evidence. Alternative explanations are acceptable when assumptions and reasoning hold.

Entry diagnostic: TE is `- | .`; `.-` could be A or ET after removing boundaries; 300 milliseconds requires a time-scale and framing agreement before classification.

1. The codebook maps allowed characters to marks; the signaling rule maps marks and boundaries to timed levels. The receiver reverses both under agreed conditions.
2. E's dot is also A's first mark. A character boundary, not a successful prefix lookup, justifies emission.
3. N E at τ=2: ON 6, OFF 2, ON 2, OFF 12, ON 2, EOF. Buffer sequence: `-`, `-`, `-.`, empty with output `N `, `.`, empty with output `N E`. Total is 24 chosen time units, or 12τ.
4. A and ET both yield `.-` without boundaries.
5. Scaling both sides preserves all duration ratios and text, doubling elapsed duration. Scaling only the sender produces ratios 2, 6 and 12 against the old unit; the strict lab rejects the first ON event of ratio 2 or 6. A tolerant or adaptive receiver would be a different model requiring analysis.
6. Both A and ET are valid messages. Grammar validation cannot distinguish intentional ET from corrupted A.
7. Our frame ends at EOF and carries no trailing gap. A physical capture needs a segmentation convention before becoming a lab frame; darkness alone does not certify finality.
8. `a` and `A` collapse to the same uppercase input. No deterministic inverse can always choose the original without additional information.
9. ON durations are τ and 3τ. Equal mark counts do not imply equal elapsed durations.
10. Example E=`..`, T=`.-`, A=`-.`, N=`--`. Grouping works in pairs if the start is aligned, mark boundaries are known and no mark is lost or inserted. Unknown start or deletion can shift all later pairs. This is an original transfer exercise, not a reconstruction of Chapter 2.
11. A saved test output observes behavior of that program on those inputs. It does not observe switch behavior, light detection or human timing.
12. Repeated measured mark/gap durations under specified equipment, distance, illumination and sending conditions could inform a tolerance model. No particular threshold or error rate is established here.

For the mastery transfer task, a correct answer must declare alignment and error assumptions. For any proposed physical result, request the actual protocol and raw observations before accepting a conclusion.
