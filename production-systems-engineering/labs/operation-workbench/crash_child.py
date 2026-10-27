"""POSIX process-crash fixture; parent kills only this directly spawned child."""
import sys
import time
from operations import OperationStore

if len(sys.argv) != 3 or sys.argv[2] not in {'before_commit', 'after_commit'}:
    raise SystemExit('database path and controlled phase required')
store = OperationStore(sys.argv[1])
phase = sys.argv[2]
def hook(current):
    if current == phase:
        print(current, flush=True)
        while True:
            time.sleep(1)
store.apply('crash-operation', 7, hook=hook)
