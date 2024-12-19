from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table

import globals
from repository.maintenance import Maintenance, MaintenanceRepository
from repository.vehicles import VehiclesRepository
from util.validation import get_validated_input, validate_digit, validate_price


class MaintenanceCommand:
    HELP_MESSAGE = """
    Available Commands:
        /maintenance list      List all maintenance records
        /maintenance ongoing   List ongoing maintenance
        /maintenance add       Add new maintenance record
        /maintenance start     Start maintenance (update to ongoing)
        /maintenance complete  Complete maintenance
        /maintenance del       Delete maintenance record
    """

    def __init__(self) -> None:
        self.repo = MaintenanceRepository()
        self.vehicle_repo = VehiclesRepository()
        self.commands = {
            "list": self.list_maintenance,
            "ongoing": self.list_ongoing,
            "add": self.add_maintenance,
            "start": self.start_maintenance,
            "complete": self.complete_maintenance,
            "del": self.delete_maintenance,
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

    def list_maintenance(self):
        records = self.repo.get()
        self.display_maintenance_table(records)

    def list_ongoing(self):
        records = self.repo.get("ongoing")
        self.display_maintenance_table(records)

    def add_maintenance(self):
        print("Add new maintenance record...")

        maintenance = Maintenance()
        maintenance.vehicle_id = int(
            get_validated_input("Enter vehicle ID", validate_digit)
        )

        # Check if vehicle exists and update its status
        vehicle = self.vehicle_repo.get_by_id(maintenance.vehicle_id)
        if not vehicle:
            print("[red]Vehicle not found[/red]")
            return

        if vehicle.status != "available":
            print("[red]Vehicle is not available for maintenance[/red]")
            return

        maintenance.staff_id = globals.current_staff.staff_id
        maintenance.description = get_validated_input(
            "Enter maintenance description"
        )
        maintenance.maintenance_date = datetime.now()
        maintenance.cost = float(
            get_validated_input("Enter estimated cost", validate_price)
        )
        maintenance.notes = input("Enter additional notes (optional): ")

        # Update vehicle status to maintenance
        self.vehicle_repo.update_status(maintenance.vehicle_id, "maintenance")

        self.repo.add(maintenance)
        print("[green]Maintenance record added successfully[/green]")

    def complete_maintenance(self):
        print("Complete maintenance record...")

        maintenance_id = int(
            get_validated_input("Enter maintenance ID", validate_digit)
        )
        completion_date = datetime.now()

        # Update maintenance record
        self.repo.update_status(maintenance_id, "completed", completion_date)

        # Update vehicle status back to available
        maintenance = self.repo.get_by_id(maintenance_id)
        if not maintenance:
            print("[red]Maintenance record not found[/red]")
            return

        if not maintenance.vehicle_id:
            print("[red]Vehicle not found[/red]")
            return
        self.vehicle_repo.update_status(maintenance.vehicle_id, "available")

        print("[green]Maintenance record completed successfully[/green]")

    def start_maintenance(self):
        print("Start maintenance work...")

        maintenance_id = int(
            get_validated_input("Enter maintenance ID", validate_digit)
        )

        self.repo.update_status(maintenance_id, "ongoing")
        print("[green]Maintenance status updated to ongoing[/green]")

    def delete_maintenance(self):
        print("Delete maintenance record...")

        maintenance_id = int(
            get_validated_input("Enter maintenance ID", validate_digit)
        )

        self.repo.delete(maintenance_id)
        print("[green]Maintenance record deleted successfully[/green]")

    def display_maintenance_table(self, records):
        table = Table()
        table.add_column("ID")
        table.add_column("Vehicle")
        table.add_column("License Plate")
        table.add_column("Description")
        table.add_column("Date")
        table.add_column("Cost")
        table.add_column("Status")
        table.add_column("Completion Date")
        table.add_column("Notes")

        for record in records:
            table.add_row(
                str(record[0]),
                f"{record[1]} {record[2]}",  # brand + model
                record[3],  # license_plate
                record[4],  # description
                str(record[5]),  # maintenance_date
                f"${record[6]}" if record[6] else "",  # cost
                record[7],  # status
                str(record[8] or ""),  # completion_date
                record[9] or "",  # notes
            )

        console = Console()
        console.print(table)
