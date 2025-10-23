import os
import json
from table import Table

class Database:
    def __init__(self, schema_path="metadata/schema.json"):
        self.schema_path = schema_path
        os.makedirs(os.path.dirname(schema_path), exist_ok=True)
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                self.schema = json.load(f)
        else:
            self.schema = {}

    def create_schema(self):
        """Create or reset the schema file."""
        self.schema = {}
        self._save_schema()
    
    def create_table(self, name, columns):
        self.schema[name] = {"columns": columns}
        self._save_schema()
        # Pass the schema_path so that the Table will create its data file
        return Table(name, columns, self.schema_path)

    def get_table(self, name):
        if name not in self.schema:
            raise ValueError(f"Table '{name}' not found.")
        cols = self.schema[name]['columns']
        return Table(name, cols, self.schema_path)

    def _save_schema(self):
        with open(self.schema_path, 'w') as f:
            json.dump(self.schema, f, indent=4)
