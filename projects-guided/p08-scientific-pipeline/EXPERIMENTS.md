# Shared-error versus independent-error experiment

Question: can averaging remove calibration uncertainty? Competing hypotheses are one calibration error shared across readings versus a fresh independent calibration error per reading. Hold reading standard deviation2, calibration standard deviation5 (both milli-Celsius), trial count10000 and public seed493; vary n through1,4,25,100. Instrument variance of repeated trial means. Predictions are25+4/n and29/n in squared units.

Run `python3 projects-guided/p08-scientific-pipeline/code/experiment.py`. [Actual JSON](evidence/observed.json) records environment, exact small-example statistics and simulation. At n=100, observed variances are24.8970551 for shared calibration versus prediction25.04, and.2921411 for independent calibration versus prediction.29. Finite trial variation and RNG draw order explain numerical deviations; no physical experiment was performed.

Follow-up: interleave standards and record time to investigate drift/correlation in a real instrument. Selection bias, nonlinear response and changing conditions are not included in either synthetic model. A source checksum cannot validate those assumptions.
