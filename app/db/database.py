import sqlite3
from contextlib import contextmanager
from typing import List, Optional, Tuple

from rich import print


class Database:
    """A class to handle SQLite database operations."""

    def __init__(self, db_path: str = "crs.db"):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures connections are properly closed after use.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.commit()
            conn.close()

    @contextmanager
    def get_cursor(self):
        """
        Context manager for database cursors.
        Ensures proper connection handling and cleanup.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Executes a query and commits changes."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            raise

    def fetch_all(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Executes a query and returns all results."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            return []

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Tuple]:
        """Executes a query and returns one result."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            return None

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Executes a query multiple times with different parameters."""
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, params_list)
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            raise
