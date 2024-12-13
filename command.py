from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from repository import CustomerRepository
from validation import (
    get_validated_input,
    validate_email,
    validate_id,
    validate_phone,
)


class CustomerCommand:
    PAGE_SIZE = 10
    HELP_MESSAGE = """
    Available Commands:
        /customer list    List customers' information
        /customer search  Search customers' information by name or phone number
        /customer add     Add a new customer
        /customer update  Update a customer information
        /customer del     Delete a customer
    """

    def __init__(self) -> None:
        self.repo = CustomerRepository()
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
        page = 1
        total = self.repo.get_total()
        if total == 0:
            print("[i]no data...[/i]")
        else:
            while total > 0:
                offset = (page - 1) * self.PAGE_SIZE
                customers = self.repo.get_all(self.PAGE_SIZE, offset)
                self.display_customer_table(customers)
                total -= 10
                page += 1
                if total > 0:
                    k = input("Press any key go to next page: ")
                    if k.lower() == "q":
                        break

    def search_customer(self):
        keyword = Prompt.ask("Enter the keyword to search")
        list = self.repo.search(keyword)
        print(list)

    def add_customer(self):
        print("Add a new customer...")

        first_name = get_validated_input("Enter the first name")
        last_name = get_validated_input("Enter the last name")
        email = get_validated_input("Enter the email", validate_email)
        phone = get_validated_input("Enter the phone number", validate_phone)

        self.repo.add(first_name, last_name, email, phone)

        print("[i]Customer added successfully[/i]")

    def update_customer(self):
        print("Update a customer...")

        id = get_validated_input("Enter the customer id", validate_id)
        first_name = Prompt.ask("Enter the first name (optional)")
        last_name = Prompt.ask("Enter the last name (optional)")
        email = get_validated_input(
            "Enter the email (optional)", validate_email
        )
        phone = get_validated_input(
            "Enter the phone number (optional)", validate_phone
        )

        self.repo.update(first_name, last_name, email, phone, id)

        print("[i]Customer updated successfully[/i]")

    def delete_customer(self):
        print("Delete a customer...")

        id = get_validated_input("Enter the customer id", validate_id)

        self.repo.delete(id)

        print("[i]Customer deleted successfully[/i]")

    def display_customer_table(self, customers):
        table = Table()
        table.add_column("id")
        table.add_column("first_name")
        table.add_column("last_name")
        table.add_column("email")
        table.add_column("phone")

        for customer in customers:
            table.add_row(
                str(customer[0]),
                customer[1],
                customer[2],
                customer[3],
                customer[4],
            )
        console = Console()
        console.print(table)
