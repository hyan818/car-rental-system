from rich import print


class HelpCommand:
    HELP_MESSAGE = """
    Avaliable Commands:
        /customer   Manage customers' information
        /car        Manage cars' information
    """

    def handle_command(self):
        print(self.HELP_MESSAGE)
        return
