from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from repository.vehicles import Vehicles, VehiclesRepository
from validation import (
    get_validated_input,
    validate_digit,
    validate_price,
    validate_year,
)


class VehicleCommand:
    HELP_MESSAGE = """
    Available Commands:
        /vehicle list    List vehicles' information
        /vehicle search  Search vehicles by brand
        /vehicle add     Add a new vehicle
        /vehicle update  Update a vehicle information
        /vehicle del     Delete a vehicle
    """

    def __init__(self) -> None:
        self.repo = VehiclesRepository()
        self.commands = {
            "list": self.list_vehicles,
            "search": self.search_vehicle,
            "add": self.add_vehicle,
            "update": self.update_vehicle,
            "del": self.delete_vehicle,
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

    def list_vehicles(self):
        vehicles = self.repo.get(search_str="")
        self.display_vehicle_table(vehicles)

    def search_vehicle(self):
        keyword = Prompt.ask("Enter the brand to search")
        vehicles = self.repo.get(keyword)
        self.display_vehicle_table(vehicles)

    def add_vehicle(self):
        print("Add a new vehicle...")

        vehicle = Vehicles()
        vehicle.brand = get_validated_input("Enter the brand")
        vehicle.model = get_validated_input("Enter the model")
        vehicle.year = int(get_validated_input("Enter the year", validate_year))
        vehicle.license_plate = get_validated_input("Enter the license plate")
        vehicle.mileage = int(
            get_validated_input("Enter the mileage", validate_digit)
        )
        vehicle.daily_rate = float(
            get_validated_input("Enter the daily rate", validate_price)
        )
        vehicle.description = Prompt.ask("Enter the description (Optional)")
        vehicle.status = Prompt.ask(
            "Enter the status",
            choices=["available", "rented", "maintenance"],
            default="available",
        )

        self.repo.add(vehicle)

        print("[i]Vehicle added successfully[/i]")

    def update_vehicle(self):
        print("Update a vehicle...")

        vehicle = Vehicles()
        vehicle.vehicle_id = int(
            get_validated_input("Enter the vehicle id", validate_digit)
        )
        vehicle.brand = Prompt.ask("Enter the brand (optional)")
        vehicle.model = Prompt.ask("Enter the model (optional)")
        year = get_validated_input(
            "Enter the year (optional)", validate_year, optional=True
        )
        vehicle.year = int(year) if year else None
        vehicle.license_plate = Prompt.ask("Enter the license plate (optional)")

        mileage = get_validated_input(
            "Enter the mileage (optional)", validate_digit, optional=True
        )
        vehicle.mileage = int(mileage) if mileage else None
        daily_rate = get_validated_input(
            "Enter the daily rate (optional)", validate_price, optional=True
        )
        vehicle.daily_rate = float(daily_rate) if daily_rate else None
        vehicle.description = Prompt.ask("Enter the description (optional)")
        vehicle.status = Prompt.ask(
            "Enter the status (optional)",
            choices=["", "available", "rented", "maintenance"],
            default="",
            show_default=False,
        )

        self.repo.update(vehicle)

        print("[i]Vehicle updated successfully[/i]")

    def delete_vehicle(self):
        print("Delete a vehicle...")

        id = get_validated_input("Enter the vehicle id", validate_digit)

        self.repo.delete(int(id))

        print("[i]Vehicle deleted successfully[/i]")

    def display_vehicle_table(self, vehicles):
        table = Table()
        table.add_column("id")
        table.add_column("brand")
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
