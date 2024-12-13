from command import CustomerCommand


def help_command():
    print("""
        Avaliable Commands:
            /customer   Manage customers' information
            /car        Manage cars' information
        """)


def main():
    print("""Welcome to Car Rental System. Enter "/?" for usage hints.""")
    customer_command = CustomerCommand()
    while True:
        command = input("crs> ")
        if command == "/bye":
            print("Goodbye!")
            break
        elif command == "/?":
            help_command()
        elif command.startswith("/customer"):
            customer_command.handle_command(command)
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
