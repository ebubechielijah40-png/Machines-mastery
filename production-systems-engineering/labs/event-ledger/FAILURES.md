# Failures

Tests inject an exception before commit, duplicate/conflicting identities, malformed types, lock contention and cache incoherence from a second instance. Recovery checks retry after rollback/lock release and clear stale cache before reading again. The two-instance test deliberately demonstrates the cache boundary; a passing demonstration is not a repaired multi-writer service. Do not fill disk or kill arbitrary processes: future storage/process fault tests must target bounded temporary artifacts and owned child processes only.
