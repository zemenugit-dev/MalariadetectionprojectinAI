import hashlib
from utils.database import get_connection, init_db

init_db()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

users = [
    ("Admin", "admin@gmail.com", "Zed1929@!@!", "admin"),
    ("Doctor", "doctor@gmail.com", "Zed1929@!@!", "doctor"),
    ("Patient", "patient@gmail.com", "Zed1929@!@!", "patient")
]

with get_connection() as conn:
    cursor = conn.cursor()

    for u in users:
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (u[0], u[1], hash_pw(u[2]), u[3]))

    conn.commit()

print("Users created successfully")