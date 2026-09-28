# Experiments

- n = 1k, 10k, 100k, 1M if your machine permits; measure query latency before/after index.
- high-selectivity vs low-selectivity predicates.
- single-column vs composite index with query order changes.
- write/insert cost before/after index.
- page/cache effects: repeat query and distinguish warm from cold-cache assumptions.
- `ORDER BY` and covering-index opportunities.

Record query plan and data distribution with every timing. A faster result on one dataset is not a universal proof.
