import re
from .base import Command

class InsertCommand(Command):
    pattern = re.compile(r"insert into (\w+)\s*values\s*\((.+)\)", re.IGNORECASE)

    def execute(self, query):
        match = self.pattern.match(query)
        if not match:
            raise ValueError("Invalid INSERT syntax.")
        name = match.group(1)
        values = [v.strip().strip("'\"") for v in match.group(2).split(",")]
        table = self.db.get_table(name)
        record = dict(zip(table.columns, values))
        table.insert(record)
        return f"✅ Inserted into '{name}': {record}"
