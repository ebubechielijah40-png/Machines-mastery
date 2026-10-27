# Solutions and reconstruction criteria

## Scheduler boundary counterexample

For A(0,2), B(1,1), q=1, cost=1, A runs `[0,1)`. B arrives at 1 and is admitted
before A returns to the queue. Switching to B costs `[1,2)`, B runs `[2,3)`,
switching back costs `[3,4)`, and A finishes in `[4,5)`. Useful service is 3;
switch time is 2. A turnaround 5 minus service 2 gives waiting 3. B first runs
at 2, so response 1 and turnaround 2. Charging cost to A's first dispatch or
letting A requeue before B produces a different, unspecified model.

A single A arriving at 3 with service 4 has idle `[0,3)` and finishes at 7,
even if the configured different-job cost is 100. Same-job quantum boundaries
do not charge that cost. This exposes a switch-cost implementation that merely
adds cost on every slice.

## Address and authority

45 divided by 16 gives quotient 2 and remainder 13. The two VPN levels are
0 and 2. PFN 7 gives 125; remapping to 9 gives 157. A TLB miss should occur
after the supported remap invalidates the cached VPN. The offset remains 13
because page translation replaces page identity rather than byte position.
A write to cached read-only data is PROTECTION; a missing mapping is
NOT_PRESENT. Neither is synonymous with an ordinary TLB miss.

## Transfer geometry

With 10-bit VAs and 32-byte pages, five bits select the offset and five select
the VPN: 32 virtual pages. For a two-level table you might choose 2 directory
bits and 3 leaf bits, giving four directories of eight leaf slots. Address 333
is VPN 10, offset 13. PFN 21 yields PA 685. This is a new specified geometry;
copying old masks `>>2`/`&3` without deriving widths would be wrong.

## Hash and result

The driver hashes raw stdin bytes. Two JSON texts with different whitespace can
name the same workload and produce the same semantic result but different
hashes. This is correct for byte provenance. Canonical semantic hashing would
need a separate canonicalization contract. Neither hash establishes scientific
truth or kernel conformance.

## Reconstruction

Without the reference, implement a ready queue and service accounting, then a
flat translator, then table hierarchy and cached permissions. Write expected
traces and direct mathematical oracle first. Only then wrap them in bounded
JSON processing. A passing reconstruction must expose a deliberate bad arrival
order, stale cache and cached-permission bypass; explain and repair each;
run independent transfer tests; and label host observations separately from
model output. Booting a real kernel remains a separate unfulfilled milestone.
