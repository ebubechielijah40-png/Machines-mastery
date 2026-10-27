# Build a reproducible measurement analysis

Analyze a bounded batch of explicitly synthetic temperature readings. Build strict ingestion, exact arithmetic, a declared calibration model, standard uncertainty propagation, content/source identity and a controlled correlation experiment. Then carry the distinction between data identity and trusted origin into the [authenticated pipeline](../p09-secure-pipeline/README.md). This is an executed computation on synthetic inputs, not a claim that any physical temperature was measured.

Entry gate: compute a mean, a squared deviation and a variance; distinguish milli-Celsius from Celsius. Review [algebra and functions](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md) and [scientific reasoning](../../09-scientific-reasoning/SELF_CONTAINED_GUIDE.md). Learn the equations below before running the reference. Tools: Python 3.12 standard library; no external dataset or packages.

## Define the measurand before the file

The quantity of interest is a constant temperature under unchanged measurement conditions. Our model is `Y = mean(X_1,...,X_n)+B`, with one estimated calibration correction B shared by all readings. Reading errors are assumed independent of one another and of B. Their distribution is not inferred merely from parsing CSV. The file declares integer milli-Celsius values; one unit equals 0.001 °C. Sequence numbers identify order, not elapsed time: this dataset has no timestamps and cannot establish a heating rate or temporal independence.

[synthetic.csv](data/synthetic.csv) contains 25000, 25002, 24998 milli-Celsius. Hand calculation gives mean 25000, deviations 0,2,-2 and squared deviations totaling eight. The sample variance is `s²=8/(3-1)=4` milli-Celsius squared. Dividing by n estimates the variance of an independent-reading mean, `u_A²=s²/n=4/3`. With correction B=-10 milli-Celsius and supplied calibration standard uncertainty `u_B=5` milli-Celsius, the result is 24990 milli-Celsius = 24.990 °C, with combined standard uncertainty `sqrt(4/3+25)/1000 ≈ 0.005132 °C`. The supplied five is a synthetic assumption, not a calibration certificate.

Why divide the scatter sum by n-1? The residuals sum to zero because the mean was fitted from the same n samples, leaving n-1 independent residual degrees of freedom. Under independent equal-variance readings, expanding `sum((X_i-mean X)²)` gives expected value `(n-1)σ²`. This makes s² unbiased for individual-reading variance under that model. It does not make a three-point sample a reliable estimate for every instrument.

## Where uncertainty comes from

Write `mean X = true mean + mean error`. Variance of a sum expands into individual variances plus twice each pairwise covariance. If reading errors have variance σ² and zero covariance, variance of their mean is `n*σ²/n²=σ²/n`. A single shared correction contributes once, giving

\[
u_c^2 = s^2/n + u_B^2.
\]

For this linear model the variance algebra is exact when the covariance assumptions hold. The general nonlinear propagation law uses a local approximation; do not infer it by blindly summing squared terms [M2]. Standard uncertainty characterizes a standard deviation estimate. It is not automatically a 95% confidence interval, worst-case error bound or statement that the true temperature lies within a particular observed interval [M1].

Counterexample: if every reading has the same uncertain offset E, averaging produces `true temperature + E`; its variance remains Var(E), regardless of n. Treating the calibration correction as a fresh independent error on every sample would incorrectly divide its contribution by n. Identical numerical readings can still have nonzero calibration uncertainty. Duplicating CSV rows also creates no new independent observations even if the schema accepts freshly numbered copies.

## A bounded, reproducible mechanism

[measurement_pipeline.py](code/measurement_pipeline.py) accepts immutable bytes, an exact ASCII header `seq,value_milli_c`, two to 10000 complete ordered rows, integer values in [-50000,150000], a 200000-byte input limit and a complete final newline. It rejects missing/duplicate/out-of-order sequence numbers, floats, leading-zero ambiguity, unknown columns, malformed units and extra blank rows. This narrow CSV dialect is deliberate; it is not a general CSV import library. `read_bounded` reads at most limit+1 bytes so an oversized file can be rejected without unbounded ingestion.

The implementation uses Fraction for mean and variances, preserving an independently checkable numerator/denominator. Only the final square root becomes a floating approximation. It records SHA-256 of exact input bytes, configuration, transform identifier and the source file used. Repeated input/config/source produce identical JSON content on this runtime. Input order changes the input digest even when summary statistics remain equal. The source digest identifies code bytes; it does not prove the code correct or authenticate an attacker-replaced manifest.

Storage is linear in row count; Fraction arithmetic here has bounded numeric inputs but is not a general large-dataset performance strategy. There is no parallel merge, database transaction, streaming checkpoint, missing-data model, outlier removal, or calibration drift estimation. Valid syntax is a prerequisite for analysis, not evidence that the data-generating assumptions hold.

## Guided milestones and acceptance

| Stage | Build before reading the reference | Independently checkable checkpoint |
| --- | --- | --- |
| A0 | Write the measurand, units, correction sign, independence assumptions and byte/row policy | Hand-derived three-point result and unit conversion |
| A1 | Parse strict bytes into ordered integer observations | Truncation, duplicate sequence, decimal and unknown-unit cases reject |
| A2 | Compute exact mean and sample variance | Use the independent identity `s²=sum_ij(x_i-x_j)²/[2n(n-1)]` as an oracle |
| A3 | Add shared correction and combined standard uncertainty | Correction changes mean; zero scatter still leaves calibration uncertainty |
| A4 | Record input/configuration/source identity | Same inputs reproduce; altered bytes change input digest |
| A5 | Execute correlation experiment | Compare shared-offset and independent-offset variances separately |
| A6 | Reconstruct without reference | Explain why copying rows or averaging shared errors does not buy independence |

Use the complete runnable reference as an oracle after a design attempt, not as the first learner deliverable. Submit code, hand derivation, test results, an assumptions ledger, actual experiment JSON and one counterexample. Assessment weights: mathematical model/units 35%, schema/resource behavior 25%, independent checks/reproduction 25%, interpretation/limits 15%. A tiny uncertainty produced by an unjustified independence assumption fails the modeling requirement.

Run from repository root:

```sh
python3 -m unittest discover -s projects-guided/p08-scientific-pipeline/code -v
python3 projects-guided/p08-scientific-pipeline/code/experiment.py
```

The controlled simulation varies n across 1,4,25,100 while holding independent reading standard deviation 2 milli-Celsius, calibration standard deviation 5 milli-Celsius and 10000 trials fixed. In one model each trial has a single shared Gaussian calibration error; in the comparison each sample gets an independent calibration draw. Predictions are `25+4/n` and `29/n` milli-Celsius squared. [Actual observations](evidence/observed.json) and environment are kept separately from these predictions. Finite simulation agreement supports the implementation under this synthetic model; it does not verify the independence or Gaussian assumptions of any real instrument.

Do [exercises](EXERCISES.md), then [hints](HINTS.md), then [solutions](SOLUTIONS.md). Verified source scopes are in [SOURCES.md](SOURCES.md). This bounded project is STRONG within its synthetic scope; the wider scientific-computing/data-engineering domains remain PARTIAL.
