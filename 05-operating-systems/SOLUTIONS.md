# Checkable solution notes

1. A file is stored instructions/data. A process adds execution/mappings/resources;
   a thread supplies an execution stream. READY means eligible but not currently
   selected; an I/O-blocked stream would not qualify in that state.
2. TimelineA0–5,B5–7,C7–8. Responses0,4,5; turnaround5,6,6; waiting0,4,5.
3. A0–2,B2–4,C4–5,A5–7,A7–8. New arrivals through a slice boundary precede the
   unfinished current job's requeue. Responses0,1,2; turnaround8,3,3.
4. Idle0–3, usefulA3–7; no switch charge. Selection is initial after idle and no
   different runnable job replaces it at intermediate quanta.
5. One repeated interval supplies q useful and c overhead, so q/(q+c), assuming
   alternating ready work and constant modeled c. Real cache/TLB/predictor state
   and interrupt paths can change measured cost.
6. Short-first finish times2,9 sum11; long-first7,9 sum16. Difference5=b−a.
7. VA167 gives VPN10,offset7; physical20×16+7=327. Directory2,leaf2 for this
   two-plus-two VPN split. Offsets are byte counts, not frame numbers.
8. A previously read mapping does not authorize writes. Model raises PROTECTION
   and does not set dirty. Cached translations cannot bypass the contract.
9. Old cached result7×16+13=125; current correct result9×16+13=157. Invalidate
   on mapping changes; real multicore invalidation requires more mechanisms.
10. The number is interpreted under different mapping contexts. Shared physical
    frames require an explicitly installed shared mapping, not equal VA spelling.
11. In the declared file example:ab,cd,ab; duplicate offset4. The separate open
    starts its own offset at0. Resource type matters; not every descriptor seeks.
12. Another writer reference may remain open in the parent or child. EOF requires
    all such writers closed after buffered bytes are consumed. Use nonblocking
    reads in a bounded local test rather than hanging indefinitely.
13. A full pipe stops the child write while parent waits for its exit. Drain
    concurrently/communicate appropriately or use bounded alternative capture;
    merely increasing a timeout does not remove that dependency cycle.
14. Compare to raw evidence; do not call simulated ticks real seconds or host
    page translations. The run does not establish a production scheduling policy.
15. Ten VA bits minus five offset bits leave five VPN bits. A possible split is
    two directory plus three leaf bits:VPN=VA//32,offset=VA%32, dir=VPN//8,
    leaf=VPN%8. Correctness requires the independent lookup result, permissions,
    invalidation and context isolation, not memorizing these constants alone.
