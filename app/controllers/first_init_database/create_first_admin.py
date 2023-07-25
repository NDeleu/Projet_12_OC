import sys
import re

from sqlalchemy.exc import SQLAlchemyError

from app.models import Collaborator
from app.models import session
from app.views.general_views.generic_message import display_message_error, display_message_info, display_message_success


def ask_to_create_admin():
    while True:
        display_message_info("Currently, no administrator exists on the database. You need at least one to use the app. Do you want to create an administrator now ?")
        try:
            display_message_info("Choice select in numerical value: for Yes: 1, for No: 2.")
            ask_select_choice = int(input("Choice"))
            if ask_select_choice == 1:
                answer_create_choice = True
                break
            elif ask_select_choice == 2:
                answer_create_choice = False
                break
            else:
                display_message_error("Invalid choice. Please try again.")
        except ValueError:
            display_message_error("Invalid input. Please enter a valid choice.")

    return answer_create_choice


def form_first_admin():
    while True:
        display_message_info("Enter the firstname of the first administrator in alphabetical value: ")
        firstname = str(input("Administrator Firstname"))
        if not firstname.isalpha():
            display_message_error("Firstname should only contain alphabetic characters. Please try again.")
        else:
            break

    while True:
        display_message_info("Enter the lastname of the first administrator in alphabetical value: ")
        lastname = str(input("Administrator Lastname"))
        if not lastname.isalpha():
            display_message_error("Lastname should only contain alphabetic characters. Please try again.")
        else:
            break

    while True:
        display_message_info("Enter the email address of the first administrator in alphabetical value in form alpha@alpha.alpha: ")
        email = input("Administrator Email")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message_error("Email address is not valid. Please try again.")
        else:
            break

    role = 1

    while True:
        display_message_info("Enter the password for the first administrator: ")
        password = str(input("Administrator Password"))
        if len(password) < 6:
            display_message_error("Password should be at least 6 characters long. Please try again.")
        elif not re.match("^[a-zA-Z0-9!@#$%^&*()_-]+$", password):
            display_message_error("Invalid input. Please enter a non-empty password containing only letters, numbers, and a limited set of special characters (!@#$%^&*()_-). Please try again.")
        else:
            break

    return firstname, lastname, email, role, password


def create_first_administrator():
    if ask_to_create_admin():
        surname, lastname, email, role, password = form_first_admin()
        try:
            collaborator = Collaborator.create(session, surname, lastname, email, role, password)
            display_message_success(f"Administrator created: {collaborator}.")
        except SQLAlchemyError as e:
            display_message_error(str(e))
    else:
        display_message_info("Come back to create the first admin later.")
        sys.exit(1)
