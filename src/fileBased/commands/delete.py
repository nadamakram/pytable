import re
from .base import Command

class DeleteCommand(Command):
    pattern = re.compile(
        r"delete from (\w+) where (\w+)=['\"]?([^'\"]+)['\"]?",
        re.IGNORECASE,
    )

    def execute(self, query):
        match = self.pattern.match(query)
        if not match:
            raise ValueError("Invalid DELETE syntax.")
        name, col, val = match.groups()
        table = self.db.get_table(name)
        table.delete({col: val})
        return f"✅ Deleted from '{name}' where {col}={val}"
