from command.factory import Command
from globals import CurrentUser
from repository.customers import Customers, CustomersRepository
from repository.users import Users, UsersRepository
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from util.validation import (
    get_validated_input,
    validate_digit,
    validate_email,
    validate_phone,
)


class CustomerCommand(Command):
    HELP_MESSAGE = """
    Available Commands:
        /customer list    List customers' information
        /customer search  Search customers' information by name or phone number
        /customer add     Add a new customer
        /customer update  Update a customer information
        /customer delete  Delete a customer
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.repo = CustomersRepository()
        self.users_repo = UsersRepository()
        self.current_user = current_user
        self.commands = {
            "list": self.list_customers,
            "search": self.search_customer,
            "add": self.add_customer,
            "update": self.update_customer,
            "delete": self.delete_customer,
        }

    def handle(self, command):
        if self.current_user.role_name == "customer":
            print(f"[red]Unknown command: {command}[/red]")
            return
        parts = command.split()
        if len(parts) < 2:
            print(self.HELP_MESSAGE)
            return

        subcommand = parts[1]

        if subcommand in self.commands:
            self.commands[subcommand]()
        else:
            print(f"[red]Unknown subcommand: {subcommand}[/red]")

    def list_customers(self):
        customers = self.repo.get(search_str="")
        self.display_customer_table(customers)

    def search_customer(self):
        keyword = Prompt.ask("Enter the keyword to search")
        customers = self.repo.get(keyword)
        self.display_customer_table(customers)

    def add_customer(self):
        print("Add a new customer...")

        username = get_validated_input(
            "Enter your username",
            "The username has exist, please try again.",
            self.users_repo.check_username,
            False,
        )
        customer = Customers()
        customer.full_name = get_validated_input(
            "Enter the full name", "Full name can not be null"
        )
        customer.email = get_validated_input(
            "Enter the email", "The email is not valid", validate_email
        )
        customer.phone = get_validated_input(
            "Enter the phone number",
            "The phone number is not valid",
            validate_phone,
        )
        customer.address = Prompt.ask("Enter the address")
        customer.driver_license = get_validated_input(
            "Enter the driver license",
            "The driver license has exist.",
            self.repo.check_driver_license,
            False,
        )

        password = get_validated_input(
            "Enter your password",
            "The password is invalid",
            optional=False,
            password=True,
        )
        user = Users(username=username, password=password, role_id=2)
        user_id = self.users_repo.add(user)

        customer.user_id = user_id
        self.repo.add(customer)

        print("[green]Customer added successfully[/green]")

    def update_customer(self):
        print("Update a customer...")

        customer = Customers()

        customer_id = get_validated_input(
            "Enter the customer id",
            "The customer id is not valid",
            validate_digit,
        )
        customer.customer_id = int(customer_id)
        customer.full_name = Prompt.ask("Enter the full name (optional)")
        customer.email = get_validated_input(
            "Enter the email (optional)",
            "The email is not valid",
            validate_email,
            optional=True,
        )
        customer.phone = get_validated_input(
            "Enter the phone number (optional)",
            "The phone number is not valid",
            validate_phone,
            optional=True,
        )
        customer.address = Prompt.ask("Enter the address (optional)")
        customer.driver_license = Prompt.ask(
            "Enter the driver license (optional)"
        )

        self.repo.update(customer)

        print("[green]Customer updated successfully[/green]")

    def delete_customer(self):
        print("Delete a customer...")

        id = get_validated_input(
            "Enter the customer id",
            "The customer id is not valid",
            validate_digit,
        )

        customer = self.repo.get_by_customer_id(id)
        if customer is None:
            print("[red]Can not find the customer[/red]")
            return

        self.repo.delete(id)
        self.users_repo.delete(customer.user_id)
        print("[green]Customer deleted successfully[/green]")

    def display_customer_table(self, customers):
        table = Table()
        table.add_column("customer_id")
        table.add_column("user_id")
        table.add_column("full_name")
        table.add_column("email")
        table.add_column("phone")
        table.add_column("address")
        table.add_column("driver_license")
        table.add_column("created_at")

        for customer in customers:
            table.add_row(
                str(customer[0]),
                str(customer[1]),
                customer[2],
                customer[3],
                customer[4],
                customer[5],
                customer[6],
                customer[7],
            )
        console = Console()
        console.print(table)
