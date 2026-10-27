# Build a bounded HTTP request machine

Build a deliberately narrow HTTP/1.1 teaching endpoint over local socketpairs. The outcome is a one-request connection handler that accepts `GET /health` with exactly `Host: localhost`, returns `ready\n` with a correct byte length, and closes the connection. This project now has executable [reference code](code/http_subset.py), [tests](code/test_http_subset.py), [experiment](code/experiment.py) and recorded [evidence](evidence/observed.json). It is not a complete conformant HTTP server: request chunking, persistence, general authority syntax, TLS, dates, caching and concurrency admission are absent.

First complete the [stream-boundary lesson](../../06-networking/stream-boundaries/LESSON.md). Entry gate: trace a length-prefixed message across three reads, explain partial sends and distinguish an empty message from EOF. For Python syntax use [programming foundations](../../02-programming/README.md). Required tools are Python 3.12 standard library and a host providing `socketpair`; there are no pip packages, external services or public listeners.

## What the learner derives

HTTP uses a start line, field lines and an empty line before any body. Unlike our binary frame, it has multiple body-length conventions. Two recipients interpreting the same bytes differently can disagree about where a request ends. RFC 9112 §2.1–2.2 specifies byte-level message parsing; §6 addresses competing body-length indicators. This project refuses unsupported cases instead of implementing their complete semantics. Its narrow rejection rules must not be presented as a general request-smuggling defence for a proxy.

Trace these exact bytes before running code:

```text
GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n
```

The `\r\n` notation denotes two wire bytes, not four printed characters. The first empty line terminates headers. Split raw bytes at that delimiter before interpreting the restricted ASCII lines. Splitting a decoded Unicode string first can introduce interpretations not defined by the wire protocol. The parser checks the request-line shape, version, token field names, one Host, no controls/obsolete folding, no duplicated fields, no Transfer-Encoding, Content-Length absent or exactly `0`, and no Expect handshake. Only the route table decides whether a syntactically supported method is allowed.

A normal request leads to body bytes `72 65 61 64 79 0a`: six bytes. The response therefore says `Content-Length: 6`. Counting Python characters instead of encoded bytes would be wrong for a non-ASCII response. A missing route returns 404; an unsupported method with otherwise valid syntax returns 405 plus `Allow: GET`; an incomplete, ambiguous or unsupported request returns 400 when the connection remains writable.

## Build milestones

Keep a separate learner copy; write a design attempt before consulting the reference or [hints](HINTS.md). Each milestone has a visible acceptance condition.

| Stage | Learner work | Checkpoint |
| --- | --- | --- |
| A0: contract | Write accepted grammar, 4096-byte header budget, deadline, ownership and unsupported features | Classify valid, duplicate Host, bare LF, body and EOF examples by hand |
| A1: pure parser | Implement bytes-to-`(method,target,headers)` without sockets | Literal vector passes; every truncated prefix rejects; duplicate case-insensitive names reject |
| A2: response | Build headers from encoded body length, map 200/400/404/405 | Independently split the response and compare body length with declared length |
| A3: stream collector | Repeatedly recv at most the remaining byte budget until header delimiter or EOF | One-byte client writes and three-byte server reads still return the same response |
| A4: lifecycle | Use an absolute monotonic header deadline and close in an outer finally | Partial arrivals cannot extend the overall deadline; injected recv/send failures close ownership |
| A5: investigation | Vary read/write chunk limits and inject malformed requests | Save actual observations separately from predictions and explain every status |
| A6: reconstruction | Rebuild A1–A4 without the implementation | Another learner's independently chosen boundary cases pass |

The architecture has a pure parser between byte collection and routing. Socket ownership belongs to `serve_once`: every exit closes it. An outer `finally` is required because receive failure can occur before response sending. The handler uses `sendall`; on an exception it closes rather than repeating a response prefix whose accepted-byte count is unknown.

A timeout on each recv alone is insufficient: a peer could send one byte just before each timeout indefinitely. Set `deadline = monotonic()+timeout` once; before each recv set its timeout to `deadline-monotonic()`. Header collection is then time-bounded independent of chunking. Response sending has its own timeout. This does not implement a whole-server connection cap; a million handlers would still require a million admission decisions and resource budgets.

Already-collected bytes after the header delimiter are rejected by the pure parser. Additional bytes arriving only after that parse may be discarded by connection closure. This is not a promise to detect all pipelining. Because the connection is neither reused nor forwarded, the lab does not create a second request from them.

## Run and evaluate

From repository root:

```sh
python3 -m unittest discover -s projects-guided/p06-http-server/code -v
python3 projects-guided/p06-http-server/code/experiment.py
```

Expected qualitative behavior: fragmented and coalesced valid requests produce identical response bytes; invalid framing and premature EOF yield 400; routing gives 404 or 405 as above. Actual observations and environment are in [evidence/observed.json](evidence/observed.json). Do not interpret mocked time in one deadline regression as a measured real-time latency benchmark.

Submit a parser/state diagram, learner code, literal test vectors, a failure log, experiment JSON, and an explanation of all excluded HTTP features. The rubric requires correct grammar and lengths (30%), state/lifecycle/resource bounds (30%), independent adverse cases (25%) and documented limits/reconstruction (15%). A solution that accepts ambiguous lengths fails the framing criterion even if `/health` works.

Deployment is limited to local tests in this project. A real service should use a maintained HTTP stack, authenticated transport, admission control, structured safe logs, load/failure testing and a reviewed deployment configuration. Implementing those is follow-up work, not an inferred capability of this endpoint. Continue to [scientific ingestion](../p08-scientific-pipeline/README.md) and then [authenticated provenance](../p09-secure-pipeline/README.md).

## Sources inspected

R. Fielding, M. Nottingham, J. Reschke, RFC 9112, *HTTP/1.1*, June 2022: [§2.1–2.2](https://www.rfc-editor.org/rfc/rfc9112.html#section-2), [§3](https://www.rfc-editor.org/rfc/rfc9112.html#section-3), [§5.2](https://www.rfc-editor.org/rfc/rfc9112.html#section-5.2), [§6–6.1](https://www.rfc-editor.org/rfc/rfc9112.html#section-6), [§8](https://www.rfc-editor.org/rfc/rfc9112.html#section-8), inspected 2026-10-22. These scopes support message syntax, byte parsing, obsolete-fold rejection, incomplete-message reasoning and framing risks. They do not establish this subset's HTTP conformance. Python socket contracts are mapped in the [network source record](../../06-networking/stream-boundaries/SOURCES.md). No RFC text or implementation is copied; original examples and lab code retain the repository's license.
