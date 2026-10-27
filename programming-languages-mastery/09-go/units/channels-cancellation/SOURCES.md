# Inspected Go scopes

Root inspected2026-10-23 after native author execution:

- Official [Go memory model](https://go.dev/ref/mem), versionJune6,2022, Channel
  communication and Goroutine destruction: send/receive/close ordering and the
  absence of an automatic synchronization edge from goroutine exit.
- Official [language specification](https://go.dev/ref/spec), displayed language
  versiongo1.27, Select statements and slice/append contracts: ready-case choice
  and shared backing storage. These selected rules do not establish full runtime
  implementation or compiler behavior.
- Official [context](https://pkg.go.dev/context) Context/Done scope and
  [race detector documentation](https://go.dev/doc/articles/race_detector), usage/
  executed-path limitations. No automatic interruption or exhaustive proof is claimed.

The finite API, input-copy policy, index/order proof, examples and experiments are
original. Actual Go1.27.3 execution is retained in evidence/observed.json with
commands and controlled environment. Official tool downloads/checksums were kept
outside the repository; no compiler binary or source manual is distributed here.
