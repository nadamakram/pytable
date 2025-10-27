# from database import Database

# # Initialize database
# db = Database("wal.log")

# # Create table
# users = db.create_table("users", ["id", "name", "age"])

# # Replay WAL (if any)
# db.replay_wal()

# # Insert data
# users.insert({"id": "1", "name": "Nada", "age": 28})
# users.insert({"id": "2", "name": "Omar", "age": 35})
# users.insert({"id": "3", "name": "Ali", "age": 42})

# # Select all users
# all_users = users.select()
# print("All users:", all_users)

# # Select users older than 30
# older = users.select(lambda r: r["age"] > 30)
# print("Older than 30:", older)

# # Delete a user
# users.delete(lambda r: r["name"] == "Nada")

# # Select after delete
# print("After delete:", users.select())

from database import Database
from table import Transaction

db = Database("wal.log")
users = db.create_table("users", ["id", "name", "age"])
tx = Transaction(db)
tx.begin()
tx.insert("users", {"id": "4", "name": "Sara", "age": 30})
tx.delete("users", {"name": "Omar"})
tx.commit()