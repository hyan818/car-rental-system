from typing import Optional

from command.factory import CommandFactory
from command.users import UsersCommand
from globals import CurrentUser
from rich import print


def welcome_prompt() -> Optional[CurrentUser]:
    print("""
    Welcome to Car Rental System. (Creator by Yan Huang)

    Available command:
        /register Register a customer account
        /login    Login into the system
        /bye      Exit the program
        """)

    users_command = UsersCommand()
    while True:
        command = input(">>> ")
        if command == "/register":
            users_command.handle_register_command()
            print("Use /login command to login into system")
        elif command == "/login":
            user = users_command.handle_login_command()
            if user is None:
                print("[red]Invalid username or password. Please try again.[/red]")
            else:
                print(f"[green]Welcome {user.username}[/green]")
                return user
        elif command == "/bye":
            return None
        else:
            print(f"[red]Unknown command: {command}[/red]")


if __name__ == "__main__":
    current_user = welcome_prompt()
    if current_user is not None:
        while True:
            type = input(">>> ")
            if type == "/bye":
                print("Goodbye!")
                break
            else:
                command_handler = CommandFactory.get_command(type, current_user)
                if command_handler:
                    command_handler.handle(type)
