import sqlite3
import os
from datetime import datetime, date
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "journal.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                content     TEXT NOT NULL,
                mood        TEXT,
                ai_analysis TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)


# ── Users ──────────────────────────────────────────────────────────────────

def upsert_user(user_id: int, username: Optional[str], first_name: Optional[str]):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username   = excluded.username,
                first_name = excluded.first_name
        """, (user_id, username, first_name))


# ── Entries ────────────────────────────────────────────────────────────────

def save_entry(user_id: int, content: str, mood: Optional[str] = None,
               ai_analysis: Optional[str] = None) -> int:
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO entries (user_id, content, mood, ai_analysis)
            VALUES (?, ?, ?, ?)
        """, (user_id, content, mood, ai_analysis))
        return cur.lastrowid


def update_entry_analysis(entry_id: int, mood: str, ai_analysis: str):
    with get_connection() as conn:
        conn.execute("""
            UPDATE entries SET mood = ?, ai_analysis = ? WHERE id = ?
        """, (mood, ai_analysis, entry_id))


def get_entries(user_id: int, limit: int = 10) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM entries
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit)).fetchall()


def get_entries_by_date(user_id: int, target_date: date) -> list[sqlite3.Row]:
    date_str = target_date.isoformat()
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM entries
            WHERE user_id = ?
              AND DATE(created_at) = ?
            ORDER BY created_at DESC
        """, (user_id, date_str)).fetchall()


def get_entry_count(user_id: int) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM entries WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["cnt"] if row else 0