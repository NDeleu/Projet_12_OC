import re
import click
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin
from app.views.class_views.collaborator_view import display_collaborator
from app.views.general_views.generic_message import display_message


@login_required_admin
def create_collaborator(session):
    while True:
        firstname = click.prompt("firstname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', firstname):
            display_message("firstname should not contain special characters. Try again.")
        else:
            break

    while True:
        lastname = click.prompt("Lastname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
            display_message("Lastname should not contain special characters. Try again.")
        else:
            break

    while True:
        email = click.prompt("Email", type=click.STRING)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
        else:
            break

    while True:
        try:
            display_message(
                "Select: 1 for administrator, 2 for seller, 3 for support")
            role = click.prompt("Role", type=click.INT)
            if role not in [1, 2, 3]:
                display_message(
                    "Invalid input. Please choose a valid role :  1, 2, or 3.")
            else:
                break
        except click.BadParameter:
            display_message(
                "Invalid input. Please enter a valid role : 1, 2, or 3.")

    while True:
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            display_message("Password should not contain special characters. Try again.")
        elif len(password) < 6:
            display_message("Password should be at least 6 characters long. Try again.")
        else:
            break

    try:
        collaborator = Collaborator.create(session, firstname, lastname, email, role, password)
        display_message(f"Collaborator created: {collaborator}")
    except ValueError as e:
        display_message(str(e))


@login_required_admin
def read_collaborator(session, collaborator_id):
    collaborator = Collaborator.read(session, collaborator_id)
    if collaborator:
        display_collaborator(collaborator)
    else:
        display_message("Collaborator not found")


@login_required_admin
def update_collaborator(session, collaborator_id, firstname, lastname, email):
    collaborator = Collaborator.read(session, collaborator_id)
    if collaborator:
        # Validate the inputs for firstname and lastname
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', firstname):
            display_message("firstname should not contain special characters. Try again.")
            return

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
            display_message("Lastname should not contain special characters. Try again.")
            return

        # Validate the input for email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
            return

        # Update the collaborator's information if any updates provided
        kwargs = {'firstname': firstname, 'lastname': lastname, 'email': email}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            collaborator.update(session, **kwargs)
            display_message("Collaborator updated")
        else:
            display_message("No updates provided")
    else:
        display_message("Collaborator not found")



@login_required_admin
def delete_collaborator(session, collaborator_id):
    collaborator = Collaborator.read(session, collaborator_id)
    if collaborator:
        collaborator.delete(session)
        display_message("Collaborator deleted")
    else:
        display_message("Collaborator not found")
