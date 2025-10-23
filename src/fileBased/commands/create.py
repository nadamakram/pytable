import re
from .base import Command

class CreateTableCommand(Command):
    pattern = re.compile(r"create table (\w+)\s*\(([^)]+)\)", re.IGNORECASE)

    def execute(self, query):
        match = self.pattern.match(query)
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax.")
        name = match.group(1)
        columns = [c.strip() for c in match.group(2).split(",")]
        self.db.create_table(name, columns)
        return f"✅ Table '{name}' created with columns {columns}"
