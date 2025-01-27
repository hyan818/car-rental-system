from command.command import Command
from globals import CurrentUser
from repository.staff import Staff, StaffRepository
from repository.users import Users, UsersRepository
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from util.validation import get_validated_input, validate_digit, validate_email


class StaffCommand(Command):
    HELP_MESSAGE = """
    Available commands:
        /staff list      List all staff
        /staff add       Add a new staff
        /staff update    Update staff information
        /staff delete    Delete a staff
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.staff_repo = StaffRepository()
        self.users_repo = UsersRepository()
        self.current_user = current_user

        self.commands = {
            "list": self.list_staffs,
            "add": self.add_staff,
            "update": self.update_staff,
            "delete": self.delete_staff,
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

    def list_staffs(self):
        staffs = self.staff_repo.get_staffs()
        self.display_staff_table(staffs)

    def add_staff(self):
        print("Add a new staff...")

        staff = Staff()
        staff.full_name = get_validated_input(
            "Enter the full name", "The full name is not none"
        )
        staff.email = get_validated_input(
            "Enter the email", "The email is not valid", validate_email
        )

        username = get_validated_input(
            "Enter your username",
            "The username has exist, please try again.",
            self.users_repo.username_exists,
            False,
        )

        password = get_validated_input(
            "Enter your password",
            "The password is invalid",
            optional=False,
            password=True,
        )

        user = Users(username=username, password=password, role_id=1)
        user_id = self.users_repo.add_user(user)

        staff.user_id = user_id

        self.staff_repo.add_staff(staff)

        print("[green]Staff added successfully[/green]")

    def update_staff(self):
        print("Update a staff... \n")

        staff = Staff()
        staff_id = get_validated_input(
            "Enter the staff id", "The staff id is not valid", validate_digit
        )
        full_name = Prompt.ask("Enter the full name (optional)")
        email = get_validated_input(
            "Enter the email (optional)", validate_email, optional=True
        )

        staff.staff_id = int(staff_id)
        staff.full_name = full_name
        staff.email = email

        self.staff_repo.update_staff(staff)

        print("[green]Staff updated successfully[/green]")

    def delete_staff(self):
        print("Delete a staff... \n")

        staff_id = get_validated_input(
            "Enter the staff id", "The staff is not valid", validate_digit
        )

        current_staff = self.staff_repo.get_by_user_id(self.current_user.user_id)
        if current_staff is None:
            print("[red]Oops, There is an error.[/red]")
            return
        if current_staff.staff_id is None:
            print("[red]Oops, There is an error.[/red]")
            return

        if int(staff_id) == current_staff.staff_id:
            print("[red]You cannot delete yourself.[/red]")
            return

        staff = self.staff_repo.get_by_staff_id(int(staff_id))
        if staff is None:
            print("[red]Can not find the staff.[/red]")
            return
        if staff.user_id is None:
            print("[red]Oops, There is an error.[/red]")
            return

        self.staff_repo.delete_staff(staff_id)
        self.users_repo.delete_user(staff.user_id)

        print("[green]Staff deleted successfully[/green]")

    def display_staff_table(self, staffs):
        table = Table()

        table.add_column("staff_id")
        table.add_column("user_id")
        table.add_column("full_name")
        table.add_column("email")
        table.add_column("created_at")

        for staff in staffs:
            table.add_row(str(staff[0]), str(staff[1]), staff[2], staff[3], staff[4])

        console = Console()
        console.print(table)
