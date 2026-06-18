import sqlite3

DB_NAME = "users.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (username, email, password_hash)
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def save_chat(user_id, question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats (user_id, question, answer)
        VALUES (?, ?, ?)
        """,
        (user_id, question, answer)
    )

    conn.commit()
    conn.close()


def get_chat_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT question, answer
        FROM chats
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (user_id,)
    )

    chats = cursor.fetchall()
    conn.close()

    return chats