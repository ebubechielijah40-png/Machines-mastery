# Sources: Distributed Quorum Consensus

## Primary Conceptual References
1. **Ongaro & Ousterhout (2014):** *In Search of an Understandable Consensus Algorithm* (Raft paper). Primary foundation for leader election, log replication, and safety invariants.
2. **Lamport (1998):** *The Part-Time Parliament* (Paxos). Foundation of majority quorum intersection to preserve state machine safety.
3. **Kleppmann (2017):** *Designing Data-Intensive Applications*, Chapter 8 (Trouble with Distributed Systems) and Chapter 9 (Consistency and Consensus). Foundation for network partition models and split-brain analysis.
4. **RFC 2104:** *HMAC: Keyed-Hashing for Message Authentication*. Foundation for inter-node message authentication tokens.
