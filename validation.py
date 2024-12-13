from rich import print
from rich.prompt import Prompt


def validate_id(id):
    if id.isdigit():
        return True
    return False


def validate_email(email):
    if email.count("@") == 1 and email.count(".") > 0:
        return True
    return False


def validate_phone(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    pass


def get_validated_input(prompt, validator=None):
    while True:
        value = Prompt.ask(prompt)
        if not validator or validator(value):
            return value
        print("Invalid input. Please try again.")
