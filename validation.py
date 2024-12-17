import datetime

from rich import print
from rich.prompt import Prompt


def validate_digit(id):
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


def get_validated_input(prompt, validator=None, optional=False):
    while True:
        value = Prompt.ask(prompt)
        if optional and not value:
            return ""
        if not validator or validator(value):
            return value
        print("Invalid input. Please try again.")


def validate_price(price: str) -> bool:
    """
    Validates if the given price is a positive number.

    Args:
        price: String representing a price value

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_price("50.00")
        True
        >>> validate_price("-10.00")
        False
        >>> validate_price("abc")
        False
    """
    try:
        price_float = float(price)
        if price_float <= 0:
            print("[red]Price must be greater than 0[/red]")
            return False
        return True
    except ValueError:
        print("[red]Price must be a valid number[/red]")
        return False


def validate_year(year: str) -> bool:
    """
    Validates if the given year is a valid year between 1900 and current year + 1.

    Args:
        year: String representing a year

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_year("2023")
        True
        >>> validate_year("1899")
        False
        >>> validate_year("abc")
        False
    """
    try:
        year_int = int(year)
        current_year = datetime.date.today().year

        if year_int < 1900 or year_int > current_year + 1:
            print(
                f"[red]Year must be between 1900 and {current_year + 1}[/red]"
            )
            return False
        return True
    except ValueError:
        print("[red]Year must be a valid number[/red]")
        return False
