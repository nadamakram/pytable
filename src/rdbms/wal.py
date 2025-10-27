import os
import json
from datetime import datetime

class WAL:
    def __init__(self, wal_path):
        self.wal_path = wal_path
        self.entries = []
        dir_name = os.path.dirname(wal_path)
        if dir_name:  # only create if directory exists
            os.makedirs(dir_name, exist_ok=True)

    def log(self, operation, table_name, row):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),  # ISO 8601 UTC timestamp
            "op": operation,
            "table": table_name,
            "row": row
        }
        with open(self.wal_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        self.add_entry(entry)  # also add to entries list

    def add_entry(self, entry):
        self.entries.append(entry)

    def replay(self, db):
        for entry in self.entries:
            if entry["op"] == "DELETE":
                table = db.get_table(entry["table"])
                condition = entry["row"]
                table._delete_no_log(condition)
        # Clear WAL after replay
        open(self.wal_path, "w").close()
