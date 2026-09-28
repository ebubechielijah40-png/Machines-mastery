"""Benchmark for distributed cluster quorum replication under normal, lossy, and partitioned network conditions."""
import argparse
import json
from pathlib import Path
import platform
import time

from cluster import DeterministicNetwork, RaftNode


def run_benchmark():
    result = {
        "kind": "agent distributed cluster benchmark; no learner evidence",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "scenarios": {},
    }

    # 1. Baseline: 0% loss, 3 nodes, 100 sequential writes
    net = DeterministicNetwork(latency_ticks=1, drop_rate=0.0, seed=42)
    node_ids = ["node-1", "node-2", "node-3"]
    nodes = {nid: RaftNode(nid, node_ids, net) for nid in node_ids}
    nodes["node-1"].start_election()
    net.step(ticks=4)
    assert nodes["node-1"].state == RaftNode.LEADER

    start_ticks = net.clock
    start_time = time.perf_counter_ns()
    writes_count = 100
    for i in range(writes_count):
        nodes["node-1"].client_write(f"k-{i}", f"v-{i}", "client-bench", i)
        net.step(ticks=3)
    elapsed_ns = time.perf_counter_ns() - start_time
    total_ticks = net.clock - start_ticks

    result["scenarios"]["baseline"] = {
        "writes_requested": writes_count,
        "writes_committed": nodes["node-1"].commit_index + 1,
        "simulated_ticks": total_ticks,
        "wall_time_ns": elapsed_ns,
        "network_metrics": dict(net.metrics),
    }

    # 2. Lossy Network: 10% packet drop
    net_loss = DeterministicNetwork(latency_ticks=1, drop_rate=0.10, seed=99)
    nodes_loss = {nid: RaftNode(nid, node_ids, net_loss) for nid in node_ids}
    nodes_loss["node-1"].start_election()
    # Step until leader elected
    for _ in range(10):
        net_loss.step(ticks=2)
        if nodes_loss["node-1"].state == RaftNode.LEADER:
            break

    start_ticks = net_loss.clock
    start_time = time.perf_counter_ns()
    for i in range(writes_count):
        nodes_loss["node-1"].client_write(f"k-loss-{i}", f"v-loss-{i}", "client-loss", i)
        net_loss.step(ticks=4)
    elapsed_ns = time.perf_counter_ns() - start_time

    result["scenarios"]["lossy_10_percent"] = {
        "writes_requested": writes_count,
        "writes_committed": nodes_loss["node-1"].commit_index + 1,
        "simulated_ticks": net_loss.clock - start_ticks,
        "wall_time_ns": elapsed_ns,
        "network_metrics": dict(net_loss.metrics),
    }

    # 3. Partitioned: Node-1 isolated in minority {node-1} vs {node-2, node-3}
    net_part = DeterministicNetwork(latency_ticks=1, drop_rate=0.0, seed=77)
    nodes_part = {nid: RaftNode(nid, node_ids, net_part) for nid in node_ids}
    nodes_part["node-1"].start_election()
    net_part.step(ticks=4)

    # Ingest 20 writes before partition
    for i in range(20):
        nodes_part["node-1"].client_write(f"k-p-{i}", f"v-p-{i}", "client-p", i)
        net_part.step(ticks=3)
    committed_pre = nodes_part["node-1"].commit_index + 1

    # Inject partition: isolate node-1
    net_part.partition({"node-1"}, {"node-2", "node-3"})
    # Attempt 20 writes to isolated node-1 (minority)
    minority_failed = 0
    for i in range(20, 40):
        nodes_part["node-1"].client_write(f"k-p-{i}", f"v-p-{i}", "client-p", i)
        net_part.step(ticks=3)
        if nodes_part["node-1"].commit_index + 1 == committed_pre:
            minority_failed += 1

    # Elect leader in majority {node-2, node-3}
    nodes_part["node-2"].start_election()
    net_part.step(ticks=6)
    majority_committed = 0
    if nodes_part["node-2"].state == RaftNode.LEADER:
        for i in range(40, 60):
            nodes_part["node-2"].client_write(f"k-p-{i}", f"v-p-{i}", "client-p", i)
            net_part.step(ticks=6)
        majority_committed = nodes_part["node-2"].commit_index + 1

    result["scenarios"]["partition"] = {
        "committed_pre_partition": committed_pre,
        "minority_writes_blocked_from_commit": minority_failed,
        "majority_writes_committed": majority_committed,
        "network_metrics": dict(net_part.metrics),
    }

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Output path for benchmark JSON.')
    args = parser.parse_args()

    bench_data = run_benchmark()
    with args.output.open('x') as f:
        json.dump(bench_data, f, indent=2)
        f.write('\n')
    print(f"PASS: recorded distributed cluster benchmark to {args.output}")
