from dataclasses import dataclass
from typing import Optional

from db.database import Database

global current_staff


@dataclass
class Staff:
    staff_id: Optional[int] = None
    username: str = ""
    password: str = ""
    full_name: str = ""
    email: str = ""
    created_at: str = ""
    last_login: str = ""


class StaffRepository:
    """Datbase operations for staff table"""

    def __init__(self):
        self.db = Database()

    def get_by_username(self, username) -> Staff | None:
        """Get staff by username"""

        query = "SELECT * FROM staff WHERE username = ?"
        result = self.db.fetch_one(query, (username,))
        if result is None:
            return None
        staff = Staff()
        staff.staff_id = result[0]
        staff.username = result[1]
        staff.password = result[2]
        staff.full_name = result[3]
        staff.email = result[4]
        staff.created_at = result[5]
        staff.last_login = result[6]
        return staff

    def update_password(self, staff: Staff):
        """Update staff password"""
        query = "UPDATE staff SET password = ? WHERE staff_id = ?"
        self.db.execute(query, (staff.password, staff.staff_id))

    def get(self, keyword=""):
        """Retrives staffs from the database"""
        query = """
        SELECT staff_id, username, full_name, email, last_login FROM staff WHERE username LIKE ? OR full_name LIKE ? OR email LIKE ?
        """
        return self.db.fetch_all(
            query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        )

    def add(self, staff: Staff):
        """Adds a new staff to the database"""
        query = """
        INSERT INTO staff(username, password, full_name, email) VALUES(?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (staff.username, staff.password, staff.full_name, staff.email),
        )

    def update(self, staff: Staff):
        """Updates an existing staff in the database"""
        query = "SELECT * FROM staff WHERE staff_id = ?"
        current_staff = self.db.fetch_one(query, (staff.staff_id,))

        if not current_staff:
            raise ValueError(f"Staff with ID {staff.staff_id} not found")

        query = """
        UPDATE staff
        SET username = ?,
            full_name = ?,
            email = ?
        WHERE staff_id = ?
        """
        self.db.execute(
            query,
            (
                staff.username or current_staff[1],
                staff.full_name or current_staff[2],
                staff.email or current_staff[3],
                staff.staff_id,
            ),
        )

    def delete(self, staff_id):
        """Deletes a staff from the database"""
        query = "DELETE FROM staff WHERE staff_id = ?"
        self.db.execute(query, (staff_id,))
