from typing import Optional

import bcrypt
from globals import CurrentUser
from repository.customers import Customers, CustomersRepository
from repository.roles import RoleRepository
from repository.users import Users, UsersRepository
from rich import print
from rich.prompt import Prompt
from util.validation import get_validated_input, validate_email


class UsersCommand:
    def __init__(self):
        self.customer_repo = CustomersRepository()
        self.users_repo = UsersRepository()
        self.roles_repo = RoleRepository()

    def handle_register_command(self):
        username = get_validated_input(
            "Enter your username",
            "The username has exist, please try again.",
            self.users_repo.username_exists,
            False,
        )

        full_name = get_validated_input(
            "Enter your full name", "Full name can not be null", False
        )
        email = get_validated_input(
            "Enter your email", "The email is not valid.", validate_email, False
        )
        phone = Prompt.ask("Enter your phone number")
        address = Prompt.ask("Enter your address")
        driver_license = get_validated_input(
            "Enter your driver license",
            "The driver license has exist.",
            self.customer_repo.driver_license_exits,
            False,
        )
        password = get_validated_input(
            "Enter your password",
            "The password is invalid",
            optional=False,
            password=True,
        )

        user = Users(username=username, password=password, role_id=2)
        user_id = self.users_repo.add_user(user)

        customer = Customers(
            full_name=full_name,
            user_id=user_id,
            email=email,
            phone=phone,
            address=address,
            driver_license=driver_license,
        )
        self.customer_repo.add_customer(customer)

        print("[green]Register successfully.[/green]")

    def handle_login_command(self) -> Optional[CurrentUser]:
        username = Prompt.ask("Enter your username")
        password = Prompt.ask("Enter your password", password=True)

        user = self.users_repo.get_by_username(username)

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode()
        ):
            if user.user_id:
                self.users_repo.update_last_login(user.user_id)
            role = self.roles_repo.get_role(user.role_id)
            if role is None:
                return None
            current_user = CurrentUser(
                user_id=user.user_id,
                username=user.username,
                role_name=role.role_name,
            )

            return current_user
        return None
