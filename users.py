import sqlite3
from database import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", ("John Doe", "john@example.com", "123456", "user"))

conn.commit()
conn.close()

print("User inserted successfully")