import json

PAGE_SIZE = 4  # number of rows per page for demonstration

class Page:
    def __init__(self):
        self.rows = []

    def is_full(self):
        return len(self.rows) >= PAGE_SIZE

    def add_row(self, row):
        if self.is_full():
            raise ValueError("Page is full")
        self.rows.append(row)

    def delete_rows(self, condition):
        if isinstance(condition, dict):
            # If condition is a dictionary, create a function to match all key-value pairs
            matcher = lambda row: all(row.get(k) == v for k, v in condition.items())
            self.rows = [r for r in self.rows if not matcher(r)]
        else:
            # If condition is already a function, use it directly
            self.rows = [r for r in self.rows if not condition(r)]
