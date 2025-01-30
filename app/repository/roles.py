from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from db.database import Database


@dataclass
class Roles:
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    created_at: Optional[datetime] = None


class RoleRepository:
    def __init__(self):
        self.db = Database()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db.execute(query)

        q1 = "INSERT OR IGNORE INTO roles VALUES(1,'staff','2024-12-31 09:45:50')"
        self.db.execute(q1)
        q2 = "INSERT OR IGNORE INTO roles VALUES(2,'customer','2024-12-31 09:45:50')"
        self.db.execute(q2)

    def get_role(self, role_id) -> Optional[Roles]:
        query = """
        SELECT * FROM roles WHERE role_id = ?
        """
        result = self.db.fetch_one(query, (role_id,))
        if result is None:
            return None
        return Roles(*result)
