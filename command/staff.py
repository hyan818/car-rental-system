from typing import Optional

import bcrypt
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

import globals
from repository.staff import Staff, StaffRepository
from validation import get_validated_input, validate_digit, validate_email


class StaffCommand:
    HELP_MESSAGE = """
    Available commands:
        /staff list      List all staff
        /staff add       Add a new staff
        /staff update    Update staff information
        /staff delete    Delete a staff
        /staff password  Change password
    """

    def __init__(self) -> None:
        self.repo = StaffRepository()
        self.commands = {
            "password": self.change_password,
            "list": self.list,
            "add": self.add,
            "update": self.update,
            "delete": self.delete,
        }

    def login(self, username, password) -> Optional[Staff]:
        staff = self.repo.get_by_username(username)
        if staff and bcrypt.checkpw(
            password.encode("utf-8"), staff.password.encode()
        ):
            if staff.staff_id:
                self.repo.update_last_login(staff.staff_id)
            return staff
        return None

    def handle(self, command):
        parts = command.split()
        if len(parts) < 2:
            print(self.HELP_MESSAGE)
            return

        subcommand = parts[1]

        if subcommand in self.commands:
            return self.commands[subcommand]()
        else:
            return f"unknown subcommand: {subcommand}"

    def change_password(self):
        current_password = Prompt.ask(
            "Enter your current password", password=True
        )
        new_password = Prompt.ask("Enter your new password", password=True)

        if bcrypt.checkpw(
            current_password.encode("utf-8"),
            globals.current_staff.password.encode(),
        ):
            hashed = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            )
            globals.current_staff.password = hashed.decode("utf-8")
            self.repo.update_password(globals.current_staff)
            print("Password updated.")
        else:
            print("Your current password is incorrect.")

    def list(self):
        staffs = self.repo.get()
        self.display_staff_table(staffs)

    def add(self):
        print("Add a new staff...")

        staff = Staff()
        staff.full_name = get_validated_input("Enter the full name")
        staff.email = get_validated_input("Enter the email", validate_email)
        staff.username = get_validated_input("Enter the username")
        password = Prompt.ask("Enter the password", password=True)

        staff.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.repo.add(staff)

        print("[i]Staff added successfully[/i]")

    def update(self):
        print("Update a staff... \n")

        staff = Staff()
        staff_id = get_validated_input("Enter the staff id", validate_digit)
        full_name = Prompt.ask("Enter the full name (optional)")
        email = get_validated_input(
            "Enter the email (optional)", validate_email, optional=True
        )
        username = Prompt.ask("Enter the username (optional)")

        staff.staff_id = int(staff_id)
        staff.full_name = full_name
        staff.email = email
        staff.username = username

        self.repo.update(staff)

        print("[i]Staff updated successfully[/i]")

    def delete(self):
        print("Delete a staff... \n")

        staff_id = int(
            get_validated_input("Enter the staff id", validate_digit)
        )
        if staff_id == globals.current_staff.staff_id:
            print("You cannot delete yourself.")
            return
        self.repo.delete(staff_id)

        print("[i]Staff deleted successfully[/i]")

    def display_staff_table(self, staffs):
        table = Table()

        table.add_column("staff_id")
        table.add_column("username")
        table.add_column("full_name")
        table.add_column("email")
        table.add_column("last_login")

        for staff in staffs:
            table.add_row(str(staff[0]), staff[1], staff[2], staff[3], staff[4])

        console = Console()
        console.print(table)
