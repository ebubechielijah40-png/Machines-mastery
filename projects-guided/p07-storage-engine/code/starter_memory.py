"""Working volatile baseline. Compare its restart behavior with the WAL.

Milestone A starts here; this intentionally makes no persistence promise.
"""
class MemoryStore:
    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def snapshot(self):
        return self.data.copy()


if __name__ == "__main__":
    first = MemoryStore()
    first.put("sample", "42")
    restarted = MemoryStore()
    print("before restart:", first.snapshot())
    print("after restart:", restarted.snapshot())
