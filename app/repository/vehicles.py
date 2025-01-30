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
    status: str = "available"  # available or rented or maintenance


class VehiclesRepository:
    """Database operations for vehicles table"""

    def __init__(self):
        self.db = Database()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS vehicles (
                vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                license_plate TEXT UNIQUE NOT NULL,
                mileage INTEGER DEFAULT 0,
                daily_rate DECIMAL(10, 2) NOT NULL,
                description TEXT,
                status TEXT CHECK (status IN ('available', 'rented', 'maintenance')) DEFAULT 'available'
        ); 
        """
        self.db.execute(query)

        q1 = """
            INSERT OR IGNORE INTO vehicles VALUES(1,'Toyota','Camry',2022,'ABC123',15000,45,'Comfortable midsize sedan with excellent fuel economy','available'),
            (2,'Honda','CR-V',2021,'XYZ789',25000,55,'Popular compact SUV with plenty of cargo space','available'),
            (3,'Ford','Mustang',2023,'MUS555',5000,75,'Sporty muscle car with powerful engine','available'),
            (4,'BMW','3 Series',2022,'BMW444',20000,85,'Luxury sedan with premium features','available'),
            (5,'Tesla','Model 3',2023,'TSL789',10000,95,'Electric vehicle with advanced autopilot','available'),
            (6,'Mercedes','C-Class',2021,'MRC123',30000,80,'Elegant luxury sedan requiring scheduled service','available'),
            (7,'Audi','Q5',2022,'AUD456',18000,75,'Premium SUV under routine maintenance','available'),
            (8,'Volkswagen','Golf',2022,'VWG123',12000,40,'Compact hatchback with great handling','available'),
            (9,'Hyundai','Tucson',2023,'HYN789',8100,50,'Modern SUV with latest safety features','available'),
            (10,'Chevrolet','Malibu',2022,'CHV456',22000,45,'Reliable family sedan with good fuel efficiency','available')
        """
        self.db.execute(q1)

    def get_vehicles(self, search_str: str = "", status: str = "") -> List[Tuple]:
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
