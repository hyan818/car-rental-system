from rich import print
from rich.prompt import Prompt

import globals
from command.customers import CustomerCommand
from command.help import HelpCommand
from command.staff import StaffCommand
from command.vehicles import VehicleCommand


def login_prompt():
    username = Prompt.ask("Enter your username")
    password = Prompt.ask("Enter your password", password=True)
    staff_command = StaffCommand()
    staff = staff_command.login(username, password)
    if staff is None:
        print("Invalid username or password. Please try again.")
        login_prompt()
    else:
        globals.current_staff = staff
        print(f"Welcome, {staff.full_name}!")


def main():
    print("""Welcome to Car Rental System.""")
    login_prompt()

    help_command = HelpCommand()
    customer_command = CustomerCommand()
    staff_command = StaffCommand()
    vehicle_command = VehicleCommand()
    while True:
        command = input("crs> ")
        if command == "/bye":
            print("Goodbye!")
            break
        elif command == "/?":
            help_command.handle_command()
        elif command.startswith("/customer"):
            customer_command.handle_command(command)
        elif command.startswith("/staff"):
            staff_command.handle(command)
        elif command.startswith("/vehicle"):
            vehicle_command.handle_command(command)
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
