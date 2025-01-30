# Car Rental System

Car Rental System is a CLI (Command line interface) application which can help customers to rent cars and staffs to manage car rental information easily.

# Feature Overview

When you run this application, it offers different features for two user roles: customer and staff. If you get stuck, you can run `/?` to get help message.

## Customer features

```bash
/register     # Register a new customer account
/login        # Login into the system

# Available commands after login
/profile      # View or change profile details
/vehicle      # View available vehicles
/rental       # View rental records or book a new one
/?            # Display help message
/bye          # Exit the program
```

## Staff features

```bash
/login        # Login into the system

# Available commands after login
/profile      # View or change profile details
/staff        # Manage staff information
/customer     # Manage customer information
/vehicle      # Manage vehicle information
/rental       # Manage rental information
/?            # Display help message
/bye          # Exit the program
```

# Local Development Setup

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run
python app/main.py
```

# Dependencies

For making this project as simple as possible, I only use a few dependencies to build this project.

- [rich](https://pypi.org/project/rich/): Make output format beautiful in terminal
- [bcrypt](https://pypi.org/project/bcrypt/): Encrypt the user's password
- [pytest](https://pypi.org/project/pytest/): Unit Test
- [pyinstaller](https://pypi.org/project/pyinstaller/): Build packages for different OS
