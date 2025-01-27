from command.command import Command
from globals import CurrentUser
from rich import print
from util.decorator import singleton


@singleton
class HelpCommand(Command):
    STAFF_AVAILABLE_COMMANDS = """
    Available Commands:
        /profile      View or change profile details
        /staff        Manage staff information
        /customer     Manage customer information
        /vehicle      Manage vehicle information
        /rental       Manage rental information
        /?            Display this help message
        /bye          Exit the program
    """
    CUSTOMER_AVAILABLE_COMMANDS = """
    Available Commands:
        /profile      View or change profile details
        /vehicle      View available vehicles
        /rental       View rental records or book a new one
        /?            Display this help message
        /bye          Exit the program
    """

    def __init__(self, current_user: CurrentUser) -> None:
        self.current_user = current_user

    def handle(self, command):
        if self.current_user.role_name == "customer":
            print(self.CUSTOMER_AVAILABLE_COMMANDS)
        else:
            print(self.STAFF_AVAILABLE_COMMANDS)
