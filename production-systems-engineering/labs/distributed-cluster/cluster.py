"""Deterministic simulated distributed replicated state machine with quorum consensus and failure injection."""
import hashlib
import hmac
import random
from typing import Dict, List, Optional, Set, Tuple


class Message:
    def __init__(self, src: str, dst: str, msg_type: str, term: int, payload: dict,
                 nonce: int = 0, token: str = ""):
        self.src = src
        self.dst = dst
        self.msg_type = msg_type
        self.term = term
        self.payload = payload
        self.nonce = nonce
        self.token = token

    def compute_token(self, secret: bytes) -> str:
        body = f"{self.src}:{self.dst}:{self.msg_type}:{self.term}:{self.nonce}:{sorted(self.payload.items())}"
        return hmac.new(secret, body.encode('utf-8'), hashlib.sha256).hexdigest()


class DeterministicNetwork:
    def __init__(self, latency_ticks: int = 1, drop_rate: float = 0.0, seed: int = 42):
        self.clock = 0
        self.latency_ticks = latency_ticks
        self.drop_rate = drop_rate
        self.rng = random.Random(seed)
        self.partitions: List[Tuple[Set[str], Set[str]]] = []
        self.queue: List[Tuple[int, Message]] = []
        self.metrics = {
            "sent": 0,
            "delivered": 0,
            "dropped_loss": 0,
            "dropped_partition": 0,
            "tampered_rejected": 0,
        }
        self.nodes: Dict[str, 'RaftNode'] = {}

    def register(self, node: 'RaftNode'):
        self.nodes[node.node_id] = node

    def partition(self, group_a: Set[str], group_b: Set[str]):
        self.partitions.append((set(group_a), set(group_b)))

    def heal_partitions(self):
        self.partitions.clear()

    def is_partitioned(self, src: str, dst: str) -> bool:
        for a, b in self.partitions:
            if (src in a and dst in b) or (src in b and dst in a):
                return True
        return False

    def send(self, msg: Message):
        self.metrics["sent"] += 1
        if self.is_partitioned(msg.src, msg.dst):
            self.metrics["dropped_partition"] += 1
            return
        if self.drop_rate > 0.0 and self.rng.random() < self.drop_rate:
            self.metrics["dropped_loss"] += 1
            return
        delivery_time = self.clock + self.latency_ticks
        self.queue.append((delivery_time, msg))

    def step(self, ticks: int = 1):
        target = self.clock + ticks
        while self.clock < target:
            self.clock += 1
            deliverable = [m for t, m in self.queue if t <= self.clock]
            self.queue = [(t, m) for t, m in self.queue if t > self.clock]
            for msg in deliverable:
                if msg.dst in self.nodes:
                    self.nodes[msg.dst].receive(msg)
                    self.metrics["delivered"] += 1


class LogEntry:
    def __init__(self, index: int, term: int, key: str, value: str, client_id: str, request_id: int):
        self.index = index
        self.term = term
        self.key = key
        self.value = value
        self.client_id = client_id
        self.request_id = request_id


