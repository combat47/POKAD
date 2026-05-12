"""
Memory management for POKAD chatbot using SQLite.
Handles conversation history and user-specific data.
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class Memory:
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Conversation history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_text TEXT NOT NULL,
                    pokad_text TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            # User metadata table (name, preferences, etc.)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_conversation(self, user_text: str, pokad_text: str):
        """Save a single exchange to database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_text, pokad_text, timestamp) VALUES (?, ?, ?)",
                (user_text, pokad_text, timestamp)
            )
            conn.commit()

    def get_recent_history(self, limit: int = 5) -> List[Tuple[str, str]]:
        """Return last `limit` exchanges as list of (user_text, pokad_text) in chronological order."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_text, pokad_text FROM history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
        # Reverse to chronological order (oldest first)
        return list(reversed(rows))

    def clear_history(self):
        """Delete all conversation history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()
        print("🗑️ Conversation history cleared.")

    def set_user_name(self, name: str):
        """Store user's name persistently."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO user_meta (key, value) VALUES (?, ?)",
                ("user_name", name)
            )
            conn.commit()

    def get_user_name(self) -> Optional[str]:
        """Retrieve stored user name, or None if not set."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_meta WHERE key = ?", ("user_name",))
            row = cursor.fetchone()
        return row[0] if row else None

    def delete_user_name(self):
        """Remove user name from storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_meta WHERE key = ?", ("user_name",))
            conn.commit()
