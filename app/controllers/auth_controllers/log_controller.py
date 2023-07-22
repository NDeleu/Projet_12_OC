import re
import click
from datetime import datetime, timedelta

from .permission_controller import generate_token, save_token_to_file, \
    get_logged_as_user, clear_token_from_file
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.views.general_views.generic_message import display_message


def login_set(session):

    while True:
        email = click.prompt("Email", type=click.STRING)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message(
                "L'adresse e-mail n'est pas valide. Veuillez réessayer.")
        else:
            break

    while True:
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            display_message(
                "Password should not contain special characters. Try again.")
        elif len(password) < 6:
            display_message(
                "Password should be at least 6 characters long. Try again.")
        else:
            break

    collaborator = Collaborator.get_by_email(session, email)

    if collaborator:
        if collaborator.verify_password(password):
            token = generate_token(collaborator.id, collaborator.role)
            collaborator.token = token
            collaborator.token_expiration = datetime.utcnow() + timedelta(minutes=10)
            session.commit()
            save_token_to_file(token)
            display_message(f"Collaborator {collaborator.role} logged in successfully")
        else:
            display_message("Incorrect password for collaborator")
    else:
        display_message("User not found")


def logout_set(session):
    user = get_logged_as_user(session)

    if user:
        user.token = None
        user.token_expiration = None
        session.commit()
        clear_token_from_file()
        display_message("User logged out successfully")
    else:
        display_message("No user logged in")
