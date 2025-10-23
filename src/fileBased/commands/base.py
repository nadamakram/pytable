class Command:
    def __init__(self, db):
        self.db = db

    def execute(self, query):
        raise NotImplementedError("Each command must implement execute()")
