from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from db.database import Database


@dataclass
class Customers:
    customer_id: Optional[int] = None
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    driver_license: Optional[str] = None
    create_at: Optional[datetime] = None


class CustomersRepository:
    """Perform CRUD operations on the customers table"""

    def __init__(self):
        self.db = Database()

    def get_customers(self, search_str):
        """Retrieves customers from the database"""
        query = """
        SELECT * FROM customers WHERE full_name LIKE ? OR email LIKE ? OR phone LIKE ? OR driver_license LIKE ?
        """
        return self.db.fetch_all(
            query,
            (
                f"%{search_str}%",
                f"%{search_str}%",
                f"%{search_str}%",
                f"%{search_str}%",
            ),
        )

    def add_customer(self, customer: Customers):
        """Adds a new customer to the database"""
        query = """
        INSERT INTO customers(user_id, full_name, email, phone, address, driver_license) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                customer.user_id,
                customer.full_name,
                customer.email,
                customer.phone,
                customer.address,
                customer.driver_license,
            ),
        )

    def update_customer(self, customer: Customers):
        """Updates an existing customer in the database"""
        query = "SELECT * FROM customers WHERE customer_id = ?"
        current_customer = self.db.fetch_one(query, (customer.customer_id,))
        if not current_customer:
            raise ValueError(f"Customer with ID {customer.customer_id} not found")
        query = """
        UPDATE customers
        SET full_name = ?,
            email = ?,
            phone = ?,
            address = ?,
            driver_license = ?
        where customer_id = ?
        """
        self.db.execute(
            query,
            (
                customer.full_name or current_customer[1],
                customer.email or current_customer[2],
                customer.phone or current_customer[3],
                customer.address or current_customer[4],
                customer.driver_license or current_customer[5],
                customer.customer_id,
            ),
        )

    def delete_customer(self, id):
        """Deletes a customer from the database"""
        query = """
        DELETE FROM customers WHERE customer_id = ?
        """
        self.db.execute(query, (id,))

    def email_exits(self, email):
        """Check if the email is exist"""
        query = """
        SELECT * FROM customers WHERE email = ?
        """
        result = self.db.fetch_one(query, email)
        if result is None:
            return False
        return True

    def driver_license_exits(self, driver_license):
        """Check if the driver license is exist"""
        query = """
        SELECT * FROM customers WHERE driver_license = ?
        """
        result = self.db.fetch_one(query, (driver_license,))
        if result is None:
            return True
        return False

    def get_by_user_id(self, user_id) -> Optional[Customers]:
        query = """
        SELECT * FROM customers WHERE user_id = ?
        """
        result = self.db.fetch_one(query, (user_id,))
        if result is None:
            return None
        return Customers(*result)

    def get_by_customer_id(self, customer_id) -> Optional[Customers]:
        query = """
        SELECT * FROM customers WHERE customer_id = ?
        """
        result = self.db.fetch_one(query, (customer_id,))
        if result is None:
            return None
        return Customers(*result)
