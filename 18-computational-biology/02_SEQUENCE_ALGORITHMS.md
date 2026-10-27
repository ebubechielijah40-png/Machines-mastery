# Sequence alignment: derive the objective, table, and reconstruction

This unit replaces the former instruction to "implement alignment" with a complete bounded learning path. It develops exact global and local alignment under an **integer, linear-gap scoring model**, with a runnable implementation, a small independent exhaustive oracle, synthetic experiments, and a guided FASTA workbench. It does not establish biological function, ancestry, or clinical meaning.

Read this lesson before opening [exercises](alignment/EXERCISES.md). [Hints](alignment/HINTS.md) and [solutions](alignment/SOLUTIONS.md) are deliberately separate. Historical claims and inspected source boundaries are in [source verification](alignment/SOURCE_VERIFICATION.md). All examples, derivations, code, exercises, and measurements here are original teaching work.

## 1. A concrete failure of position-by-position comparison

Suppose one recorded sequence is `AG` and another is `ACG`. Comparing the first positions finds A/A, then comparing second positions finds G/C. That misses a simpler account: the second sequence contains one extra C between A and G. An **alignment** introduces a gap symbol to express a proposed correspondence:

| Column | Sequence A | Sequence B | Meaning in the model |
| --- | --- | --- | --- |
| 1 | A | A | Match |
| 2 | - | C | Symbol in B with no paired symbol in A |
| 3 | G | G | Match |

The gap is a display instruction. It is not a chemical molecule or an observed insertion event. We have recorded strings; the history producing them is unobserved. A scoring model ranks possible correspondences. Different scores can prefer different explanations.

The original Needleman–Wunsch paper developed a matrix/path approach to sequence comparison, while Smith–Waterman developed a maximum-similarity segment search permitting internal insertions/deletions [NW70, SW81]. Our derivation below is a modern restricted linear-gap teaching model, not a transcription of either original algorithm. In particular, SW81 allows more general length-dependent deletion weights than the three-candidate implementation here.

## 2. Prerequisite bridge, built into this lesson

A **string** is an ordered list of symbols. `a = "AG"` has length 2. Python indices start at zero: `a[0]` is A, `a[1]` is G. A **prefix of length i** contains the first i symbols; the length-zero prefix is empty. `a[:i]` is Python's spelling. The slice `a[start:end]` includes start and excludes end, so `a[1:2]` has length 1.

An integer score adds rewards and penalties. Here match = 2, mismatch = -1, gap = -2. These are **dimensionless objective values**, not energy, probability, evolutionary time, or physical units. The maximum of `(-3, 0, -5)` is 0. Adding the same final-column score to all candidate prefixes preserves their order; this simple fact makes dynamic programming work.

A table with n+1 rows and m+1 columns stores one number per pair of prefix lengths. A cell's row coordinate i means "i symbols of a have been consumed"; its column coordinate j means "j symbols of b have been consumed." Zero-length prefixes need their own row and column. An **invariant** is a fact maintained as the algorithm runs. Our invariant will be: every completed cell holds the optimum for exactly its prefix problem.

Programming prerequisites are loops, indexing, conditions, tuples, functions, and exceptions; the preceding definitions make the mathematics accessible, but a learner who cannot yet write those constructs should first use the [Python route](../programming-languages-mastery/08-python/README.md). No mechanics, electronics, or chemistry is required to derive this string algorithm. Basic molecular context is provided in the [domain handbook](DEEP_HANDBOOK.md); the sparse molecular-foundations file remains an incomplete biology bridge. No learner mastery is inferred from executing the reference.

## 3. State the admissible objects before optimizing them

An alignment is two equal-length displayed strings obtained by inserting `-` into a and b, with no column containing two gaps. Removing gaps recovers the original inputs for **global** alignment. For **local** alignment it recovers a contiguous interval from each input. Internal gaps are allowed inside those intervals.

Our model permits adjacent columns that are a gap in opposite sequences. For example `A-`/`-C` is admissible. Some production alignment models exclude or constrain this; do not silently assume that restriction here.

For each column x/y define its score:

\[
s(x,y)=\begin{cases}r & x=y\text{ and neither is a gap}\\
q & x\ne y\text{ and neither is a gap}\\
g & \text{exactly one is a gap.}\end{cases}
\]

The alignment score is the sum of column scores. A run of k gaps costs kg: this is a **linear gap model**. We require integer r, q, and g, with g <= 0. Integers allow exact equality during traceback. A positive gap reward would incentivize long fragmented correspondences; a model permitting it would require a separate scientific justification, so this implementation rejects it. It does not require positive r or negative q; unusual values are allowed as mathematical experiments.

