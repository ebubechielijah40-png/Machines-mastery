# Formal model and correctness

[DERIVED] Original model based on the inspected mapping and timing premises C-CODE-01/02. No equations below are attributed to the author.

## Domains

Let L = {E,T,A,N}. Texts contain letters in L with at most one space between nonempty words; the empty text is allowed. Define c(E)=`.`, c(T)=`-`, c(A)=`.-`, c(N)=`-.`. Let τ > 0 be the shared time unit. A dot costs τ of ON time and a dash 3τ. Internal gaps cost τ, character gaps 3τ, word gaps 6τ. A frame carries an explicit end; no final OFF event is encoded.

## Duration derivation

For a character with d dots and h dashes, there are d+h−1 internal gaps. Its duration is therefore

```text
T_character = [d + 3h + (d+h−1)] τ = (2d + 4h − 1) τ.
```

For a nonempty message with k letters in w words, let D and H be total dots and dashes. Internal gaps number D+H−k. Inter-letter gaps inside words number k−w; inter-word gaps number w−1. These sets are disjoint, so

```text
T_message / τ = D + 3H + (D+H−k) + 3(k−w) + 6(w−1)
              = 2D + 4H + 2k + 3w − 6.
```

Check a one-letter E: D=1,H=0,k=1,w=1 gives 1. Check E A: D=2,H=1,k=2,w=2 gives 12. Empty text has duration zero by a separate case; the nonempty formula does not apply to it. These are ideal serial elapsed durations, not throughput measurements or a claim about human sending speed.

## Decoder invariant

After each accepted event, completed output equals the decoded characters whose boundaries have already been seen. The buffer contains exactly the marks since the most recent character boundary, in order. The expected level is the opposite of the last event's level (ON initially). A pending buffer must not be emitted simply because it matches a codeword: E is a prefix of A.

Proof by induction: initially both sequences are empty. An ON event appends exactly its classified mark. An internal OFF event changes no character boundary. A boundary OFF event converts exactly the accumulated pattern using the agreed mapping, then clears it, adding a space only for a word boundary. Each case preserves the invariant. At EOF, the final valid pattern is closed. Unknown patterns or malformed events produce rejection, so no incorrect successful return follows from an invalid lookup.

For every permitted input x and agreed positive integer τ, decode(encode(x,τ),τ)=x: encoding supplies exactly the marks and boundaries needed by the invariant, and the four codewords are distinct at character boundaries. This is a round-trip claim for the restricted domain; arbitrary received signals can be corrupted into other valid inputs.

## Information-loss counterexample

Let strip delete all boundaries from codewords concatenated for a message. Then strip(A)=`.-`=strip(ET), yet A≠ET. Assume an inverse g always recovers both. It would require g(`.-`)=A and g(`.-`)=ET, a contradiction for a function. Exact universal recovery is impossible after that deletion. Case normalization gives the same proof shape: two distinct inputs collapse to one output.

## Algorithmic cost

Let m be the number of input events and n the number of text characters. Encoding is O(n) time and O(n) output space because the codebook has bounded codeword length. Decoding is O(m) time and O(m) space including returned output; the pending pattern is bounded to two marks by this lab's prefix rejection. Output lists are joined once. These bounds assume bounded-size duration integers and constant-time table operations; Python's arbitrary-size integer arithmetic adds bit-length cost for unusually large durations. Repeated concatenation of a growing output string would undermine the simple linear-time argument.
