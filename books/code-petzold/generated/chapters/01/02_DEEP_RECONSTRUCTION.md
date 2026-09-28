# From a signal to a message

The explanations and examples below are original teaching material. Source-backed premises are listed in [references](11_SOURCE_REFERENCES.md); deductions are explicitly scoped to our small model.

## A representation is an agreement, not the thing represented

[SOURCE: C-CODE-01] Chapter 1, PDF 6–8, distinguishes shared codes from the physical means of sending them. The letter-code table on PDF 7 and the realization discussion on PDF 8 support this distinction.

[EXPLANATION] Suppose our input is the message TE. An encoder consults the shared table and produces two patterns, `-` and `.`. Those marks on paper are descriptions; a lamp cannot emit a printed dash. A second rule turns the description into durations of light and darkness. A receiver must undo both decisions: classify the durations, then group and interpret the classified marks. Agreement about one step does not supply agreement about the other.

The inputs to our encoder are allowed text and a positive time unit τ. Its output is a sequence of `(level, duration)` pairs. The decoder takes that sequence and the same τ and yields text or a rejection. The codebook and timing rules are configuration; the unfinished character and output so far are changing state. Knowing which is which matters when diagnosing a mismatch: replacing a codebook changes interpretation even when the observed signal stays identical.

There are at least three boundaries to keep distinct: the sender's intended meaning, the text supplied to the encoder, and the signal the receiver observes. A correct decoder recovers permitted text under the model. It does not prove that the sender's statement was true, that the receiver understood its meaning, or that the claimed sender produced it. Encoding is not secrecy or authentication.

## Time and silence carry structure

[SOURCE: C-CODE-02/03] PDF 8 specifies relative durations; PDF 9 explains the sending-speed ambiguity. For this lab, we idealize the book's approximate timing as exact: dot τ, dash 3τ; off gaps τ inside a character, 3τ between characters, 6τ between words.

[EXPLANATION] Both a dot and a dash use the same ON level. Their durations differ. OFF also has more than one role: it separates marks, closes a character or closes a word. Counting physical levels therefore does not count all possible messages. Duration and grouping are part of the representation.

A raw interval of 300 milliseconds is not inherently a dash. With τ = 100 milliseconds it is a dash; with τ = 300 milliseconds it is a dot. Our lab makes τ an explicit input rather than pretending to infer it reliably from one interval. Real receivers also need a clock, a threshold for observing light and a policy for noisy durations. Those mechanisms are absent from the ideal event list; reject rather than silently invent tolerance.

[DERIVED: C-CODE-06] Deleting character gaps makes the representation ambiguous: A and ET both reduce to `.-`. No decoder given only those two marks can always distinguish the two original inputs. Trying harder, using a faster computer or memorizing more table entries cannot restore a distinction that the channel discarded. A language guess might select one input, but it adds a prior assumption and can be wrong.

## Decoding requires unfinished state

[DERIVED: C-CODE-07] Seeing `.` is insufficient to emit E immediately: the next internal gap and dash may complete A. Our decoder retains a buffer of marks until a character boundary arrives. A short gap leaves the buffer open; a character gap closes it; a word gap closes it and appends a word separator. Only after closure is lookup justified.

The state consists of the current pattern, completed output and expected event kind. Initially the pattern and output are empty and the decoder expects ON. Every valid event alternates level. At the end of the supplied event list, a separate end-of-frame agreement closes the last character. Without an agreed end, darkness after the last mark might mean a delay, an unfinished transmission or completion. An event list's end is an interface convention, not a light measurement.

Unknown completed patterns are rejected. The reference model also rejects unsupported durations, repeated levels and a trailing gap. Rejection identifies a violation of this interface; it does not locate the physical cause. A sender error, a missed edge or a wrong τ can produce similar symptoms.

## Recovery preserves only retained distinctions

[SOURCE: C-CODE-04] PDF 9 notes that letter case is not distinguished by the discussed code.

[DERIVED: C-CODE-08] If a preprocessing rule maps both `a` and `A` to `A`, any later decoder receives the same representation for two inputs. Exact case recovery is impossible without extra information. Our implementation instead accepts only uppercase symbols: it rejects lowercase so that its round-trip promise is precise. Normalization is a possible different contract, not a harmless invisible correction.

Even a well-formed signal can encode a different valid message after a disturbance. Changing A's internal gap into a character gap yields ET. Validation of syntax therefore does not guarantee faithful transmission. Detecting such changes would need redundancy or another check outside this unit.

## Cost depends on what is counted

[SOURCE: C-CODE-09 premise] PDF 9 connects common letters with shorter patterns. [EXPLANATION] Counting marks, elapsed duration, switching actions and reader effort asks different questions. E and T each use one mark, but T takes three times E's ON duration in this model. A character boundary adds time without adding a mark. Do not call one representation universally faster after counting only marks.

The [formal model](06_FORMALISMS.md) is intentionally small: it separates a countable prediction from a hardware measurement. Mechanical switch behavior, propagation delay, visibility and actual human response are unmeasured here. To study them, define a new physical protocol with calibration and raw observations rather than presenting these ideal calculations as measured facts.

## How to test understanding

Hide the table and explain which agreements the receiver needs; then bring it back and trace an unfamiliar permitted message. Predict what changes when you alter only τ, only one gap or only the lookup mapping. A useful explanation names the state and the precise failing assumption. “It gets confused” is a starting question, not a mechanism.
