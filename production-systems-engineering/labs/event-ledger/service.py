"""Local SQLite ledger with bounded single-writer cache; not a deployed service."""
from collections import OrderedDict
import sqlite3


class Ledger:
    def __init__(self, path, capacity=0, indexed=False):
        if type(capacity) is not int or capacity < 0:
            raise ValueError("nonnegative cache capacity required")
        self.db = sqlite3.connect(path, timeout=0.1)
        self.db.execute("CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY, account INTEGER NOT NULL, amount INTEGER NOT NULL)")
        self.db.commit()
        self.capacity = capacity
        self.cache = OrderedDict()
        self.metrics = {"reads": 0, "hits": 0, "writes": 0, "duplicates": 0, "errors": 0}
        if indexed:
            self.add_index()

    def add_index(self):
        self.db.execute("CREATE INDEX IF NOT EXISTS account_idx ON events(account)")
        self.db.commit()

    def ingest(self, event_id, account, amount, fail=False):
        if any(type(v) is not int for v in (event_id, account, amount)) or not (0 <= event_id < 2**63 and 0 <= account < 1000 and -1000000 <= amount <= 1000000):
            self.metrics["errors"] += 1
            raise ValueError("invalid synthetic event")
        try:
            with self.db:
                existing = self.db.execute("SELECT account,amount FROM events WHERE event_id=?", (event_id,)).fetchone()
                if existing is not None:
                    if existing != (account, amount):
                        raise ValueError("event identity conflicts with stored payload")
                    self.metrics["duplicates"] += 1
                    return False
                self.db.execute("INSERT INTO events VALUES (?,?,?)", (event_id,account,amount))
                if fail:
                    raise RuntimeError("injected failure before commit")
        except (ValueError, RuntimeError, sqlite3.Error):
            self.metrics["errors"] += 1
            raise
        self.cache.pop(account, None)
        self.metrics["writes"] += 1
        return True

    def total(self, account):
        if type(account) is not int or not 0 <= account < 1000:
            self.metrics["errors"] += 1
            raise ValueError("invalid account")
        self.metrics["reads"] += 1
        if account in self.cache:
            self.metrics["hits"] += 1
            self.cache.move_to_end(account)
            return self.cache[account]
        value = self.db.execute("SELECT COALESCE(SUM(amount),0) FROM events WHERE account=?", (account,)).fetchone()[0]
        if self.capacity:
            self.cache[account] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
        return value

    def close(self):
        self.db.close()
