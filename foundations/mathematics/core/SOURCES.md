# Source inspection and authorship boundary

Verified on 2026-10-23. The instruction, examples, exercises, code and deterministic
experiments in this unit are original. These sources check definitions and
mechanisms; no source's full text, figures, exercises or code is redistributed.
Inspection of selected sections does not certify an entire book or subject.

| ID | Primary resource and inspected scope | What it supports here | Limits |
| --- | --- | --- | --- |
| M-VMLS | Stephen Boyd and Lieven Vandenberghe, *Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares*, Cambridge University Press; [author page](https://web.stanford.edu/~boyd/vmls/) and [author-hosted PDF](https://web.stanford.edu/~boyd/vmls/vmls.pdf). Cover, §§2.1,10.1–10.2,11.2 and12.1–12.2 selected bodies inspected; printed pp29–31,177–184,202–204,225–229. | Linear/affine distinction, composition, inverse conditions, residual objective and gradient. | Row-scaled elimination, examples, implementation and stability experiment are original; this is not a reconstruction of all the book's content. PDF date/version not inferred from the changing web page. |
| M-CHAIN | [OpenStax *Calculus Volume 1*, §3.6](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule), theorem/assumptions and proof around equation3.17 inspected. | Chain rule under differentiability assumptions. | Our first-order argument and computational graph are original; not a proof of every multivariable analysis theorem. |
| M-GCD | Albert R. Meyer, MIT6.042J/18.062J, March6,2015, [GCDs and linear combinations](https://courses.csail.mit.edu/6.042/spring18/gcd-def.pdf) and [Euclidean algorithm](https://courses.csail.mit.edu/6.042/spring18/gcd-euclid.pdf), all three pages of each inspected. | Division theorem, common-divisor invariant, termination and linear combinations. | Full 2018 coursebook web fetch was too large; do not count that book as inspected. Modular exponentiation here is independently derived. |
| M-C11 | ISO/IEC JTC1/SC22/WG14, [N1570 committee draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), April12,2011, §6.5.5¶5–6 and footnote105, printed p92, PDF page109 (zero based). | Signed integer division truncation, remainder identity and undefined zero/unrepresentable quotient cases. | A C11 draft, not a claim that every later standard or compiler was verified. |
| M-SI | BIPM, [SI Brochure landing page](https://www.bipm.org/en/publications/si-brochure), ninth edition2019 updated2026; linked *Concise Summary* pp2–5, quantities/derived units, prefix table and quantity calculus inspected. | Quantity versus numerical value, dimensions, milli conversion and units of rates/accumulation. | No claim of calibrated physical measurement. Landing page states CC-BY4.0; no source wording or tables copied. |
| M-GEOMETRY | OpenStax, *Algebra and Trigonometry2e*, [§7.3 Unit Circle](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-3-unit-circle), sine/cosine definitions and ranges; [§10.5 Polar Form](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-5-polar-form-of-complex-numbers), modulus, rectangular/polar conversion and product mechanism. | Coordinate definitions, radians and complex polar arithmetic. | Original area construction/diagram and worked arithmetic here; no source problems, illustrations or prose copied. Complex exponential series are not reconstructed. |

The locally inspected VMLS PDF had7,061,628 bytes and SHA256
`254738c8763f6c6fc29c0a837884bc58deca7c3e762e5ec79068208ac7214362`.
The author's page explicitly identifies Cambridge University Press as copyright
holder and web availability by permission. The PDF was used privately for
verification and is excluded from this repository and release archive.

The derivative/rounding/error propagation foundation has its own
[source record](../change-error-and-evidence/SOURCES.md). Matrix sensitivity,
trapezoid error and diagonal update bounds here follow the displayed original
algebra and can be checked against exact rational formulas, rather than relying
on a generic external recommendation or an uninspected paper.
