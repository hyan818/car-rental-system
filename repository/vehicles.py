from dataclasses import dataclass
from typing import List, Optional, Tuple

from db.database import Database


@dataclass
class Vehicles:
    vehicle_id: Optional[int] = None
    brand: str = ""
    model: str = ""
    year: Optional[int] = None
    license_plate: str = ""
    mileage: Optional[int] = None
    daily_rate: Optional[float] = None
    description: str = ""
    status: str = "available"  # available or rented or maintance


class VehiclesRepository:
    """Database operations for vehicles table"""

    def __init__(self):
        self.db = Database()

    def get(self, search_str: str = "") -> List[Tuple]:
        """Retrieves vehicles from the database."""
        query = """
        SELECT vehicle_id, brand, model, year, license_plate, mileage, daily_rate, description, status
        FROM vehicles
        WHERE brand LIKE ?
        """
        return self.db.fetch_all(query, (f"%{search_str}%",))

    def add(self, vehicle: Vehicles) -> None:
        """Adds a new vehicle to the database."""
        query = """
        INSERT INTO vehicles (brand, model, year, license_plate, mileage, daily_rate, description, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                vehicle.brand,
                vehicle.model,
                vehicle.year,
                vehicle.license_plate,
                vehicle.mileage,
                vehicle.daily_rate,
                vehicle.description,
                vehicle.status,
            ),
        )

    def update(self, vehicle: Vehicles) -> None:
        """Updates an existing vehicle in the database."""
        query = "SELECT * FROM vehicles WHERE vehicle_id = ?"
        current_vehicle = self.db.fetch_one(query, (vehicle.vehicle_id,))

        if not current_vehicle:
            raise ValueError(f"Vehicle with ID {vehicle.vehicle_id} not found")

        # Update only the fields that were provided
        query = """
        UPDATE vehicles
        SET brand = ?,
            model = ?,
            year = ?,
            license_plate = ?,
            mileage = ?,
            daily_rate = ?,
            description = ?,
            status = ?
        WHERE vehicle_id = ?
        """

        self.db.execute(
            query,
            (
                vehicle.brand or current_vehicle[1],
                vehicle.model or current_vehicle[2],
                vehicle.year or current_vehicle[3],
                vehicle.license_plate or current_vehicle[4],
                vehicle.mileage or current_vehicle[5],
                vehicle.daily_rate or current_vehicle[6],
                vehicle.description or current_vehicle[7],
                vehicle.status or current_vehicle[8],
                vehicle.vehicle_id,
            ),
        )

    def delete(self, vehicle_id: int) -> None:
        """Deletes a vehicle from the database."""
        query = "DELETE FROM vehicles WHERE vehicle_id = ?"
        self.db.execute(query, (vehicle_id,))

    def update_status(self, vehicle_id: int, status: str) -> None:
        """Updates the status of a vehicle."""
        query = "UPDATE vehicles SET status = ? WHERE vehicle_id = ?"
        self.db.execute(query, (status, vehicle_id))
