# Hints after a design attempt

Scheduler: keep future arrivals separate from the ready queue. At a slice end,
admit arrivals before requeueing the unfinished job. Record first execution
only once; finish only when remaining service reaches zero.

Switch cost: a job selected before a switch remains selected during that cost
in this model. Jobs arriving during the cost can enter the queue but do not
replace it. State this rule explicitly rather than assuming a universal policy.

Translation: derive `(vpn, offset) = divmod(address, 16)` before introducing
bit operations. Split VPN into `(vpn >> 2, vpn & 3)` only after checking widths.

TLB: a cached entry carries permissions as well as frame identity. Access checks
must run on both the hit and walk paths. A map/unmap changes authority and must
invalidate affected cached state through the supported API.

Evidence: a hash labels input bytes. It cannot turn an incorrect model into a
correct one. Preserve the transition specification and independent tests too.
