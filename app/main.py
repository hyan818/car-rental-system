from typing import Optional

from command.factory import CommandFactory
from command.users import UsersCommand
from globals import CurrentUser
from repository.customers import CustomersRepository
from repository.rentals import RentalsRepository
from repository.roles import RoleRepository
from repository.staff import StaffRepository
from repository.users import UsersRepository
from repository.vehicles import VehiclesRepository
from rich import print


def welcome_prompt() -> Optional[CurrentUser]:
    print("""
    Welcome to Car Rental System.

    Available command:
        /register Register a customer account
        /login    Login into the system
        /bye      Exit the program
        """)

    users_command = UsersCommand()
    while True:
        try:
            command = input(">>> ")
            if command == "/register":
                users_command.handle_register_command()
                print("Use /login command to login into system")
            elif command == "/login":
                user = users_command.handle_login_command()
                if user is None:
                    print(
                        "[red]Invalid username or password. Please try again.[/red]"
                    )
                else:
                    print(f"[green]Welcome {user.username}[/green]")
                    return user
            elif command == "/bye":
                return None
            else:
                print(f"[red]Unknown command: {command}[/red]")
        except KeyboardInterrupt:
            print("\n")
            pass


def initialize():
    customerRepo = CustomersRepository()
    customerRepo.create_table()
    rentalRepo = RentalsRepository()
    rentalRepo.create_table()
    roleRepo = RoleRepository()
    roleRepo.create_table()
    staffRepo = StaffRepository()
    staffRepo.create_table()
    usersRepo = UsersRepository()
    usersRepo.create_table()
    vehiclesRepo = VehiclesRepository()
    vehiclesRepo.create_table()


if __name__ == "__main__":
    initialize()

    current_user = welcome_prompt()
    if current_user is not None:
        while True:
            try:
                type = input(">>> ")
                if type == "/bye":
                    print("Goodbye!")
                    break
                else:
                    command_handler = CommandFactory.get_command(
                        type, current_user
                    )
                    if command_handler:
                        command_handler.handle(type)
            except KeyboardInterrupt:
                print("\n")
                pass
