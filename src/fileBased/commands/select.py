import re
from .base import Command

class SelectCommand(Command):
    pattern = re.compile(r"select \* from (\w+)(?: limit (\d+))?", re.IGNORECASE)

    def execute(self, query):
        match = self.pattern.match(query)
        if not match:
            raise ValueError("Invalid SELECT syntax.")
        name = match.group(1)
        limit = int(match.group(2)) if match.group(2) else None
        table = self.db.get_table(name)
        rows = table.select(limit)
        return "\n".join(str(r) for r in rows)
