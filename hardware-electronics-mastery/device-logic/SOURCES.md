# Primary inspection record

Inspected2026-10-23. Exact original scopes below support selected concepts;
original prose, images, PDFs and source exercises are not redistributed.
Authors' broader referenced textbooks were not silently treated as inspected.

| Resource | Inspected version/locator | Claim scope and limits |
| --- | --- | --- |
| MIT6.012 course team, Spring2009, *Lecture2 Semiconductor Physics(I)* | [Original PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009/6583f0018f5bb90464ea68b550f73c95_MIT6_012S09_lec02.pdf), slides2–17, especially8 and15–17 | Mobile electrons/holes, donor/acceptor fixed charge, equilibrium mass action and charge neutrality. The simultaneous exact-in-model quadratic solution and stable numerical rearrangement here are independently derived. No degeneracy/freeze-out/nonequilibrium prediction |
| MIT6.012 course team, Spring2009, *Lecture3* | [Original PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009/4692cf463514c4f47d8629fab7d41c15_MIT6_012S09_lec03.pdf), slides4–8 | Drift/mobility/current-density signs and conductivity. Code converts to SI and assumes constant mobilities. Diffusion and real impurity/temperature dependence are not implemented |
| MIT6.012, Fall2005, *Lecture9 MOSFET(I)*, dated October6,2005 | [Original PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/5c5960f14ae37d0a65478c4f3f628d98_lec9.pdf), slides3–15; channel integration slide12 visually checked | Four terminals, qualitative inversion, low-field charge-control integral and triode boundary. Ideal saturation is separately qualified; no claim of full numerical semiconductor solution or real part fit |
| MIT6.012 course team, Spring2009, *Lecture13 Digital Circuits(III)* | [Original PDF](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009/de333d22ec4230412f4e7bdd4da3d6ce_MIT6_012S09_lec13.pdf), slides2–6 and remaining selected static-gate diagrams | Complementary inverter rail operation, capacitive transition and approximate delay. Our integrated resistor-loaded circuit is a different explicitly specified model; “no idle power” applies only to an idealized CMOS limit |
| MIT6.111, Fall2017, *Lecture4 Sequential Logic* | [Original PDF](https://web.mit.edu/6.111/www/f2017/handouts/L04.pdf), slides10–19 and22–23; slide17 visually checked | Register min/max, setup/hold, signed skew event inequalities, RC half transition and scheduled HDL assignments. Some slides carry older dates and third-party adaptation notices; no figures are copied. No physical timing measurements |
| Chris Terman, MIT6.004, Spring2017, *5.1 Annotated Slides* | [Original written course](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/), latch/register dynamic discipline and register-to-register constraints | Independent corroboration of setup/hold and no-period hold repair. No video is required. The separate6.1 page did not yield the searched synchronizer passage; it is not cited as inspected evidence for metastability |
| Chris Wellheuser, Texas Instruments, *Metastability Performance of Clocked FIFOs*, SCZA004A, copyright1996 | [Manufacturer PDF](https://www.ti.com/jp/lit/pdf/scza004), printed pp5–7, equations1–4 | Sampling-aperture/nonresolution distinction, resolution-time model and synchronization limits. Historical hardware parameters/results are not reproduced or used as current-device guarantees |
| BIPM, *SI: Defining constants* | [Official table](https://www.bipm.org/en/measurement-units/si-defining-constants), elementary-charge row | Exact SI value1.602176634×10^-19 C; floating representation remains approximate |
| OpenStax, Flowers et al., *Chemistry2e*, §8.4 Band Theory | [Primary book](https://openstax.org/books/chemistry-2e/pages/8-4-molecular-orbital-theory), selected band/occupation discussion | Qualitative allowed-state bridge. The chapter's simplified conductor-gap description is not used as a universal metal model. A full band calculation is outside scope |

Circuit uniqueness, independent quadratic oracle, numerical energy residual,
Boolean adder/network proofs, timing examples and synthetic experiments are
original repository work. MIT OCW terms include third-party exceptions; TI's
report is copyrighted; the BIPM/OpenStax originals state their own terms. Public
reading does not grant a repository-wide license. No uninspected modern component
pinout, rating, threshold or timing guarantee is asserted.