Inputs reserve `-` for display gaps. The core aligns generic symbols, is case sensitive, and does not normalize alphabets. The workbench separately accepts uppercased DNA `ACGTN`. There N is a literal unknown symbol, **not a wildcard**: N/A is a mismatch and N/N is a match. This is a stated toy convention, not a claim that two unknown bases are equal.

## 4. Derive the global recurrence

Let F(i,j) be the highest score among all global alignments of `a[:i]` and `b[:j]`. Consider the **last column** of any such alignment. Only three possibilities consume input:

| Last column | Previously consumed prefixes | Added score |
| --- | --- | --- |
| `a[i-1] / b[j-1]` | i-1 and j-1 | r if equal, otherwise q |
| `a[i-1] / -` | i-1 and j | g |
| `- / b[j-1]` | i and j-1 | g |

There is no fourth gap/gap option: it would consume nothing. Consequently,

\[
F(i,j)=\max\{F(i-1,j-1)+s(a_{i-1},b_{j-1}),\;F(i-1,j)+g,\;F(i,j-1)+g\}.
\]

The boundary is not decoration. Aligning i symbols with the empty string requires i gap columns, so F(i,0)=ig. Likewise F(0,j)=jg and F(0,0)=0. Initializing the whole first row and column to zero would make terminal deletions free and solve a different problem.

**Why this is a proof rather than a guess.** Every possible final column is in the table above. If a supposedly optimum alignment used a non-optimum preceding prefix alignment, replace that prefix by a better one and keep its last column. The total would increase, contradicting optimality. Conversely, appending each valid column to an optimum predecessor constructs an admissible candidate. The maximum therefore is both an achievable score and an upper bound on all possible scores. Induction over i+j proves the invariant. Filling rows top to bottom and columns left to right ensures every predecessor has already been computed.

This argument relies on scores adding by column, without dependence on the earlier path. Change to a gap-opening cost plus gap-extension cost and the table state must remember whether a gap is already open. One scalar cell no longer carries enough information for the same three local candidates.

## 5. Work the entire small matrix

Take a=`AG`, b=`ACG`, r=2, q=-1, g=-2. Row/column labels below show the consumed symbol, with empty prefix first.

| F | empty | A | C | G |
| --- | ---: | ---: | ---: | ---: |
| empty | 0 | -2 | -4 | -6 |
| A | -2 | 2 | 0 | -2 |
| G | -4 | 0 | 1 | 2 |

F(1,1)=max(0+2, -2-2, -2-2)=2. F(1,2)=max(-2-1, -4-2, 2-2)=0. The zero here means one match followed by one gap, not a local restart. F(2,2)=max(2-1, 0-2, 0-2)=1. F(2,3)=max(0+2, -2-2, 1-2)=2.

The last cell gives the optimum **score**. It does not by itself identify the alignment. Start at (2,3): its value came from the diagonal (1,2), so append G/G. At (1,2) the best predecessor is left (1,1), so append -/C. At (1,1) append A/A and reach (0,0). These columns were visited backwards. Reverse them to recover `A-G`/`ACG`, scoring 2-2+2=2.

The [test suite](code/test_alignment.py) checks the entire worked matrix and displayed output. It also rescans columns with a separate scoring function and checks that removing gaps reconstructs the consumed input. These independent invariants catch a correct score combined with a broken traceback.

## 6. Ties are model ambiguity, not a coding accident

Under r=1, q=-1, g=-1, `AA` against `A` has two optimum alignments: `AA`/`-A` and `AA`/`A-`, both score 0. The inputs and scores cannot decide which A is "the" corresponding residue.

The implementation chooses diagonal before up before left whenever predecessor scores tie. In the example its traceback chooses the second A for the match, yielding `AA`/`-A`. This creates reproducible output, not extra evidence. For local alignment it chooses the first maximum endpoint in row-major order and stops at a zero cell. Enumerating all optima would require retaining all tied predecessors and may produce exponentially many outputs.

An empty global input against `AC` yields `--`/`AC`, score -2 with defaults. Two empty strings score 0. Global scores may be negative; clamping them to zero changes the objective. With q=-5 and g=-1, `A` against `C` prefers the two permitted opposing-gap columns, score -2, over a mismatch, score -5. This counterexample exposes a consequential modeling choice instead of hiding it with a convenient test case.

## 7. Derive the local recurrence and its coordinates

Perhaps only a shared motif matters: `TTACGTAA` and `GGACGTCC` have dissimilar flanks around `ACGT`. Global alignment must account for every symbol. Local alignment asks for the highest-scoring pair of **contiguous intervals**, permitting internal gaps. The boundary changes to H(i,0)=H(0,j)=0 and:

