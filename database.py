import sqlite3
from functools import wraps


class DatabaseManager:
    def __init__(self, db_name) -> None:
        self.db_name = db_name

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        return conn, conn.cursor()

    def close_connection(self, conn, cur):
        cur.close()
        conn.close()


def db_connector(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = DatabaseManager("crs.db")
        conn, cur = db.get_connection()
        try:
            result = func(*args, cur=cur, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            db.close_connection(conn, cur)

    return wrapper
