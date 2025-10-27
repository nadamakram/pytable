from page import Page
import os
import json

class Table:
    def __init__(self, name, columns, file_path, wal):
        self.name = name
        self.columns = columns
        self.file_path = file_path
        self.wal = wal
        self.pages = self._load_pages()

    def _load_pages(self):
        pages = []
        page = Page()
        if not os.path.exists(self.file_path):
            return [page]
        with open(self.file_path, "r") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    page.add_row(row)
                    if page.is_full():
                        pages.append(page)
                        page = Page()
        if page.rows:
            pages.append(page)
        return pages

    # Insert with WAL logging
    def insert(self, row):
        self.wal.log("insert", self.name, row)
        self._insert_no_log(row)

    # Insert without WAL (used by WAL replay)
    def _insert_no_log(self, row):
        page = self.pages[-1]
        if page.is_full():
            page = Page()
            self.pages.append(page)
        page.add_row(row)
        self._flush_page(page)

    def _flush_page(self, page):
        # For simplicity, rewrite all rows
        with open(self.file_path, "w") as f:
            for p in self.pages:
                for r in p.rows:
                    f.write(json.dumps(r) + "\n")

    def select(self, condition=lambda r: True):
        result = []
        for page in self.pages:
            for row in page.rows:
                if condition(row):
                    result.append(row)
        return result

    def delete(self, condition):
        self._delete_no_log(condition)

    def _delete_no_log(self, condition):
        for page in self.pages:
            page.delete_rows(condition)
        self._flush_page(Page())  # rewrite file


class Transaction:
    def __init__(self, db):
        self.db = db
        self.operations = []  # staged operations

    def begin(self):
        self.operations.clear()
        print("Transaction started")

    def insert(self, table_name, row):
        self.operations.append(("insert", table_name, row))

    def delete(self, table_name, condition):
        table = self.db.get_table(table_name)
        # Pass the condition directly without trying to convert it
        table.delete(condition)

    def commit(self):
        for op, table_name, data in self.operations:
            table = self.db.get_table(table_name)
            if op == "insert":
                table.insert(data)  # logs to WAL
            elif op == "delete":
                table.delete(data)
        self.operations.clear()
        print("Transaction committed")

    def rollback(self):
        self.operations.clear()
        print("Transaction rolled back")
