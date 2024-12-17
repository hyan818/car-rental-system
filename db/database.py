import sqlite3
from contextlib import contextmanager
from typing import List, Optional, Tuple


class Database:
    """
    A class to handle SQLite database operations.
    """

    def __init__(self, db_name: str = "crs.db"):
        """
        Initializes the database connection.
        """
        self.db_name = f"./db/{db_name}"

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures connections are properly closed after use.
        """
        conn = sqlite3.connect(self.db_name)
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

    def execute(self, query: str, params: tuple = ()) -> None:
        """
        Executes a query and commits changes.

        Args:
            query: SQL query to execute
            params: Parameters for the query
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            raise

    def fetch_all(self, query: str, params: tuple = ()) -> List[Tuple]:
        """
        Executes a query and returns all results.

        Args:
            query: SQL query to execute
            params: Parameters for the query

        Returns:
            List of tuples containing the query results
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            return []

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Tuple]:
        """
        Executes a query and returns one result.

        Args:
            query: SQL query to execute
            params: Parameters for the query

        Returns:
            Tuple containing the query result or None if not found
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            return None

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """
        Executes a query multiple times with different parameters.

        Args:
            query: SQL query to execute
            params_list: List of parameter tuples
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, params_list)
        except sqlite3.Error as e:
            print(f"[red]Database error: {e}[/red]")
            raise
