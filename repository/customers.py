from dataclasses import dataclass
from typing import Optional

from db.database import Database


@dataclass
class Customers:
    customer_id: Optional[int] = None
    full_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    driver_license: str = ""
    create_at: str = ""


class CustomersRepository:
    """
    Perform CRUD operations on the customers table
    """

    def __init__(self):
        self.db = Database()

    def get(self, search_str):
        """
        Retrieves customers from the database
        """

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

    def add(self, customer: Customers):
        """
        Adds a new customer to the database
        """

        query = """
        INSERT INTO customers(full_name, email, phone, address, driver_license) VALUES(?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                customer.full_name,
                customer.email,
                customer.phone,
                customer.address,
                customer.driver_license,
            ),
        )

    def update(self, customer: Customers):
        """
        Updates an existing customer in the database
        """

        query = "SELECT * FROM customers WHERE customer_id = ?"
        current_customer = self.db.fetch_one(query, (customer.customer_id,))
        if not current_customer:
            raise ValueError(
                f"Customer with ID {customer.customer_id} not found"
            )
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

    def delete(self, id):
        """
        Deletes a customer from the database
        """

        query = """
        DELETE FROM customers WHERE customer_id = ?
        """
        self.db.execute(query, (id,))
