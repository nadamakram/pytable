import json, os

class Table:
    def __init__(self, name, columns, schema_path, data_folder="data"):
        self.name = name
        self.columns = columns
        # Derive the base path relative to the schema_path's directory
        base_path = os.path.join(os.path.dirname(schema_path), data_folder)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        self.file_path = os.path.join(base_path, f"{name}.json")
        
        if not os.path.isfile(self.file_path):
            # Create an empty file
            open(self.file_path, 'w').close()
        

    def insert(self, row):
        """Insert a new row"""
        for col in self.columns:
            if col not in row:
                raise ValueError(f"Missing column '{col}' in insert.")
        with open(self.file_path, "a") as f:
            f.write(json.dumps(row) + "\n")


    def select(self, limit=None):
        """Select rows with optional limit"""
        results = []
        with open(self.file_path, "r") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line))
                    if limit and len(results) >= limit:
                        break
        return results

    def update(self, where: dict, new_values: dict):
        """Update rows that match `where` with `new_values`."""
        updated_count = 0
        rows = []

        with open(self.file_path, "r") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    if all(row.get(k) == v for k, v in where.items()):
                        row.update(new_values)
                        updated_count += 1
                    rows.append(row)

        # Rewrite file
        with open(self.file_path, "w") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")

        return updated_count

    def delete(self, where: dict):
        """Delete rows that match `where`."""
        remaining = []
        deleted_count = 0

        with open(self.file_path, "r") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    if all(row.get(k) == v for k, v in where.items()):
                        deleted_count += 1
                    else:
                        remaining.append(row)

        # Rewrite file without deleted rows
        with open(self.file_path, "w") as f:
            for row in remaining:
                f.write(json.dumps(row) + "\n")

        return deleted_count