from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import bcrypt
from db.database import Database


@dataclass
class Users:
    user_id: Optional[int] = None
    username: Optional[str] = None
    password: str = ""
    role_id: Optional[int] = None
    last_login: Optional[datetime] = None


class UsersRepository:
    def __init__(self):
        self.db = Database()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER,
            last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES roles (role_id)
        );
        """
        self.db.execute(query)

        q = "INSERT OR IGNORE INTO users VALUES(1,'admin','$2b$12$LWdTnqauV6Qxv2wcKl306ehLM0zUCKlvFKJiY5NF7qLySZD6qBxQS',1,'2025-01-27 17:27:37.235554')"
        self.db.execute(q)

    def get_by_username(self, username) -> Optional[Users]:
        query = "SELECT * FROM users WHERE username = ?"
        result = self.db.fetch_one(query, (username,))
        if result is None:
            return None
        return Users(*result)

    def username_exists(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        result = self.db.fetch_one(query, (username,))
        if result is None:
            return True
        return False

    def add_user(self, users: Users):
        password = bcrypt.hashpw(users.password.encode("utf-8"), bcrypt.gensalt())
        query = "INSERT INTO users(username, password, role_id) VALUES(?, ?, ?)"
        cursor = self.db.execute(
            query, (users.username, password.decode("utf-8"), users.role_id)
        )
        return cursor.lastrowid

    def update_last_login(self, user_id):
        query = "UPDATE users SET last_login = ? WHERE user_id = ?"
        self.db.execute(query, (datetime.now(), user_id))

    def get_by_user_id(self, user_id) -> Optional[Users]:
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self.db.fetch_one(query, (user_id,))
        if result is None:
            return None
        return Users(*result)

    def update_password(self, user_id, new_password):
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        self.db.execute(query, (new_password, user_id))

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = ?"
        self.db.execute(query, (user_id,))