class RaftNode:
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"

    def __init__(self, node_id: str, cluster_ids: List[str], net: DeterministicNetwork,
                 secret: bytes = b"cluster-shared-secret"):
        self.node_id = node_id
        self.cluster_ids = sorted(cluster_ids)
        self.net = net
        self.secret = secret
        self.quorum_size = (len(self.cluster_ids) // 2) + 1

        self.state = self.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.current_leader: Optional[str] = None

        self.log: List[LogEntry] = []
        self.commit_index = -1
        self.last_applied = -1
        self.state_machine: Dict[str, str] = {}
        self.client_responses: Dict[Tuple[str, int], str] = {}

        self.match_index: Dict[str, int] = {nid: -1 for nid in self.cluster_ids}
        self.next_index: Dict[str, int] = {nid: 0 for nid in self.cluster_ids}
        self.votes_received: Set[str] = set()

        self.nonce_out = 0
        self.last_seen_nonce: Dict[str, int] = {nid: 0 for nid in self.cluster_ids}
        self.metrics = {
            "writes_total": 0,
            "writes_committed": 0,
            "replays_handled": 0,
            "elections_started": 0,
            "terms_advanced": 0,
            "security_violations": 0,
        }
        self.net.register(self)

    def _sign_and_send(self, dst: str, msg_type: str, payload: dict):
        self.nonce_out += 1
        msg = Message(src=self.node_id, dst=dst, msg_type=msg_type,
                      term=self.current_term, payload=payload, nonce=self.nonce_out)
        msg.token = msg.compute_token(self.secret)
        self.net.send(msg)

    def receive(self, msg: Message):
        expected_token = msg.compute_token(self.secret)
        if not hmac.compare_digest(msg.token, expected_token):
            self.metrics["security_violations"] += 1
            self.net.metrics["tampered_rejected"] += 1
            return
        if msg.nonce <= self.last_seen_nonce.get(msg.src, 0):
            self.metrics["security_violations"] += 1
            self.net.metrics["tampered_rejected"] += 1
            return
        self.last_seen_nonce[msg.src] = msg.nonce

        if msg.term > self.current_term:
            self.current_term = msg.term
            self.state = self.FOLLOWER
            self.voted_for = None
            self.metrics["terms_advanced"] += 1

        if msg.msg_type == "REQUEST_VOTE":
            self._handle_request_vote(msg)
        elif msg.msg_type == "VOTE_REPLY":
            self._handle_vote_reply(msg)
        elif msg.msg_type == "APPEND_ENTRIES":
            self._handle_append_entries(msg)
        elif msg.msg_type == "APPEND_REPLY":
            self._handle_append_reply(msg)

    def start_election(self):
        self.state = self.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.metrics["elections_started"] += 1
        self.metrics["terms_advanced"] += 1

        last_term = self.log[-1].term if self.log else 0
        last_index = len(self.log) - 1
        for peer in self.cluster_ids:
            if peer != self.node_id:
                self._sign_and_send(peer, "REQUEST_VOTE", {
                    "candidate_id": self.node_id,
                    "last_log_index": last_index,
                    "last_log_term": last_term,
                })

    def _handle_request_vote(self, msg: Message):
        candidate = msg.payload["candidate_id"]
        last_index = msg.payload["last_log_index"]
        last_term = msg.payload["last_log_term"]

        my_last_term = self.log[-1].term if self.log else 0
        my_last_index = len(self.log) - 1
        log_ok = (last_term > my_last_term) or (last_term == my_last_term and last_index >= my_last_index)
        vote_granted = False
        if msg.term >= self.current_term and (self.voted_for is None or self.voted_for == candidate) and log_ok:
            vote_granted = True
            self.voted_for = candidate

        self._sign_and_send(candidate, "VOTE_REPLY", {"vote_granted": vote_granted})

    def _handle_vote_reply(self, msg: Message):
        if self.state == self.CANDIDATE and msg.term == self.current_term and msg.payload.get("vote_granted"):
            self.votes_received.add(msg.src)
            if len(self.votes_received) >= self.quorum_size:
                self.state = self.LEADER
                self.current_leader = self.node_id
                for peer in self.cluster_ids:
                    self.next_index[peer] = len(self.log)
                    self.match_index[peer] = -1
                self._broadcast_heartbeat()

    def _broadcast_heartbeat(self):
        for peer in self.cluster_ids:
            if peer != self.node_id:
                self._send_append_to_peer(peer)

    def _send_append_to_peer(self, peer: str):
        prev_index = self.next_index[peer] - 1
        prev_term = self.log[prev_index].term if 0 <= prev_index < len(self.log) else 0
        entries = [{
            "index": e.index,
            "term": e.term,
            "key": e.key,
            "value": e.value,
            "client_id": e.client_id,
            "request_id": e.request_id,
        } for e in self.log[self.next_index[peer]:]]
        self._sign_and_send(peer, "APPEND_ENTRIES", {
            "leader_id": self.node_id,
            "prev_log_index": prev_index,
            "prev_log_term": prev_term,
            "entries": entries,
            "leader_commit": self.commit_index,
        })

    def _handle_append_entries(self, msg: Message):
        leader_id = msg.payload["leader_id"]
        prev_index = msg.payload["prev_log_index"]
        prev_term = msg.payload["prev_log_term"]
        entries = msg.payload["entries"]
        leader_commit = msg.payload["leader_commit"]

        if msg.term < self.current_term:
            self._sign_and_send(leader_id, "APPEND_REPLY", {"success": False, "match_index": -1})
            return

        self.current_leader = leader_id
        self.state = self.FOLLOWER

        if prev_index >= 0:
            if prev_index >= len(self.log) or self.log[prev_index].term != prev_term:
                self._sign_and_send(leader_id, "APPEND_REPLY", {"success": False, "match_index": len(self.log) - 1})
                return

        insert_idx = prev_index + 1
        for e_dict in entries:
            entry = LogEntry(**e_dict)
            if insert_idx < len(self.log):
                if self.log[insert_idx].term != entry.term:
                    self.log = self.log[:insert_idx]
                    self.log.append(entry)
            else:
                self.log.append(entry)
            insert_idx += 1

        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)
            self._apply_entries()

        match_idx = len(self.log) - 1
        self._sign_and_send(leader_id, "APPEND_REPLY", {"success": True, "match_index": match_idx})

    def _handle_append_reply(self, msg: Message):
        if self.state != self.LEADER or msg.term != self.current_term:
            return
        success = msg.payload.get("success", False)
        match_idx = msg.payload.get("match_index", -1)
        peer = msg.src
        if success:
            self.match_index[peer] = match_idx
            self.next_index[peer] = match_idx + 1
            self._check_and_advance_commit()
        else:
            if self.next_index[peer] > 0:
                self.next_index[peer] -= 1
                self._send_append_to_peer(peer)

    def _check_and_advance_commit(self):
        for idx in range(len(self.log) - 1, self.commit_index, -1):
            if self.log[idx].term == self.current_term:
                matches = 1 + sum(1 for peer, m_idx in self.match_index.items() if peer != self.node_id and m_idx >= idx)
                if matches >= self.quorum_size:
                    self.commit_index = idx
                    self._apply_entries()
                    self._broadcast_heartbeat()
                    break

    def _apply_entries(self):
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            entry = self.log[self.last_applied]
            self.state_machine[entry.key] = entry.value
            self.client_responses[(entry.client_id, entry.request_id)] = entry.value

    def client_write(self, key: str, value: str, client_id: str, request_id: int) -> Tuple[bool, str, Optional[str]]:
        self.metrics["writes_total"] += 1
        if self.state != self.LEADER:
            return False, "NOT_LEADER", self.current_leader

        dedup_key = (client_id, request_id)
        if dedup_key in self.client_responses:
            self.metrics["replays_handled"] += 1
            return True, "COMMITTED_IDEMPOTENT", self.client_responses[dedup_key]

        new_entry = LogEntry(
            index=len(self.log),
            term=self.current_term,
            key=key,
            value=value,
            client_id=client_id,
            request_id=request_id,
        )
        self.log.append(new_entry)
        self.match_index[self.node_id] = new_entry.index

        self._broadcast_heartbeat()
        return True, "APPENDED_PENDING_QUORUM", None

    def client_read(self, key: str) -> Tuple[bool, str, Optional[str]]:
        if self.state != self.LEADER:
            return False, "NOT_LEADER", self.current_leader
        val = self.state_machine.get(key)
        return True, "SUCCESS", val
