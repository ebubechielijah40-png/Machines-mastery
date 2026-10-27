# Meaningful checks and executed scope

The project suite has four tests: partition/exchange/duplicate/causal write,
tombstone versus empty-string value, invalid identity/message/schema controls,
and actual CLI success plus duplicate-JSON-field rejection. Run the exact
commands in [README](README.md). They passed during integration.

The core's eight tests separately check all24 delivery permutations plus
duplicates, keywise merge identities, deletion/resurrection, state/clock failure
atomicity, bounded overflow, immutable snapshots and an Envelope send counter
that exceeds all stored record counters. Their independent expected winner
comes from a fixed stamp order rather than reusing the join function.

Passing a finite schedule is not a linearizability test or proof of network
failure recovery. The algebra supplies a conditional convergence argument;
valid histories and eventual delivery remain assumptions. No benchmark,
physical-clock measurement or hostile multi-tenant execution was performed.
