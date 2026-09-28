# Postmortem: Simulated Network Partition and Split-Brain Prevention

## Incident Summary
- **Simulated Condition:** Network link between node 1 and the remainder of a 3-node cluster ({node 2, node 3}) was severed during high write volume.
- **Observed Behavior:** Node 1 accepted client write requests into its local log but did not commit them, as it could not reach a quorum of 2 nodes. Simultaneously, nodes 2 and 3 elected node 2 as the new leader and continued committing writes.
- **Impact:** Writes sent to the minority leader stalled rather than returning false success. No divergent state was committed.
- **Root Cause & Mechanism:** Physical partition severed heartbeat propagation. Quorum check `matches >= 2` correctly failed on node 1.
- **Recovery:** Upon partition healing, node 1 discovered node 2's higher term, stepped down to follower, truncated uncommitted entries, and reconciled state cleanly.
- **Preventative Action:** Return explicit `NOT_LEADER` or partition error to client after bounded election timeout to allow rapid client failover to the active majority leader.
