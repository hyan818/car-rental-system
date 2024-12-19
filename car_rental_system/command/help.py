from rich import print


class HelpCommand:
    HELP_MESSAGE = """
    Avaliable Commands:
        /staff        Manage staff information
        /customer     Manage customer information
        /vehicle      Manage vehicle information
        /rental       Manage rental information
        /maintenance  Manage maintenance information
        /?            Display this help message
        /bye          Exit the program
    """

    def handle_command(self):
        print(self.HELP_MESSAGE)
        return
