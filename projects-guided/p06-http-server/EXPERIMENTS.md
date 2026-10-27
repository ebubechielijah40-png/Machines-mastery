# Local HTTP framing investigation

Question: does read/write fragmentation affect the supported request semantics? Hypothesis: supported GET /health returns the same six-byte body while malformed framing and truncated EOF produce 400. Keep request bytes and route table fixed; vary sender chunk size and server receive limit. Instrument sender chunk lengths, client response recv sizes, status line, declared Content-Length and actual body bytes.

Run `python3 projects-guided/p06-http-server/code/experiment.py`. The [executed JSON](evidence/observed.json) records Python/platform and six trials: health at small and large reads, absent route, rejected method, competing framing indicators and truncated EOF. The status lines are respectively 200,200,404,405,400,400. Chunk shapes are interface observations, not TCP packet measurements. No public listener is created.

Alternative explanations for different chunk lengths include scheduling and local kernel buffering. Follow-up: instrument an authorized loopback TCP endpoint separately; do not relabel socketpair results as a TCP experiment. Load admission, actual timeout latency and power/network failures remain unmeasured.
