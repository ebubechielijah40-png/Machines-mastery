# Executed validation

Run `python3 -m unittest discover -s projects-guided/p06-http-server/code -v` from repository root. The [actual log](evidence/tests.txt) records ten unittest methods and exit status. Cases cover literal request/response bytes; every truncated request; duplicate/competing framing fields; controls/bare LF/non-ASCII/size; real fragmented sockets; real 404/405; premature EOF; absolute-deadline regression; invalid configuration; and injected receive/send cleanup failures.

Literal vectors, response-length checking and malformed inputs give evidence beyond encode/decode self-agreement. The deadline case uses a fake clock, not an observed latency result. No throughput, public-network, TLS or full HTTP conformance test was run. Run the separate [experiment](EXPERIMENTS.md) for actual local interface observations.
