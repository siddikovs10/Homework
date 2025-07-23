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

def is_user_registered(telegram_id):
    with sqlite3.connect("bookshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone() is not None

def create_books_table():
    with sqlite3.connect("bookshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT
            );
        """)
        conn.commit()

def get_books(limit=10, offset=0):
    with sqlite3.connect("bookshop.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, author FROM books LIMIT ? OFFSET ?", (limit, offset))
        return cursor.fetchall()

def insert_sample_books():
    sample_books = [
        ("Atomic Habits", "James Clear"),
        ("The Alchemist", "Paulo Coelho"),
        ("Sapiens", "Yuval Noah Harari"),
        ("The 7 Habits of Highly Effective People", "Stephen Covey"),
        ("To Kill a Mockingbird", "Harper Lee"),
        ("1984", "George Orwell"),
        ("Think and Grow Rich", "Napoleon Hill"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki"),
        ("Brave New World", "Aldous Huxley"),
        ("The Power of Now", "Eckhart Tolle"),
        ("The Subtle Art of Not Giving a F*ck", "Mark Manson"),
        ("Deep Work", "Cal Newport"),
        ("Start With Why", "Simon Sinek"),
        ("Man's Search for Meaning", "Viktor Frankl"),
        ("Educated", "Tara Westover"),
        ("Can’t Hurt Me", "David Goggins"),
        ("The Psychology of Money", "Morgan Housel"),
        ("Zero to One", "Peter Thiel"),
        ("Hooked", "Nir Eyal"),
        ("The Four Agreements", "Don Miguel Ruiz"),
    ]
    with sqlite3.connect("bookshop.db") as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO books (title, author) VALUES (?, ?)", sample_books)
        conn.commit()

