from table import Table
from wal import WAL
class Database:
    def __init__(self, wal_path="wal.log"):
        self.tables = {}
        self.wal = WAL(wal_path)

    def create_table(self, name, columns, file_path=None):
        if not file_path:
            file_path = f"{name}.tbl"
        table = Table(name, columns, file_path, self.wal)
        self.tables[name] = table
        return table

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist")
        return self.tables[name]

    def replay_wal(self):
        self.wal.replay(self)
