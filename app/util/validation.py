import datetime
import re
from decimal import Decimal, InvalidOperation

from rich import print
from rich.prompt import Prompt


def validate_digit(str):
    """Validates if the given string is digit"""
    if str.isdigit():
        return True
    return False


def validate_email(email):
    """Validates if the given email is valid"""
    if email.count("@") == 1 and email.count(".") > 0:
        return True
    return False


def validate_phone(phone):
    """Validates if the given phone is valid"""
    if phone.isdigit():
        return True
    return False


def get_validated_input(
    prompt, error, validator=None, optional=False, password=False
):
    """Validates input with validator"""
    while True:
        value = Prompt.ask(prompt, password=password)
        if optional and not value:
            return value
        if not optional and not value:
            print("[red]The value cannot be empty.[/red]")
        elif not validator or validator(value):
            return value
        else:
            print(f"[red]{error}[/red]")


def validate_price(price: str) -> bool:
    """Validates if the given price is a positive number."""
    if not re.match(r"^\d+\.\d{2}$", price):
        return False
    try:
        Decimal(price)
        return True
    except InvalidOperation:
        return False


def validate_year(year: str) -> bool:
    """Validates if the given year is a valid year between 1900 and current year + 1."""
    try:
        year_int = int(year)
        current_year = datetime.date.today().year

        if year_int < 1900 or year_int > current_year + 1:
            return False
        return True
    except ValueError:
        return False
