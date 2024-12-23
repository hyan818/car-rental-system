import pytest

from car_rental_system.util.validation import (
    validate_digit,
    validate_email,
    validate_phone,
    validate_price,
    validate_year,
)


@pytest.mark.parametrize(
    "str,expected",
    [
        ("1", True),
        ("-1", False),
        ("abc", False),
        ("12.3", False),
        ("", False),
        ("123abc", False),
    ],
)
def test_validate_digit(str, expected):
    assert validate_digit(str) == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("test@example.com", True),
        ("invalid.email", False),
        ("test@multiple@at.com", False),
        ("", False),
        ("test@nodot", False),
    ],
)
def test_validate_email(email, expected):
    assert validate_email(email) == expected


@pytest.mark.parametrize(
    "phone,expected",
    [
        ("1234567890", True),
        ("123456789", False),
        ("12345678901", False),
        ("abcdefghij", False),
        ("", False),
    ],
)
def test_validate_phone(phone, expected):
    assert validate_phone(phone) == expected


def test_validate_year():
    import datetime

    current_year = datetime.date.today().year

    assert validate_year(str(current_year)) is True
    assert validate_year("1950") is True
    assert validate_year("1899") is False  # Too early
    assert validate_year(str(current_year + 2)) is False  # Too far in future
    assert validate_year("abc") is False
    assert validate_year("") is False


@pytest.mark.parametrize(
    "price,expected",
    [
        ("100", False),
        ("100.00", True),
        ("1.2.3", False),
        ("abc", False),
        ("12b", False),
        ("100.0023", False),
        ("-1", False),
    ],
)
def test_validate_price(price, expected):
    assert validate_price(price) == expected
