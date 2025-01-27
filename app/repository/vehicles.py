from dataclasses import dataclass
from typing import List, Optional, Tuple

from db.database import Database


@dataclass
class Vehicles:
    vehicle_id: Optional[int] = None
    make: str = ""
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

    def get_vehicles(
        self, search_str: str = "", status: str = ""
    ) -> List[Tuple]:
        """Retrieves vehicles from the database."""
        query = """
        SELECT vehicle_id, make, model, year, license_plate, mileage, daily_rate, description, status
        FROM vehicles
        WHERE make LIKE ?
        """
        if status:
            query += " and status = ?"
            return self.db.fetch_all(query, (f"%{search_str}%", status))
        else:
            return self.db.fetch_all(query, (f"%{search_str}%",))

    def add_vehicle(self, vehicle: Vehicles) -> None:
        """Adds a new vehicle to the database."""
        query = """
        INSERT INTO vehicles (make, model, year, license_plate, mileage, daily_rate, description, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                vehicle.make,
                vehicle.model,
                vehicle.year,
                vehicle.license_plate,
                vehicle.mileage,
                vehicle.daily_rate,
                vehicle.description,
                vehicle.status,
            ),
        )

    def update_vehicle(self, vehicle: Vehicles) -> None:
        """Updates an existing vehicle in the database."""
        query = "SELECT * FROM vehicles WHERE vehicle_id = ?"
        current_vehicle = self.db.fetch_one(query, (vehicle.vehicle_id,))

        if not current_vehicle:
            raise ValueError(f"Vehicle with ID {vehicle.vehicle_id} not found")

        # Update only the fields that were provided
        query = """
        UPDATE vehicles
        SET make = ?,
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
                vehicle.make or current_vehicle[1],
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

    def delete_vehicle(self, vehicle_id: int) -> None:
        """Deletes a vehicle from the database."""
        query = "DELETE FROM vehicles WHERE vehicle_id = ?"
        self.db.execute(query, (vehicle_id,))

    def update_status(self, vehicle_id: int, status: str) -> None:
        """Updates the status of a vehicle."""
        query = "UPDATE vehicles SET status = ? WHERE vehicle_id = ?"
        self.db.execute(query, (status, vehicle_id))

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicles]:
        """Retrieves a vehicle by ID."""
        query = """
        SELECT vehicle_id, make, model, year, license_plate, mileage, daily_rate, description, status
        FROM vehicles
        WHERE vehicle_id = ?
        """
        result = self.db.fetch_one(query, (vehicle_id,))
        if result is None:
            return None
        else:
            return Vehicles(*result)

    def update_after_return(self, vehicle_id: int, return_mileage: int) -> None:
        """Updates vehicle mileage after a rental is completed."""
        query = """
        UPDATE vehicles
        SET mileage = ?,
            status = 'available'
        WHERE vehicle_id = ?
        """
        self.db.execute(query, (return_mileage, vehicle_id))
