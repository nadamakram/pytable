from database import Database

# Create DB instance
db = Database()

# Create a new table
users = db.create_table("users", ["id", "name", "age"])

# Insert data
users.insert({"id": 1, "name": "Nada", "age": 28})
users.insert({"id": 2, "name": "Omar", "age": 35})

# Read data
print(users.select())
users.update(where={"id": 1}, new_values={"age": 29})

# Delete
users.delete(where={"name": "Omar"})
print(users.select())
