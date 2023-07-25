import re
from datetime import datetime, timedelta

from .permission_controller import generate_token, save_token_to_file, \
    clear_token_from_file, login_required
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.views.general_views.generic_message import display_message_success, display_message_error


def login_func(session, email, password):
    try:
        if not email:
            raise ValueError("Email cannot be empty.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        if not password:
            raise ValueError("Invalid input. Password cannot be empty.")
        if not password.strip():
            raise ValueError("Invalid input. Password cannot be empty.")
        if not re.match("^[a-zA-Z0-9!@#$%^&*()_-]+$", password):
            raise ValueError("Invalid input. Please enter a non-empty password containing only letters, numbers, and a limited set of special characters (!@#$%^&*()_-).")

        collaborator = Collaborator.get_by_email(session, email)

        if collaborator:
            if collaborator.verify_password(password):
                token = generate_token(collaborator.id, collaborator.role)
                collaborator.token = token
                collaborator.token_expiration = datetime.utcnow() + timedelta(minutes=10)
                session.commit()
                save_token_to_file(token)
                display_message_success(f"Collaborator {collaborator.role} logged in successfully")
            else:
                display_message_error("Incorrect password for collaborator")
        else:
            display_message_error("User not found")
    except ValueError as ve:
        display_message_error(str(ve))


@login_required
def logout_func(session, user):

    if user:
        user.token = None
        user.token_expiration = None
        session.commit()
        clear_token_from_file()
        display_message_success("User logged out successfully")
    else:
        display_message_error("No user logged in")
