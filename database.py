import sqlite3
import os

BASE_DIR = "Logs"
os.makedirs(BASE_DIR, exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "diary.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    UNIQUE(section, subject)
)
""")

conn.commit()


def diary_sections():
    cursor.execute("SELECT name FROM sections")
    return [row[0] for row in cursor.fetchall()]


def folder_exists(section):
    cursor.execute("INSERT OR IGNORE INTO sections (name) VALUES (?)", (section,))
    conn.commit()


def logs_input(section):
    cursor.execute("SELECT subject FROM entries WHERE section = ?", (section,))
    return [row[0] for row in cursor.fetchall()]


def write_entry(section, subject, body):
    cursor.execute("""
        INSERT INTO entries (section, subject, body)
        VALUES (?, ?, ?)
        ON CONFLICT(section, subject)
        DO UPDATE SET body = excluded.body
    """, (section, subject, body))
    conn.commit()


def read_entry(section, subject):
    cursor.execute("SELECT body FROM entries WHERE section=? AND subject=?", (section, subject))
    result = cursor.fetchone()
    return result[0] if result else ""