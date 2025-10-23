import re
from .base import Command

class UpdateCommand(Command):
    pattern = re.compile(
        r"update (\w+) set (\w+)=['\"]?([^'\"]+)['\"]? where (\w+)=['\"]?([^'\"]+)['\"]?",
        re.IGNORECASE,
    )

    def execute(self, query):
        match = self.pattern.match(query)
        if not match:
            raise ValueError("Invalid UPDATE syntax.")
        name, col, val, where_col, where_val = match.groups()
        table = self.db.get_table(name)
        table.update(where_col, where_val, {col: val})
        return f"✅ Updated '{name}' where {where_col}={where_val}"
