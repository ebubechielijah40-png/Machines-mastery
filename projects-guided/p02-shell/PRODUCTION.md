# Engineering beyond the bounded build

A shell serving a person and a service running arbitrary jobs have different
requirements. This unit supplies neither a security boundary nor a complete
interactive interface. Before extending it, state the threat and failure model.

For a trusted batch tool, preserve full argv, cwd, per-stage exit codes and
bounded diagnostics in an audit record; avoid logging credentials carried in
arguments. Report truncation explicitly instead of silently presenting a
complete-looking stderr. Choose whether any failing stage should fail the
pipeline, and test early consumer termination as well as producer failure.

Temporary-file capture avoids pipe-drain deadlock but moves pressure to disk.
A scalable runner would stream with a selector/event loop or dedicated readers,
enforce output limits during execution, apply backpressure, and guarantee
cleanup on cancellation. Measure bytes produced, peak stored bytes, time to
first output, completion latency, and child count before optimizing.

For interactive use, process groups, terminal foreground ownership, and signal
delivery have to be designed together. Killing one process is insufficient for
a process tree. For untrusted execution, use OS-enforced isolation, restricted
identities, resource quotas, filesystem/network policy, and independent cleanup.
Those mechanisms are not implemented or validated here. Deployment of this
reference as a public execution endpoint is outside its contract.
