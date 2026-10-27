# Executed scientific checks

Run `python3 -m unittest discover -s projects-guided/p08-scientific-pipeline/code -v`. The [saved log](evidence/tests.txt) records six methods: hand-derived exact three-point result, offset/scatter distinction, zero-scatter calibration floor, content identity/determinism, an independent pairwise variance oracle, and schema/order/unit/range/truncation rejection.

The independent variance identity uses pairwise differences rather than duplicating the implementation's centered-square loop. Exact rational assertions distinguish denominators4/3 and79/3; approximate comparison is limited to the final square root. These checks establish bounded calculation behavior, not physical calibration validity, input independence, statistical coverage or large-scale data-engineering performance.
