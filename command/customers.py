from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from repository.customers import Customers, CustomersRepository
from validation import (
    get_validated_input,
    validate_digit,
    validate_email,
    validate_phone,
)


class CustomerCommand:
    HELP_MESSAGE = """
    Available Commands:
        /customer list    List customers' information
        /customer search  Search customers' information by name or phone number
        /customer add     Add a new customer
        /customer update  Update a customer information
        /customer del     Delete a customer
    """

    def __init__(self) -> None:
        self.repo = CustomersRepository()
        self.commands = {
            "list": self.list_customers,
            "search": self.search_customer,
            "add": self.add_customer,
            "update": self.update_customer,
            "del": self.delete_customer,
        }

    def handle_command(self, command):
        parts = command.split()
        if len(parts) < 2:
            print(self.HELP_MESSAGE)
            return

        subcommand = parts[1]

        if subcommand in self.commands:
            return self.commands[subcommand]()
        else:
            return f"unknown subcommand: {subcommand}"

    def list_customers(self):
        customers = self.repo.get(search_str="")
        self.display_customer_table(customers)

    def search_customer(self):
        keyword = Prompt.ask("Enter the keyword to search")
        customers = self.repo.get(keyword)
        self.display_customer_table(customers)

    def add_customer(self):
        print("Add a new customer...")

        customer = Customers()
        customer.full_name = get_validated_input("Enter the full name")
        customer.email = get_validated_input("Enter the email", validate_email)
        customer.phone = get_validated_input(
            "Enter the phone number", validate_phone
        )
        customer.address = get_validated_input("Enter the address")
        customer.driver_license = get_validated_input(
            "Enter the driver license"
        )

        self.repo.add(customer)

        print("[i]Customer added successfully[/i]")

    def update_customer(self):
        print("Update a customer...")

        customer = Customers()
        customer.customer_id = int(
            get_validated_input("Enter the customer id", validate_digit)
        )
        customer.full_name = Prompt.ask("Enter the full name (optional)")
        customer.email = get_validated_input(
            "Enter the email (optional)", validate_email, optional=True
        )
        customer.phone = get_validated_input(
            "Enter the phone number (optional)", validate_phone, optional=True
        )
        customer.address = Prompt.ask("Enter the address (optional)")
        customer.driver_license = Prompt.ask(
            "Enter the driver license (optional)"
        )

        self.repo.update(customer)

        print("[i]Customer updated successfully[/i]")

    def delete_customer(self):
        print("Delete a customer...")

        id = get_validated_input("Enter the customer id", validate_digit)

        self.repo.delete(id)

        print("[i]Customer deleted successfully[/i]")

    def display_customer_table(self, customers):
        table = Table()
        table.add_column("id")
        table.add_column("full_name")
        table.add_column("email")
        table.add_column("phone")
        table.add_column("address")
        table.add_column("driver_license")

        for customer in customers:
            table.add_row(
                str(customer[0]),
                customer[1],
                customer[2],
                customer[3],
                customer[4],
                customer[5],
            )
        console = Console()
        console.print(table)
