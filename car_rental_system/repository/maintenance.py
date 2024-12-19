from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from db.database import Database


@dataclass
class Maintenance:
    maintenance_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    staff_id: Optional[int] = None
    description: str = ""
    maintenance_date: Optional[datetime] = None
    cost: Optional[float] = None
    status: str = "scheduled"
    completion_date: Optional[datetime] = None
    notes: str = ""


class MaintenanceRepository:
    """Database operations for maintenance table"""

    def __init__(self):
        self.db = Database()

    def get(self, status: str = "") -> List[Tuple]:
        """Retrieves maintenance records from the database."""
        query = """
        SELECT m.maintenance_id, v.brand, v.model, v.license_plate,
               m.description, m.maintenance_date, m.cost,
               m.status, m.completion_date, m.notes
        FROM maintenance m
        JOIN vehicles v ON m.vehicle_id = v.vehicle_id
        WHERE m.status LIKE ?
        ORDER BY m.maintenance_date DESC
        """
        return self.db.fetch_all(query, (f"%{status}%",))

    def add(self, maintenance: Maintenance) -> None:
        """Creates a new maintenance record."""
        query = """
        INSERT INTO maintenance (
            vehicle_id, staff_id, description, maintenance_date,
            cost, status, completion_date, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                maintenance.vehicle_id,
                maintenance.staff_id,
                maintenance.description,
                maintenance.maintenance_date,
                maintenance.cost,
                maintenance.status,
                maintenance.completion_date,
                maintenance.notes,
            ),
        )

    def update_status(
        self,
        maintenance_id: int,
        status: str,
        completion_date: Optional[datetime] = None,
    ) -> None:
        """Updates the status of a maintenance record."""
        query = """
        UPDATE maintenance
        SET status = ?,
            completion_date = ?
        WHERE maintenance_id = ?
        """
        self.db.execute(query, (status, completion_date, maintenance_id))

    def get_by_id(self, maintenance_id: int) -> Optional[Maintenance]:
        """Retrieves a maintenance record by ID."""
        query = "SELECT * FROM maintenance WHERE maintenance_id = ?"
        result = self.db.fetch_one(query, (maintenance_id,))

        if result is None:
            return None
        return Maintenance(*result)

    def delete(self, maintenance_id: int) -> None:
        """Deletes a maintenance record."""
        query = "DELETE FROM maintenance WHERE maintenance_id = ?"
        self.db.execute(query, (maintenance_id,))
