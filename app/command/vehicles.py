from command.command import Command
from globals import CurrentUser
from repository.vehicles import Vehicles, VehiclesRepository
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from util.decorator import singleton
from util.validation import (
    get_validated_input,
    validate_digit,
    validate_price,
    validate_year,
)


@singleton
class VehicleCommand(Command):
    STAFF_AVAILABLE_COMMANDS = """
    Available Commands:
        /vehicle list    List vehicles' information
        /vehicle search  Search vehicles by make
        /vehicle add     Add a new vehicle
        /vehicle update  Update a vehicle information
        /vehicle delete  Delete a vehicle
    """

    CUSTOMER_AVAILABLE_COMMANDS = """
    Available Commands:
        /vehicle list    List vehicles' information
        /vehicle search  Search vehicles by make
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.vehicles_repo = VehiclesRepository()
        self.current_user = current_user
        self.staff_commands = {
            "list": self.list_vehicles,
            "search": self.search_vehicle,
            "add": self.add_vehicle,
            "update": self.update_vehicle,
            "delete": self.delete_vehicle,
        }
        self.customer_commands = {
            "list": self.list_available_vehicles,
            "search": self.search_available_vehicles,
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

    def list_vehicles(self):
        vehicles = self.vehicles_repo.get_vehicles(search_str="")
        self.display_vehicle_table(vehicles)

    def search_vehicle(self):
        keyword = Prompt.ask("Enter the make to search")
        vehicles = self.vehicles_repo.get_vehicles(keyword)
        self.display_vehicle_table(vehicles)

    def add_vehicle(self):
        vehicle = Vehicles()
        vehicle.make = get_validated_input("Enter the make", "The make should not none")
        vehicle.model = get_validated_input(
            "Enter the model", "The model should not none"
        )
        year = get_validated_input(
            "Enter the year", "The year is not valid", validate_year
        )
        vehicle.year = int(year)
        vehicle.license_plate = get_validated_input(
            "Enter the license plate", "The license plate should not none"
        )

        mileage = get_validated_input(
            "Enter the mileage", "The value is not valid", validate_digit
        )
        vehicle.mileage = int(mileage)
        daily_rate = get_validated_input(
            "Enter the daily rate", "The value is not valid", validate_price
        )
        vehicle.daily_rate = float(daily_rate)
        vehicle.description = Prompt.ask("Enter the description (Optional)")
        vehicle.status = Prompt.ask(
            "Enter the status",
            choices=["available", "rented", "maintenance"],
            default="available",
        )

        self.vehicles_repo.add_vehicle(vehicle)

        print("[green]Vehicle added successfully[/green]")

    def update_vehicle(self):
        vehicle = Vehicles()

        vehicle_id = get_validated_input(
            "Enter the vehicle id", "The value is not valid", validate_digit
        )
        vehicle.vehicle_id = int(vehicle_id)
        vehicle.make = Prompt.ask("Enter the make (optional)")
        vehicle.model = Prompt.ask("Enter the model (optional)")
        year = get_validated_input(
            "Enter the year (optional)",
            "The value is not valid",
            validate_year,
            optional=True,
        )
        vehicle.year = int(year) if year else None
        vehicle.license_plate = Prompt.ask("Enter the license plate (optional)")

        mileage = get_validated_input(
            "Enter the mileage (optional)",
            "The value is not valid",
            validate_digit,
            optional=True,
        )
        vehicle.mileage = int(mileage) if mileage else None
        daily_rate = get_validated_input(
            "Enter the daily rate (optional)",
            "The value is not valid",
            validate_price,
            optional=True,
        )
        vehicle.daily_rate = float(daily_rate) if daily_rate else None
        vehicle.description = Prompt.ask("Enter the description (optional)")
        vehicle.status = Prompt.ask(
            "Enter the status (optional)",
            choices=["", "available", "rented", "maintenance"],
            default="",
            show_default=False,
        )

        self.vehicles_repo.update_vehicle(vehicle)

        print("[green]Vehicle updated successfully[/green]")

    def delete_vehicle(self):
        id = get_validated_input(
            "Enter the vehicle id", "The value is not valid", validate_digit
        )
        self.vehicles_repo.delete_vehicle(int(id))
        print("[green]Vehicle deleted successfully[/green]")

    def display_vehicle_table(self, vehicles):
        table = Table()
        table.add_column("id")
        table.add_column("make")
        table.add_column("model")
        table.add_column("year")
        table.add_column("license_plate")
        table.add_column("mileage")
        table.add_column("daily_rate")
        table.add_column("description")
        table.add_column("status")

        for vehicle in vehicles:
            table.add_row(
                str(vehicle[0]),
                vehicle[1],
                vehicle[2],
                str(vehicle[3]),
                vehicle[4],
                str(vehicle[5]),
                str(vehicle[6]),
                vehicle[7],
                vehicle[8],
            )

        console = Console()
        console.print(table)

    def list_available_vehicles(self):
        vehicles = self.vehicles_repo.get_vehicles(status="available")
        self.display_vehicle_table(vehicles)

    def search_available_vehicles(self):
        keyword = Prompt.ask("Enter the make to search")
        vehicles = self.vehicles_repo.get_vehicles(
            search_str=keyword, status="available"
        )
        self.display_vehicle_table(vehicles)
