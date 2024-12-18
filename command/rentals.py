from datetime import datetime, timedelta

from rich import print
from rich.console import Console
from rich.table import Table

import globals
from repository.rentals import Rentals, RentalsRepository
from repository.vehicles import VehiclesRepository
from validation import get_validated_input, validate_digit


class RentalCommand:
    HELP_MESSAGE = """
    Available Commands:
        /rental list     List all rentals
        /rental active   List active rentals
        /rental add      Create a new rental
        /rental complete Complete a rental
        /rental cancel   Cancel a rental
    """

    def __init__(self) -> None:
        self.repo = RentalsRepository()
        self.vehicle_repo = VehiclesRepository()
        self.commands = {
            "list": self.list_rentals,
            "active": self.list_active_rentals,
            "add": self.add_rental,
            "complete": self.complete_rental,
            "cancel": self.cancel_rental,
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

    def list_rentals(self):
        rentals = self.repo.get()
        self.display_rental_table(rentals)

    def list_active_rentals(self):
        rentals = self.repo.get("active")
        self.display_rental_table(rentals)

    def add_rental(self):
        print("Create a new rental...")

        rental = Rentals()
        rental.vehicle_id = int(
            get_validated_input("Enter the vehicle ID", validate_digit)
        )
        rental.customer_id = int(
            get_validated_input("Enter the customer ID", validate_digit)
        )
        rental.staff_id = globals.current_staff.staff_id

        # Set dates
        rental.start_date = datetime.now()
        days = int(
            get_validated_input("Enter rental duration (days)", validate_digit)
        )
        rental.expected_return_date = rental.start_date + timedelta(days=days)

        # Get vehicle information for initial mileage and cost calculation
        vehicle = self.vehicle_repo.get_by_id(rental.vehicle_id)
        if not vehicle:
            print("[red]Vehicle not found[/red]")
            return

        # Check if vehicle is available
        if vehicle[8] != "available":
            print("[red]Vehicle is not available for rent[/red]")
            return

        rental.initial_mileage = vehicle[5]  # mileage from vehicle record
        rental.total_cost = vehicle[6] * days  # daily_rate * days

        # Update vehicle status
        self.vehicle_repo.update_status(rental.vehicle_id, "rented")

        self.repo.add(rental)
        print("[green]Rental created successfully[/green]")

    def complete_rental(self):
        print("Complete a rental...")

        rental_id = int(
            get_validated_input("Enter the rental ID", validate_digit)
        )
        return_mileage = int(
            get_validated_input("Enter return mileage", validate_digit)
        )

        rental = self.repo.get_by_id(rental_id)
        if not rental:
            print("[red]Rental not found[/red]")
            return
        if return_mileage < rental.initial_mileage:
            print(
                "[red]Return mileage cannot be less than initial mileage[/red]"
            )
            return
        if not rental.vehicle_id:
            print("[red]Vehicle not found[/red]")
            return

        self.repo.complete_rental(rental_id, return_mileage, datetime.now())
        self.vehicle_repo.update_after_return(rental.vehicle_id, return_mileage)
        print("[green]Rental completed successfully[/green]")

    def cancel_rental(self):
        print("Cancel a rental...")

        rental_id = int(
            get_validated_input("Enter the rental ID", validate_digit)
        )
        self.repo.cancel_rental(rental_id)
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
