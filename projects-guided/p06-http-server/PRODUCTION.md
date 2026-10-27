# Deployment boundary and extension tasks

The runnable artifact is a local connection handler, not a deployed listener. Keep experiments local and synthetic. For an actual service, use a maintained HTTP implementation and specify TLS identity, request/body limits, admission control, route authorization, log redaction and graceful shutdown.

Concrete extension tasks: enforce a shared maximum active-connection count; record bounded route/status/latency metrics without raw request bodies; inject client disconnect during response; and define deployment rollback under in-flight requests. Adding persistence requires a complete body-framing state machine and a reviewed policy after parse errors. Each extension changes the contract and needs separate tests; none is counted as implemented in this project.
