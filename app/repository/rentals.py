from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from db.database import Database


@dataclass
class Rentals:
    rental_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    customer_id: Optional[int] = None
    staff_id: Optional[int] = None
    start_date: Optional[datetime] = None
    expected_return_date: Optional[datetime] = None
    actual_return_date: Optional[datetime] = None
    initial_mileage: int = 0
    return_mileage: int = 0
    rental_status: str = "apply"
    total_cost: Optional[float] = None
    created_at: Optional[datetime] = None


class RentalsRepository:
    """Database operations for rentals table"""

    def __init__(self):
        self.db = Database()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS rentals (
            rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            customer_id INTEGER,
            staff_id INTEGER,
            start_date DATETIME NOT NULL,
            expected_return_date DATETIME NOT NULL,
            actual_return_date DATETIME,
            initial_mileage INTEGER,
            return_mileage INTEGER,
            rental_status TEXT CHECK (
                rental_status IN (
                    'apply',
                    'active',
                    'reject',
                    'completed',
                    'cancelled'
                )
            ) DEFAULT 'apply',
            total_cost DECIMAL(10, 2),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
        );
        """
        self.db.execute(query)

    def get_rental_details(
        self, status: str = "", customer_id: int = 0
    ) -> List[Tuple]:
        """Retrieves rentals from the database."""
        query = """
        SELECT r.rental_id, v.make, v.model, c.full_name,
               r.start_date, r.expected_return_date, r.actual_return_date,
               r.initial_mileage, r.return_mileage, r.rental_status, r.total_cost
        FROM rentals r
        JOIN vehicles v ON r.vehicle_id = v.vehicle_id
        JOIN customers c ON r.customer_id = c.customer_id
        WHERE r.rental_status LIKE ?
        """
        if customer_id != 0:
            query += " AND c.customer_id = ? ORDER BY r.rental_id DESC"
            return self.db.fetch_all(
                query,
                (
                    f"%{status}%",
                    customer_id,
                ),
            )
        else:
            query += " ORDER BY r.rental_id DESC "
            return self.db.fetch_all(query, (f"%{status}%",))

    def add_rental(self, rental: Rentals) -> None:
        """Creates a new rental record."""
        query = """
        INSERT INTO rentals (
            vehicle_id, customer_id, staff_id, start_date,
            expected_return_date, initial_mileage, rental_status, total_cost
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                rental.vehicle_id,
                rental.customer_id,
                rental.staff_id,
                rental.start_date,
                rental.expected_return_date,
                rental.initial_mileage,
                rental.rental_status,
                rental.total_cost,
            ),
        )

    def complete_rental(
        self, rental_id: int, return_mileage: int, actual_return_date: datetime
    ) -> None:
        """Completes a rental by updating return information."""
        query = """
        UPDATE rentals
        SET return_mileage = ?,
            actual_return_date = ?,
            rental_status = 'completed'
        WHERE rental_id = ?
        """
        self.db.execute(query, (return_mileage, actual_return_date, rental_id))

    def update_status(self, rental_id: int, status: str) -> None:
        """Update rental status."""
        query = """
        UPDATE rentals
        SET rental_status = ?
        WHERE rental_id = ?
        """
        self.db.execute(
            query,
            (
                status,
                rental_id,
            ),
        )

    def get_by_id(self, rental_id: int) -> Optional[Rentals]:
        """Retrieves a rental record by ID."""
        query = """
        SELECT * FROM rentals WHERE rental_id = ?
        """
        result = self.db.fetch_one(query, (rental_id,))

        if result is None:
            return None
        else:
            return Rentals(*result)
