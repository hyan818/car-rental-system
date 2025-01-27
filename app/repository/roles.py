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

    def get_role(self, role_id) -> Optional[Roles]:
        query = """
        SELECT * FROM roles WHERE role_id = ?
        """
        result = self.db.fetch_one(query, (role_id,))
        if result is None:
            return None
        return Roles(*result)
