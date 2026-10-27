# Exercises: measurement analysis

1. Hand-compute mean, sample variance, mean variance and corrected result for 1000,1004,1002 milli-Celsius with correction +20 and standard calibration uncertainty 3 milli-Celsius.
2. Derive `Var(mean X)` including covariance. If every distinct pair has covariance c and every reading variance σ², what happens as n grows?
3. Explain why `value_milli_c=25000.0` rejects even though it denotes an integer mathematically. Propose a versioned format accepting decimal Celsius without silently changing the existing protocol.
4. Use the pairwise-difference identity to test sample variance independently. Why is writing the identical sum-of-squares loop in your expected-value code weaker evidence?
5. Run the shared/independent calibration experiment. Record observed error from each prediction. List two real-world effects missing from both models.
6. A colleague hashes the input and stores the hash beside it. Can an attacker who may replace both establish a different history that passes? Explain the extra authority needed in the next project.
7. Reconstruction: implement ingestion, exact rational statistics and the shared-correction model without consulting the source. Include zero scatter, minimum two samples, failed schema, and reordered-content digest tests.
8. Transfer: a sensor drifts during the batch. What additional observations or experiment design could distinguish drift from independent reading noise? State why the present dataset cannot resolve that question.
