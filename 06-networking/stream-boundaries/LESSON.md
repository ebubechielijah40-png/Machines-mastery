# From bytes to messages

This unit builds one bounded stream decoder and investigates the socket interface that feeds it. It prepares the [HTTP project](../../projects-guided/p06-http-server/README.md) and [authenticated provenance project](../../projects-guided/p09-secure-pipeline/README.md). It does not teach routing, congestion control, DNS or a complete TCP implementation.

Before starting, explain array slices, exceptions and an unsigned four-byte integer. If bit positions are unfamiliar, write 513 as `0*256^3 + 0*256^2 + 2*256 + 1`. Its network-order bytes are `00 00 02 01`. Network order fixes how the endpoints interpret bytes; it does not depend on their host CPU byte order. Use [proofs and invariants](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md) to state the decoder's invariant before testing it.

## Why a receiver needs state

A stream transports an ordered sequence of bytes. TCP's service definition is an ordered byte stream, rather than a sequence of application messages [N1]. Suppose a producer writes `cat` and then `dog`. A consumer could receive `c`, `atdo`, `g`, or `catdog`. None tells it which byte was the last byte of the first logical message. A successful `send` tells the caller how many bytes were accepted by that call; it does not imply the peer processed them [N2].

Three common ways to recover boundaries are fixed-size records, delimiters with escaping, and explicit lengths. A newline protocol is simple until a payload itself contains a newline. A length-prefixed protocol allows arbitrary payload bytes, but must limit a peer's requested allocation. This unit chooses:

| Field | Bytes | Meaning |
| --- | ---: | --- |
| Length | 4 | unsigned big-endian payload length |
| Payload | length | uninterpreted bytes; zero length is valid |

The exact bytes for `hi`, followed by an empty message, are `00 00 00 02 68 69 00 00 00 00`. The prefix length excludes its own four bytes. A receiver configured for at most 100 payload bytes rejects the declaration `00 00 00 65` immediately, even if no body bytes follow. Waiting to allocate or receive that body would grant the sender control over resource use.

## Deriving the incremental machine

`Decoder` in [framing.py](../code/framing.py) retains only the current incomplete frame. `expected=None` means it is collecting the four length bytes. Once all four arrive, it decodes their integer, checks the budget and collects exactly that many payload bytes. A completed frame is copied to the output list, then the machine returns to collecting a prefix. A single call may complete zero, one or many frames.

Trace the first example with calls `feed(00 00)`, `feed(00 02 68)`, `feed(69 00 00 00 00)`. After the first call, two header bytes remain pending. During the second call, the header completes with length two and one payload byte remains pending. During the third call, `69` completes `hi`; the following four bytes complete an empty frame. The output of the last call is `[b'hi', b'']`.

State the invariant as a disjunction: either no length is known and `0 <= len(buf) < 4`, or a checked length `L <= max` is known and `4 <= len(buf) < 4+L` between completed-frame steps. At the moment a frame completes, equality is handled before continuing. Empty frames complete immediately after their headers. The implementation copies only the bytes needed for the next transition, so a huge input holding many short messages does not become one huge pending buffer.

Each input byte advances the offset once, and each payload byte is copied out once. Time is linear in bytes plus message count. Retained incomplete-frame storage is at most `max+4`. This is **not a total process memory bound**: the caller already owns `data`, and the returned list can retain arbitrarily many completed messages. A service must also bound read chunks, outstanding outputs, queued writes and connection count. A generator or callback interface could avoid building the whole output list, with different exception and ownership rules.

## EOF and errors are protocol events

An empty `recv` means the peer's sending direction has ended. It does not itself prove that the application message finished. Call `finish()` after EOF. At a frame boundary it changes OPEN to CLOSED; inside a prefix or payload it raises `TruncatedFrame` and enters FAILED. A zero-length application message is a four-byte frame, whereas an empty `recv` is transport EOF. Confusing these loses messages.

An oversized declaration also enters FAILED and clears pending bytes. Subsequent input cannot safely resume: those bytes might be body bytes from the rejected frame, and their apparent length prefix would be accidental. Create a new decoder for a new connection. CLOSED accepts a repeated `finish()` but no more input. Type mistakes reject the call; protocol failures are terminal.

One API limitation matters for delivery semantics. If one `feed` call completes a good frame and then finds an invalid prefix, that call raises instead of returning its accumulated list. Previously returned messages stay returned. It therefore provides neither transactional batch delivery nor a promise to deliver every good prefix before a later error. Design the application around the documented behavior; do not infer exactly-once processing from framing.

## Partial writes and backpressure

For raw `send`, maintain `offset`: send `wire[offset:]`, then add the returned positive count. In nonblocking mode, `BlockingIOError` means wait for writability and try the remaining suffix. Repeating the whole original message after a short send duplicates its accepted prefix. Blocking `sendall` performs repeated sends for you, but an exception does not report a recoverable accepted-byte offset [N2]. Recovery then belongs to the application protocol: reconnect, authenticate a request identifier, and reconcile whether the request committed.

`shutdown(SHUT_WR)` ends one direction while leaving the other available. The socketpair test sends frames, half-closes the producer, verifies clean EOF and then returns an acknowledgement over the reverse direction. This demonstrates why application completion, connection closure and direction closure are distinct states.

## Controlled experiment and actual evidence

Question: does changing application `recv` size change decoded messages? Hypothesis: it changes delivery chunks while the frame sequence remains `[5, 0, 80]` payload bytes. Hold wire bytes and sender write chunks at five bytes; vary receive limit across 1, 3, 7 and 64. Instrument every send-call chunk, every receive return length, decoder state and peak pending storage. [stream_experiment.py](../code/stream_experiment.py) runs real local `AF_UNIX/SOCK_STREAM` socketpairs.

Run from the repository root:

```sh
python3 -m unittest discover -s 06-networking/code -v
python3 06-networking/code/test_framing.py
python3 06-networking/code/stream_experiment.py
```

The committed [observations](evidence/observed.json) reconstructed all three messages for every receive limit. In the backpressure trial the kernel accepted 8064 bytes of a 1 MiB pending send before reporting would-block; it reported an 8192-byte send buffer after a request for 4096. These are observations of that recorded Linux environment, not portable constants. Buffer accounting and scheduling offer alternative explanations for numeric differences on another host. The test checks accepted bytes survive a later drain; it does not assert a particular short-send size.

This experiment does not observe TCP packets, retransmission, routing, Internet latency or congestion control. An AF_UNIX stream supports the interface exercise without asserting that its implementation equals TCP. Follow up with authorized loopback TCP instrumentation and separately record the interface, kernel and packet capture, rather than relabeling these results.

Finish [exercises](EXERCISES.md) before opening [hints](HINTS.md) or [solutions](SOLUTIONS.md). The source map and verification scopes are in [SOURCES.md](SOURCES.md).
