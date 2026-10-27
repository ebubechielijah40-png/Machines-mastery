"""Deterministic byte-cut fault model; never claims physical power-loss testing."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import tempfile
import time
from unittest import mock

from wal_store import FILE_MAGIC, CorruptionError, WalStore, encode_transaction, recover


def run():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "experiment.wal"
        first = encode_transaction(1, [("put", "a", "10"), ("put", "b", "20")])
        second = encode_transaction(2, [("put", "a", "9"), ("put", "b", "21")])
        outcomes = []
        for cut in range(len(second) + 1):
            path.write_bytes(FILE_MAGIC + first + second[:cut])
            report = recover(path)
            outcomes.append({"cut_bytes": cut, "transactions": report.transactions,
                             "data": report.data, "tail_reason": report.tail_reason})
        assert all(row["data"] == {"a": "10", "b": "20"}
                   for row in outcomes[:-1])
        assert outcomes[-1]["data"] == {"a": "9", "b": "21"}
        damaged = bytearray(FILE_MAGIC + first + second)
        damaged[len(FILE_MAGIC) + len(first) + 18] ^= 1
        path.write_bytes(damaged)
        try:
            recover(path)
        except CorruptionError as error:
            corruption = str(error)
        else:
            raise AssertionError("corruption was not detected")
        path.unlink()
        with WalStore(path) as store:
            try:
                with mock.patch("wal_store.os.fsync", side_effect=OSError("injected")):
                    store.commit([("put", "uncertain", "present")])
            except OSError:
                acknowledged = False
            else:
                raise AssertionError("injection did not trigger")
            live_snapshot = store.snapshot()
        uncertain = {"acknowledged": acknowledged, "live_snapshot": live_snapshot,
                     "recovered_snapshot": recover(path).data}
        scaling = []
        for n in (100, 1000, 10000):
            path.unlink()
            # Build fixture bytes without timing or fsync. Time replay only.
            with path.open("wb") as stream:
                stream.write(FILE_MAGIC)
                for tx in range(1, n + 1):
                    stream.write(encode_transaction(tx, [("put", str(tx % 100), str(tx))]))
            times = []
            for _ in range(5):
                start = time.perf_counter_ns()
                recovered = recover(path)
                times.append(time.perf_counter_ns() - start)
            assert recovered.transactions == n
            scaling.append({"transactions": n, "file_bytes": path.stat().st_size,
                            "retained_keys": len(recovered.data), "replay_ns": times})
    return {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(), "platform": platform.platform(),
            "fault_model": "explicit proper byte prefixes; no physical power-loss emulation",
            "second_frame_bytes": len(second), "cut_outcomes": outcomes,
            "corruption_observation": corruption, "failed_sync_observation": uncertain,
            "replay_scaling": scaling}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    else:
        print(output, end="")
