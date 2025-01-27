from typing import Optional

from command.command import Command
from command.customers import CustomerCommand
from command.help import HelpCommand
from command.profile import ProfileCommand
from command.rentals import RentalCommand
from command.staff import StaffCommand
from command.vehicles import VehicleCommand
from rich import print


class CommandFactory:
    @staticmethod
    def get_command(type: str, current_user) -> Optional[Command]:
        if type == "/?":
            return HelpCommand(current_user)
        elif type.startswith("/customer"):
            return CustomerCommand(current_user)
        elif type.startswith("/staff"):
            return StaffCommand(current_user)
        elif type.startswith("/vehicle"):
            return VehicleCommand(current_user)
        elif type.startswith("/rental"):
            return RentalCommand(current_user)
        elif type.startswith("/profile"):
            return ProfileCommand(current_user)
        else:
            print(f"[red]Unknown command: {type}[/red]")