\[
H(i,j)=\max\{0,\;H(i-1,j-1)+s(a_{i-1},b_{j-1}),\;H(i-1,j)+g,\;H(i,j-1)+g\}.
\]

Zero means "choose an empty prefix here and start anew." If a proposed segment starts with a negative-scoring prefix, discarding that prefix improves its score. Thus the same optimal-substructure argument applies, now with a restart option. Track the largest cell anywhere, not just H(n,m), and trace backwards until a zero cell. With all matches unfavorable, the empty alignment wins with score 0.

At r=2, q=-3, g=-2 the flanked example returns score 8 and `ACGT`/`ACGT`. Both intervals are [2,6), referring to zero-based indices in the original inputs. Its local score is not directly comparable with the global score as evidence of quality: the two methods optimize different admissible objects.

**Incorrect approach:** globally align the whole strings, then trim bad ends. The optimum whole-string alignment can choose different internal gaps to pay for flanks. Trimming its output does not generally recover the optimum local interval. Likewise, selecting the longest exact common substring forbids internal mismatches and gaps and answers a narrower question.

## 8. Implement and investigate

The reference mechanism is [alignment.py](code/alignment.py). Read the API contract before running it. From the repository root, with Python 3.10+ and no third-party packages:

```sh
python3 -m unittest discover -s 18-computational-biology/code -p 'test_alignment.py' -v
python3 18-computational-biology/code/test_sequence_lab.py
python3 18-computational-biology/code/alignment_experiment.py
```

`Alignment` returns score, both displayed strings, input intervals, the score table, and the number of interior cells evaluated. The old `sequence_lab.global_alignment()` tuple API delegates to this implementation. Its formerly implicit score contract is now checked: integer scores and nonpositive gaps. A table-cell budget rejects oversized requests before allocation; it counts cells, not memory bytes.

To build it yourself: implement boundaries first, then row filling, then explicit traceback directions, then display reversal, then input reconstruction checks. Write the global version before changing to local boundaries/restart/endpoint selection. Keep the scoring function independent from the optimizer. Implement one deterministic tie policy and test it with repeated symbols.

The test oracle enumerates **every column path** for very short strings, without dynamic programming or memoization. It compares 675 global cases across three score settings. For local alignment it independently enumerates every pair of contiguous input intervals and all their global paths, checking 147 cases. This is stronger than comparing an implementation against a second copy of its own recurrence. It is still bounded evidence, not proof for arbitrary inputs; the recurrence proof supplies that separate argument.

## 9. Experiments: objective sensitivity and finite resources

Use the [experiment protocol and actual observations](alignment/EXPERIMENTS.md). The script varies only gap cost for a fixed pair, compares global/local objectives on fixed flanked inputs, enumerates a composition-preserving toy null, and measures increasing input sizes. Raw measured outputs and environment are preserved in [results.json](alignment/evidence/results.json). These are agent measurements, not learner experiments and not reproductions of reported paper results.

**Interpretation discipline:** an alignment is optimum for the selected score model. That proves neither ancestry nor the mechanism that produced the strings. Repeated symbols generate high scores by chance; maximizing over many candidates creates selection effects. A conditional permutation tail fraction answers a question under its specified null, not under every biological process. Changing a score parameter after inspecting outcomes further weakens an uncorrected significance claim.

## 10. Complexity, engineering limits, and the next abstraction

There are nm interior cells and constant candidate work per cell, so arithmetic-operation complexity is O(nm) for this linear-gap recurrence. Python big-integer arithmetic also grows with score bit length; the usual bound assumes fixed-size scores. Full table plus traceback storage is O(nm); output traceback has at most n+m columns. A score-only variant can retain two rows, O(min(n,m)) auxiliary cells, but loses the ordinary traceback path. Space-reduced reconstruction requires an additional algorithm and proof, not merely deleting the table.

Whole genomes are far beyond this pure Python full-table implementation. A cell is not one byte: Python lists, integer objects, two working tables, and the returned immutable table add overhead. `max_cells` is a predictable guard rather than a precise memory quota. The CLI separately bounds raw input bytes. Do not expose it as an unbounded public service; concurrent jobs multiply memory demand. For real data consider validated libraries, formats/quality information, established score matrices, better gap models, indexing/seeding, resource isolation, and documented approximations. None is implemented by this unit.

The guide covers pairwise alignment only. KMP, edit distance as a separate cost formulation, suffix/FM indexes, read mapping, assembly, affine-gap optimization, protein substitution matrices, and calibrated significance need additional instruction and executable evidence. This unit does not mark the computational-biology domain complete.

Continue with the [guided workbench](../projects-guided/p14-bioinformatics/README.md), then attempt the reconstruction challenge without consulting the code.
