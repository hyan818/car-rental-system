from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from db.database import Database


@dataclass
class Staff:
    staff_id: Optional[int] = None
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None


class StaffRepository:
    """Datbase operations for staff table"""

    def __init__(self):
        self.db = Database()

    def get_staffs(self, keyword=""):
        """Retrives staffs from the database"""
        query = """
        SELECT staff_id, user_id, full_name, email, created_at FROM staff WHERE full_name LIKE ? OR email LIKE ?
        """
        return self.db.fetch_all(query, (f"%{keyword}%", f"%{keyword}%"))

    def add_staff(self, staff: Staff):
        """Adds a new staff to the database"""
        query = """
        INSERT INTO staff(user_id, full_name, email) VALUES(?, ?, ?)
        """
        self.db.execute(
            query,
            (staff.user_id, staff.full_name, staff.email),
        )

    def update_staff(self, staff: Staff):
        """Updates an existing staff in the database"""
        query = "SELECT * FROM staff WHERE staff_id = ?"
        current_staff = self.db.fetch_one(query, (staff.staff_id,))

        if not current_staff:
            raise ValueError(f"Staff with ID {staff.staff_id} not found")

        query = """
        UPDATE staff
        SET full_name = ?,
            email = ?
        WHERE staff_id = ?
        """
        self.db.execute(
            query,
            (
                staff.full_name or current_staff[1],
                staff.email or current_staff[2],
                staff.staff_id,
            ),
        )

    def delete_staff(self, staff_id) -> None:
        """Deletes a staff from the database"""
        query = "DELETE FROM staff WHERE staff_id = ?"
        self.db.execute(query, (staff_id,))

    def get_by_user_id(self, user_id) -> Optional[Staff]:
        query = "SELECT * from STAFF WHERE user_id = ?"
        result = self.db.fetch_one(query, (user_id,))
        if result is None:
            return None
        return Staff(*result)

    def get_by_staff_id(self, staff_id) -> Optional[Staff]:
        query = "SELECT * from STAFF WHERE staff_id = ?"
        result = self.db.fetch_one(query, (staff_id,))
        if result is None:
            return None
        return Staff(*result)
