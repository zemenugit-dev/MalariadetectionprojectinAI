import sqlite3
import os

# ======================================
# ABSOLUTE DATABASE PATH
# ======================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "malaria.db")

# Create database folder automatically if not exists
os.makedirs(DB_DIR, exist_ok=True)

print("Using Database:", DB_PATH)


# ======================================
# DATABASE CONNECTION (SAFE FOR FLASK)
# ======================================

def get_connection():
    """
    Create and return a fresh SQLite connection.
    Prevents locking issues in Flask.
    """

    conn = sqlite3.connect(DB_PATH, timeout=30)

    # Stability improvements
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")

    return conn


# ======================================
# INIT DATABASE (CREATE TABLES)
# ======================================
def init_db():
    """
    Create users and predictions tables if not exist
    """

    print("Initializing database...")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # USERS TABLE
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'patient',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # PREDICTIONS TABLE
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                image TEXT NOT NULL,
                result TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE SET NULL
            )
            """)

            # DEFAULT USERS SEED
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]

            if count == 0:
                print("Creating default users...")

                import hashlib
                def hash_password(password):
                    return hashlib.sha256(password.encode()).hexdigest()

                cursor.execute("""
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                """, ("Admin", "admin@gmail.com", hash_password("admin123"), "admin"))

                cursor.execute("""
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                """, ("Doctor", "doctor@gmail.com", hash_password("doctor123"), "doctor"))

                cursor.execute("""
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                """, ("Patient", "patient@gmail.com", hash_password("patient123"), "patient"))

                print("Default users created successfully!")

            conn.commit()

        print("Tables created successfully!")

    except Exception as e:
        print("Database Error:", e)

# ======================================
# GET USER BY EMAIL (LOGIN SUPPORT)
# ======================================

def get_user_by_email(email):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT * FROM users WHERE email = ?
            """, (email,))

            user = cursor.fetchone()
            return user

    except Exception as e:
        print("Fetch User Error:", e)
        return None


# ======================================
# GET USER HISTORY (OPTIONAL FEATURE)
# ======================================

def get_user_predictions(user_id):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT * FROM predictions
            WHERE user_id = ?
            ORDER BY created_at DESC
            """, (user_id,))

            return cursor.fetchall()

    except Exception as e:
        print("History Fetch Error:", e)
        return []
    # ======================================
# SAVE PREDICTION
# ======================================

# ======================================
# SAVE PREDICTION
# ======================================

def save_prediction(image, result, confidence, user_id=None):

    try:
        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO predictions
            (user_id, image, result, confidence)
            VALUES (?, ?, ?, ?)
            """, (
                user_id,
                image,
                result,
                confidence
            ))

            conn.commit()

            print("Prediction saved successfully!")

    except Exception as e:
        print("Database Save Error:", e)