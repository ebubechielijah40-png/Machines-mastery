# Selected primary sources and original work

Inspected2026-10-25 by the integrating author. Source pages are live and may
change; no complete text, figures, code example or copyrighted book is included.
The lab's state machines, arithmetic derivations, workload, counterexamples,
implementation, questions and observed data are original repository work.

| Source | Exact inspected scope | Claim supported and boundary |
| --- | --- | --- |
| SQLite project, [Online Backup API](https://www.sqlite.org/backup.html), §§1,3 and3.1 | Engine-managed page copying and locking in incremental online backup | Explains use of the backup interface. Our generation/manifest/receipt protocol is not SQLite's algorithm or a reproduced power-failure guarantee. |
| Python Software Foundation, Python3.12.15 documentation, [Connection.backup](https://docs.python.org/3.12/library/sqlite3.html#sqlite3.Connection.backup) | target,pages,progress,name,sleep and concurrent-use note | Exact Python interface and callback parameters. Actual runtime is3.12.14/SQLite3.53.1 in raw JSON; documentation version is not the executed interpreter. |
| Prometheus Authors, [Histograms and summaries](https://prometheus.io/docs/practices/histograms/), Overview,Bucketing,Quantiles | Aggregate distributions rather than average precomputed quantiles; cumulative inclusive buckets | Intellectual source for choosing distributions. Local bucket upper bounds are original finite arithmetic, not PromQL interpolation or an implementation of modern native histograms. |
| Python Software Foundation, Python3.12.15 documentation, [http.server](https://docs.python.org/3.12/library/http.server.html), HTTPServer,BaseHTTPRequestHandler and introductory security warning | Dispatch/lifecycle/response framing and limited security | Supports the loopback-only teaching choice. No claim that this standard-library server is suitable for a public production boundary. |

Third-party source and documentation terms remain with their respective
publishers. No blanket redistribution permission is inferred
from readability. We inspected selected scopes, not entire SRE books, complete
Python/SQLite implementations, external storage hardware or an actual hosted
monitoring installation. Existing SLO/transaction/timer source records remain in
[SOURCES.md](SOURCES.md). The chosen two-window rule and its numeric thresholds
are an original transparent policy, not a calibrated alarm quoted from a source.
