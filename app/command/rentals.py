from datetime import datetime, timedelta

from command.command import Command
from globals import CurrentUser
from repository.customers import CustomersRepository
from repository.rentals import Rentals, RentalsRepository
from repository.staff import StaffRepository
from repository.vehicles import VehiclesRepository
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from util.validation import get_validated_input, validate_digit


class RentalCommand(Command):
    STAFF_AVAILABLE_COMMANDS = """
    Available Commands:
        /rental list     List all rentals
        /rental active   List active rentals
        /rental add      Create a new rental
        /rental audit    Active or reject a rental application
        /rental complete Complete a rental
        /rental cancel   Cancel a rental
    """

    CUSTOMER_AVAILABLE_COMMANDS = """
    Available Commands:
        /rental list     List rental history
        /rental book     Book a new rental
        /rental cancel   Cancel a rental
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.rental_repo = RentalsRepository()
        self.current_user = current_user
        self.customer_repo = CustomersRepository()
        self.staff_repo = StaffRepository()
        self.vehicle_repo = VehiclesRepository()
        self.staff_commands = {
            "list": self.list_rentals,
            "active": self.list_active_rentals,
            "add": self.add_rental,
            "audit": self.audit_rental,
            "complete": self.complete_rental,
            "cancel": self.cancel_rental,
        }

        self.customer_commands = {
            "list": self.list_rental_history,
            "book": self.book_rental,
            "cancel": self.cancel_rental,
        }

    def handle(self, command):
        parts = command.split()
        if len(parts) < 2:
            if self.current_user.role_name == "customer":
                print(self.CUSTOMER_AVAILABLE_COMMANDS)
            else:
                print(self.STAFF_AVAILABLE_COMMANDS)
            return

        subcommand = parts[1]

        if self.current_user.role_name == "customer":
            if subcommand in self.customer_commands:
                self.customer_commands[subcommand]()
            else:
                print(f"[red]Unknown subcommand: {subcommand}[/red]")
        else:
            if subcommand in self.staff_commands:
                self.staff_commands[subcommand]()
            else:
                print(f"[red]Unknown subcommand: {subcommand}[/red]")

    def list_rentals(self):
        rentals = self.rental_repo.get_rental_details()
        self.display_rental_table(rentals)

    def list_active_rentals(self):
        rentals = self.rental_repo.get_rental_details("active")
        self.display_rental_table(rentals)

    def add_rental(self):
        print("Create a new rental...")

        rental = Rentals()

        vehicle_id = get_validated_input(
            "Enter the vehicle ID", "The value is not valid", validate_digit
        )
        rental.vehicle_id = int(vehicle_id)
        customer_id = get_validated_input(
            "Enter the customer ID", "The value is not valid", validate_digit
        )
        rental.customer_id = int(customer_id)

        staff = self.staff_repo.get_by_user_id(self.current_user.user_id)
        if staff is None:
            print("[red]Can not find your information[/red]")
            return
        if staff.staff_id is None:
            print("[red]Oops. There is an error[/red]")
            return

        rental.staff_id = staff.staff_id

        # Set dates
        rental.start_date = datetime.now()
        days = get_validated_input(
            "Enter rental duration (days)",
            "The value is not valid",
            validate_digit,
        )
        rental.expected_return_date = rental.start_date + timedelta(
            days=int(days)
        )

        # Get vehicle information for initial mileage and cost calculation
        vehicle = self.vehicle_repo.get_by_id(rental.vehicle_id)
        if not vehicle:
            print("[red]Vehicle not found[/red]")
            return

        # Check if vehicle is available
        if vehicle.status != "available":
            print("[red]Vehicle is not available for rent[/red]")
            return

        if vehicle.mileage is None:
            print(
                "[yellow]Warning: Vehicle mileage is 0, consider checking the vehicle before rental[/yellow]"
            )
            return
        rental.initial_mileage = vehicle.mileage  # mileage from vehicle record

        if vehicle.daily_rate is None:
            print("[red]Vehicle daily rate is not set[/red]")
            return

        rental.total_cost = vehicle.daily_rate * int(days)  # daily_rate * days
        rental.rental_status = "active"

        # Update vehicle status
        self.vehicle_repo.update_status(rental.vehicle_id, "rented")

        self.rental_repo.add_rental(rental)
        print("[green]Rental created successfully[/green]")

    def complete_rental(self):
        print("Complete a rental...")

        rental_id = get_validated_input(
            "Enter the rental ID", "The value is not valid", validate_digit
        )

        return_mileage = get_validated_input(
            "Enter return mileage", "The value is not valid", validate_digit
        )

        rental = self.rental_repo.get_by_id(int(rental_id))
        if not rental:
            print("[red]Rental not found[/red]")
            return
        if int(return_mileage) < rental.initial_mileage:
            print(
                "[red]Return mileage cannot be less than initial mileage[/red]"
            )
            return
        if not rental.vehicle_id:
            print("[red]Vehicle not found[/red]")
            return

        self.rental_repo.complete_rental(
            int(rental_id), int(return_mileage), datetime.now()
        )
        self.vehicle_repo.update_after_return(
            rental.vehicle_id, int(return_mileage)
        )
        print("[green]Rental completed successfully[/green]")

    def cancel_rental(self):
        print("Cancel a rental...")

        rental_id = get_validated_input(
            "Enter the rental ID", "The value is not valid", validate_digit
        )
        rental = self.rental_repo.get_by_id(int(rental_id))
        if rental is None:
            print("[red]Can not find this rental data[/red]")
            return
        if rental.rental_status != "apply":
            print(
                "[red]This rental status has been changed, please check its details[/red]"
            )
            return
        self.rental_repo.update_status(int(rental_id), "cancel")

        # Update the vehicle status is available
        if rental.vehicle_id:
            self.vehicle_repo.update_status(rental.vehicle_id, "available")

        print("[green]Rental cancelled successfully[/green]")

    def display_rental_table(self, rentals):
        table = Table()
        table.add_column("ID")
        table.add_column("Vehicle")
        table.add_column("Customer")
        table.add_column("Start Date")
        table.add_column("Expected Return")
        table.add_column("Actual Return")
        table.add_column("Initial Mileage")
        table.add_column("Return Mileage")
        table.add_column("Status")
        table.add_column("Total Cost")

        for rental in rentals:
            table.add_row(
                str(rental[0]),
                f"{rental[1]} {rental[2]}",  # brand + model
                rental[3],  # customer name
                str(rental[4]),
                str(rental[5]),
                str(rental[6] or ""),
                str(rental[7]),
                str(rental[8] or ""),
                rental[9],
                f"${rental[10]}" if rental[10] else "",
            )

        console = Console()
        console.print(table)

    def list_rental_history(self):
        customer = self.customer_repo.get_by_user_id(self.current_user.user_id)
        if customer is None:
            print("[red]Can not find your infomation[/red]")
            return
        if customer.customer_id is None:
            print("[red]Oops, there is an error[/red]")
            return
        rentals = self.rental_repo.get_rental_details(
            customer_id=customer.customer_id
        )
        self.display_rental_table(rentals)

    def book_rental(self):
        print("Book a new rental...")

        customer = self.customer_repo.get_by_user_id(self.current_user.user_id)
        if customer is None:
            print("[red]Can not find your infomation[/red]")
            return
        if customer.customer_id is None:
            print("[red]Oops, there is an error[/red]")
            return

        rental = Rentals()
        vehicle_id = get_validated_input(
            "Enter the vehicle ID",
            "The vehicle id should be number",
            validator=validate_digit,
            optional=False,
        )
        rental.vehicle_id = int(vehicle_id)
        rental.customer_id = customer.customer_id

        rental.start_date = datetime.now()
        days = get_validated_input(
            "Enter rental duration (days)",
            "The rental duration should be number",
            validate_digit,
        )
        rental.expected_return_date = rental.start_date + timedelta(
            days=int(days)
        )

        # Get vehicle information for initial mileage and cost calculation
        vehicle = self.vehicle_repo.get_by_id(rental.vehicle_id)
        if not vehicle:
            print("[red]Vehicle not found[/red]")
            return

        # Check if vehicle is available
        if vehicle.status != "available":
            print("[red]Vehicle is not available for rent[/red]")
            return

        if vehicle.mileage is None:
            print(
                "[yellow]Warning: Vehicle mileage is 0, consider checking the vehicle before rental[/yellow]"
            )
            return
        rental.initial_mileage = vehicle.mileage  # mileage from vehicle record

        if vehicle.daily_rate is None:
            print("[red]Vehicle daily rate is not set[/red]")
            return

        rental.total_cost = vehicle.daily_rate * int(days)  # daily_rate * days

        # Update vehicle status
        self.vehicle_repo.update_status(rental.vehicle_id, "rented")

        self.rental_repo.add_rental(rental)
        print("[green]Rental created successfully[/green]")

    def audit_rental(self):
        rental_id = get_validated_input(
            "Enter the rental ID", "The value is not valid", validate_digit
        )
        rental = self.rental_repo.get_by_id(int(rental_id))
        if rental is None:
            print("[red]Can not find this rental data[/red]")
            return
        if rental.rental_status != "apply":
            print(
                "[red]This rental status has been changed, please check its details[/red]"
            )
            return

        status = Prompt.ask(
            "Enter the status",
            choices=["active", "reject"],
            default="reject",
        )

        self.rental_repo.update_status(int(rental_id), status)

        # If reject the application then update the vehicle status to available
        if status == "reject" and rental.vehicle_id:
            self.vehicle_repo.update_status(rental.vehicle_id, "available")

        print("[green]Change rental status successfully[/green]")
