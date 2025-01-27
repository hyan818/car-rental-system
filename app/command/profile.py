import bcrypt
from command.command import Command
from globals import CurrentUser
from repository.customers import Customers, CustomersRepository
from repository.staff import Staff, StaffRepository
from repository.users import UsersRepository
from rich import print
from rich.prompt import Prompt
from util.decorator import singleton
from util.validation import get_validated_input, validate_email, validate_phone


@singleton
class ProfileCommand(Command):
    HELP_MESSAGE = """
    Available Command:
        /profile detail     View profile details
        /profile update     Update profile details
        /profile password   Update password
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.current_user = current_user
        self.user_repo = UsersRepository()
        self.customer_repo = CustomersRepository()
        self.staff_repo = StaffRepository()
        self.commands = {
            "detail": self.get_details,
            "update": self.update_details,
            "password": self.update_password,
        }

    def handle(self, command):
        parts = command.split()
        if len(parts) < 2:
            print(self.HELP_MESSAGE)
            return

        subcommand = parts[1]

        if subcommand in self.commands:
            self.commands[subcommand]()
        else:
            print(f"[red]Unknown subcommand: {subcommand}[/red]")

    def get_details(self):
        if self.current_user.role_name == "customer":
            customer = self.customer_repo.get_by_user_id(self.current_user.user_id)
            if customer is None:
                print("[red]Can't find the details. [/red]")
            else:
                print(f"Full Name: {customer.full_name}")
                print(f"Email: {customer.email}")
                print(f"Phone: {customer.phone}")
                print(f"Address: {customer.address}")
                print(f"Driver License: {customer.driver_license}")
        else:
            staff = self.staff_repo.get_by_user_id(self.current_user.user_id)
            if staff is None:
                print("[red]Can't find the details. [/red]")
            else:
                print(f"Full Name: {staff.full_name}")
                print(f"Email: {staff.email}")

    def update_details(self):
        print("Update your profile...")
        if self.current_user.role_name == "customer":
            current_customer = self.customer_repo.get_by_user_id(
                self.current_user.user_id
            )
            if current_customer is None:
                print("[red]Can not find your data[/red]")
                return
            customer = Customers()
            customer.customer_id = current_customer.customer_id
            customer.full_name = Prompt.ask("Enter the full name (optional)")
            customer.email = get_validated_input(
                "Enter the email (optional)", validate_email, optional=True
            )
            customer.phone = get_validated_input(
                "Enter the phone number (optional)",
                validate_phone,
                optional=True,
            )
            customer.address = Prompt.ask("Enter the address (optional)")
            customer.driver_license = Prompt.ask("Enter the driver license (optional)")
            self.customer_repo.update_customer(customer)
            print("[green]Update profile successfully[/green]")
        else:
            current_staff = self.staff_repo.get_by_user_id(self.current_user.user_id)
            if current_staff is None:
                print("[red]Can not find your data[/red]")
                return
            staff = Staff()
            staff.staff_id = current_staff.staff_id
            full_name = Prompt.ask("Enter the full name (optional)")
            email = get_validated_input(
                "Enter the email (optional)", validate_email, optional=True
            )
            staff.full_name = full_name
            staff.email = email
            self.staff_repo.update_staff(staff)
            print("[green]Update profile successfully[/green]")

    def update_password(self):
        current_password = get_validated_input(
            "Enter your current password",
            "The password is invalid",
            optional=False,
            password=True,
        )

        new_password = get_validated_input(
            "Enter your new password",
            "The password is invalid",
            optional=False,
            password=True,
        )

        user = self.user_repo.get_by_user_id(self.current_user.user_id)
        if user is None:
            print("[red]Can not find your user details.[/red]")
            return

        if bcrypt.checkpw(current_password.encode("utf-8"), user.password.encode()):
            hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            self.user_repo.update_password(user.user_id, hashed.decode("utf-8"))
            print("[green]Password updated.[/green]")
        else:
            print("[red]Your current password is incorrect.[/red]")
