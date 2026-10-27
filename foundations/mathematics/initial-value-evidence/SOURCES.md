# Actual source scope and original work

Selected original sources were opened on2026-10-25. This unit's lesson, code,
parameter choices, examples, questions, exact Fraction oracles, invariant and
missed-pulse experiment are original instructional constructions. No full PDF,
extracted source text, source figure, upstream implementation or copied exercise
is bundled. Access is not a blanket redistribution license.

| Source | Scope actually inspected | Supported use and limits |
| --- | --- | --- |
| MIT18.03, Class2,Feb3,2010, [Numerical Methods](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/e3df34d59f3f16db89d2043b7125c7aa_MIT18_03S10_c02.pdf) | Selected passages in6pages: IVP/tangent Euler construction, accumulated error, higher-order methods/evaluation costs | Numerical-method context and definitions. Individual note author is not identified by the PDF, so none is invented. Its informalC4(4h)^4=64C4h^4 line contains an arithmetic slip:4^4=256. That statement and outdated digit-record remarks are not adopted. |
| Masayuki Yano,James Douglass Penn,George Konidaris,Anthony T.Patera, [Math,Numerics,&Programming(for Mechanical Engineers),UnitIV](https://ocw.mit.edu/courses/2-086-numerical-computation-for-mechanical-engineers-spring-2013/64e7bed65373841c988a0fd98e1ae16e_MIT2_086S13_Unit4_Textbook.pdf), DRAFTV2.1,August2013 | Cover/version/rights; selected scalar Euler-forward/backward consistency/amplification passages; RK introduction and Example21.1.15,PDFpp38–42 | Formula/stability cross-check and scope of the general RK accuracy claim. Cover namesMIT/authors2011–2013,CCBY-NC-SA3.0; this is a draft, not an inferred later edition. No full coursebook reconstruction is claimed. |

The Euler error bound is derived with explicit Lipschitz/second-derivative
assumptions; abbreviated consistency/stability statements in teaching sources
are not promoted to an unrestricted theorem. Some sources divide a one-step
state defect byh before naming it truncation error. This unit uses state defect
O(h²) for Euler, distinguished from globalO(h); those conventions must not be
mixed.

Step doubling is justified conditionally by the displayedCh⁵ ansatz. It is not
attributed as a theorem certifying an arbitrary global error. Modified energy,
phase angle, waiting-time solution, blowup and pulse normalization are checked
by the original displayed algebra and tests. The numerical observations come
only from the newly executed local experiment, not from those sources or from
physical apparatus. Mathematical correctness and a source fingerprint do not
establish learner mastery or the correctness of a physical model.
