import sqlite3
from config import DB_NAME

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                full_name TEXT,
                phone_number TEXT
            );
        """)
        conn.commit()

def add_user(telegram_id, full_name, phone_number):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (telegram_id, full_name, phone_number)
            VALUES (?, ?, ?)
        """, (telegram_id, full_name, phone_number))
        conn.commit()


