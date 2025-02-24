# Car Rental System

Car Rental System is a CLI (Command line interface) application which can help customers to rent cars and staffs to manage car rental information easily.

**❗️Important: This project uses SQLite to store data. When you run this project, it will create a `crs.db` file, which is a SQLite database file. If you delete this file, you will lose all data.**

# Project Structure

```bash
car-rental-system/          # Root directory of the car rental system project
│
├── app/                    # Main application folder containing all business logic
│   ├── command/            # Classes that handle commands
│   ├── db/                 # Database schema definitions and database access classes
│   ├── repository/         # Data access layer (repositories for handling CRUD)
│   └── util/               # Utility functions
├── doc/                    # Project documentation
└── tests/                  # Unit tests
```

# Local Development Setup

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate  # macOS/Linux
.venv\bin\activate     # Windows

# Install packages
pip install -r requirements.txt

# Run
python app/main.py
```

# Feature Overview

When you run this application, it offers different features for two user roles: customer and staff. If you get stuck, you can run `/?` to get help message.

**If you want to cancel input, press `Ctrl+C` (Press `Ctrl+C` can not exit program, please use `/bye` command instead.)**

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

## Subcommand details

When you enter command like `/vehicle`, it will display available subcommands you can use.

![subcommand_example](doc/subcommand_example.png)

# Dependencies

For making this project as simple as possible, I only use a few dependencies to build this project.

- [rich](https://pypi.org/project/rich/): Make output format beautiful in terminal
- [bcrypt](https://pypi.org/project/bcrypt/): Encrypt the user's password
- [pytest](https://pypi.org/project/pytest/): Unit Test
- [pyinstaller](https://pypi.org/project/pyinstaller/): Build packages for different OS
