# Alignment source verification — 2026-10-22

Status applies only to the inspected scope below. Original copyrighted source files are not copied into this repository. Public access is not a redistribution license. This unit's code, worked strings, proofs, exercises, and experiments are original contributions; no blanket license is assigned here.

| ID | Primary work and original publication | Inspected source | Verified scope | Limitations |
| --- | --- | --- | --- | --- |
| NW70 | Saul B. Needleman and Christian D. Wunsch. *A General Method Applicable to the Search for Similarities in the Amino Acid Sequence of Two Proteins*. Journal of Molecular Biology 48(3), 443–453 (1970). DOI: [10.1016/0022-2836(70)90057-4](https://doi.org/10.1016/0022-2836(70)90057-4). | [University-hosted primary-paper scan](https://bytes.usc.edu/cs270/docs/needleman-wunsch-1970.pdf), retrieved through web open on 2026-10-22, PDF pages 1–5, printed pp. 443–447; metadata cross-checked against [PubMed 5420325](https://pubmed.ncbi.nlm.nih.gov/5420325/). | Introduction; section 2 matrix/path mechanism; section 3 randomized comparison; section 4 weighting; opening of section 5 application. | Remaining application tables/results, printed pp. 448–453, not inspected. No reproduction of original FORTRAN, protein comparisons, timings, or reported measurements is claimed. |
| SW81 | Temple F. Smith and Michael S. Waterman. *Identification of Common Molecular Subsequences*. Journal of Molecular Biology 147(1), 195–197 (1981). DOI: [10.1016/0022-2836(81)90087-5](https://doi.org/10.1016/0022-2836(81)90087-5). | [University-hosted primary-paper scan](https://cs.brown.edu/courses/csci1820/spring-2022/resources/Smith_Waterman_1981.pdf), web open on 2026-10-22, PDF pages 2–4, printed pp. 195–197; identity cross-check [PubMed 7265238](https://pubmed.ncbi.nlm.nih.gov/7265238/). | Algorithm equation (1), zero boundary and restart, maximum-cell traceback to zero, length-dependent deletion weights, illustrative worked example. | Scan OCR garbles some indices. The repository does not reproduce Figure 1 or its numerical result. Our linear-gap integer specialization differs from its more general deletion weights. |

## Claim-to-source map

- Historical matrix/path comparison and gap weighting: NW70, section 2, pp. 443–445.
- Composition-preserving randomized comparison as a way to investigate chance similarity: NW70, section 3, p. 446. Our 90-permutation experiment is an original toy, not that study's data or reproduction.
- Local segment objective, zero restart, maximum endpoint, and traceback stopping at zero: SW81, equation (1) and explanation, pp. 195–196.
- Original sources support the historical mechanism only within these scopes. The restricted modern recurrence, proof, coordinates, tie contract, resource caps, brute-force tests, and complexity analysis in this unit are original derivations tied to the executable code.

No modern biological benchmark, calibrated statistical significance, empirical homology claim, or gap-cost estimate is source-verified by this record. The standard-library tools used are inspectable source code in this repository; their results are execution evidence, not citations to the papers.
