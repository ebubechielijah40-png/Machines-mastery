# Incident exercise: a slow dependency exhausts a finite latency budget

This is an analysis of the controlled local run in [observed.json](evidence/observed.json),
not a report of a customer incident or an invented outage. The eligible population
is40 submitted lab operations. The intended objective is at least95% known
successful responses within30 ms;40 events permit2 bad outcomes.

## Impact and evidence

Under12 ms injected dependency delay at4 ms arrival spacing, only6/40 events
were good;23 expired and11 were rejected for capacity. p95 queue wait was23.906875
ms and p95 total latency36.146772 ms. Process CPU was8.560365 ms across188.918797
ms elapsed. These observations point to waiting rather than heavy CPU arithmetic
in this constructed workload. They do not distinguish every internal SQLite
wait from all scheduling delays. The raw per-event records allow that claim to
be challenged rather than inferred from a single average.

The operation-store invariant survived: only operations actually committed appear
in the counter and retained identity table. Availability and correctness are
separate: preserving state does not make the34 bad responses acceptable. Fast
overload must not be hidden by a success-only latency report.

## Mechanism and corrective action actually exercised

The generator offers250 requests/s while two workers with12 ms sleep have a
sleep-only upper service capacity about166.7/s. Database work reduces available
capacity further. Six running-plus-waiting slots eventually fill; queued requests
use their deadline before application; additional offers are rejected. Increasing
queue length would store more delay rather than remove the capacity mismatch.

The exercised correction changed spacing to8 ms while retaining the slow delay.
All40 offers were then good; queue p95 fell to.088085 ms and total p95 to15.920601
ms. Offered throughput was reduced. This is acceptable only if the application
can defer or reject demand under a declared contract; it is not a free capacity
increase. No deployment or external traffic change occurred.

## Recovery and unknown outcomes

A separate controlled kill before commit left counter0; retry applied+7 once.
After-commit kill left counter7 and a retained response; retry returned7 as a
duplicate. A real caller that times out cannot infer which case occurred and
must reconcile the same identity. Retrying under a new identity could duplicate
an already committed effect. The observed local process kills do not certify
physical storage durability or backup restoration.

## Review and follow-up acceptance conditions

Retain eligible/good/status counts, timestamp decomposition and raw operation
history. Set a finite retry budget and same-key policy before adding retries.
Run repeated paced/slow pairs in alternating order to reduce host-load bias.
Add explicit dependency and database timing if their contributions must be
separated. A proposed worker increase must improve good-event throughput under
fixed offered demand without breaking identity invariants or hiding rejections.
A backup change must demonstrate a restored invariant on a separate copy. These
are follow-up tasks; this report makes no claim that they were performed.
