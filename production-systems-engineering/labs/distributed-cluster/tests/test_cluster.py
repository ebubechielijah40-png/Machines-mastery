"""Test suite for distributed cluster quorum consensus, failure injection, and security."""
import sys
import unittest
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_DIR))

from cluster import DeterministicNetwork, RaftNode, Message


class ClusterTests(unittest.TestCase):
    def setUp(self):
        self.net = DeterministicNetwork(latency_ticks=1, drop_rate=0.0, seed=123)
        self.node_ids = ["node-1", "node-2", "node-3"]
        self.nodes = {nid: RaftNode(nid, self.node_ids, self.net) for nid in self.node_ids}

    def _elect_leader(self, candidate_id: str) -> RaftNode:
        candidate = self.nodes[candidate_id]
        candidate.start_election()
        self.net.step(ticks=4)
        self.assertEqual(candidate.state, RaftNode.LEADER)
        return candidate

    def test_election_and_normal_quorum_write(self):
        leader = self._elect_leader("node-1")
        ok, status, _ = leader.client_write(key="balance", value="500", client_id="user-1", request_id=1)
        self.assertTrue(ok)
        self.assertEqual(status, "APPENDED_PENDING_QUORUM")

        self.net.step(ticks=6)
        self.assertEqual(leader.commit_index, 0)
        self.assertEqual(leader.state_machine.get("balance"), "500")

        for nid, node in self.nodes.items():
            self.assertEqual(node.state_machine.get("balance"), "500", f"{nid} did not commit state")
            self.assertEqual(node.commit_index, 0)

    def test_idempotent_replay_handling(self):
        leader = self._elect_leader("node-1")
        leader.client_write("balance", "500", "user-1", 1)
        self.net.step(ticks=4)
        self.assertEqual(len(leader.log), 1)

        ok, status, val = leader.client_write("balance", "500", "user-1", 1)
        self.assertTrue(ok)
        self.assertEqual(status, "COMMITTED_IDEMPOTENT")
        self.assertEqual(val, "500")
        self.assertEqual(len(leader.log), 1)
        self.assertEqual(leader.metrics["replays_handled"], 1)

    def test_partition_split_brain_prevention(self):
        leader = self._elect_leader("node-1")
        leader.client_write("counter", "1", "c1", 1)
        self.net.step(ticks=6)
        self.assertEqual(leader.state_machine["counter"], "1")

        self.net.partition({"node-1"}, {"node-2", "node-3"})

        ok, status, _ = leader.client_write("counter", "2", "c1", 2)
        self.assertTrue(ok)
        self.net.step(ticks=10)

        self.assertEqual(leader.commit_index, 0)
        self.assertEqual(leader.state_machine["counter"], "1")

        new_leader = self.nodes["node-2"]
        new_leader.start_election()
        self.net.step(ticks=6)
        self.assertEqual(new_leader.state, RaftNode.LEADER)

        ok, status, _ = new_leader.client_write("counter", "999", "c2", 1)
        self.assertTrue(ok)
        self.net.step(ticks=8)

        self.assertEqual(new_leader.commit_index, 1)
        self.assertEqual(new_leader.state_machine["counter"], "999")
        self.assertEqual(self.nodes["node-3"].state_machine["counter"], "999")

    def test_partition_healing_and_log_reconciliation(self):
        leader = self._elect_leader("node-1")
        leader.client_write("val", "initial", "c", 1)
        self.net.step(ticks=6)

        self.net.partition({"node-1"}, {"node-2", "node-3"})
        leader.client_write("val", "uncommitted_stale", "c", 2)
        self.net.step(ticks=6)
        self.assertEqual(leader.commit_index, 0)

        new_leader = self.nodes["node-2"]
        new_leader.start_election()
        self.net.step(ticks=6)
        new_leader.client_write("val", "committed_majority", "c", 3)
        self.net.step(ticks=8)

        self.net.heal_partitions()
        new_leader._broadcast_heartbeat()
        self.net.step(ticks=6)

        self.assertEqual(self.nodes["node-1"].state, RaftNode.FOLLOWER)
        for nid in self.node_ids:
            self.assertEqual(self.nodes[nid].state_machine["val"], "committed_majority")

    def test_security_tampering_and_replay_rejection(self):
        n1 = self.nodes["node-1"]
        n2 = self.nodes["node-2"]

        tampered_msg = Message(src="node-1", dst="node-2", msg_type="REQUEST_VOTE",
                               term=1, payload={"candidate_id": "node-1", "last_log_index": -1, "last_log_term": 0},
                               nonce=1, token="forged-bad-token")
        n2.receive(tampered_msg)
        self.assertEqual(n2.metrics["security_violations"], 1)

        valid_msg = Message(src="node-1", dst="node-2", msg_type="REQUEST_VOTE",
                            term=1, payload={"candidate_id": "node-1", "last_log_index": -1, "last_log_term": 0},
                            nonce=1)
        valid_msg.token = valid_msg.compute_token(n1.secret)
        n2.receive(valid_msg)
        self.assertEqual(n2.last_seen_nonce["node-1"], 1)

        n2.receive(valid_msg)
        self.assertEqual(n2.metrics["security_violations"], 2)


if __name__ == '__main__':
    unittest.main()
