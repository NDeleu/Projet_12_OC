from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin
from app.views.class_views.collaborator_view import display_collaborator
from app.views.general_views.generic_message import display_message


@login_required_admin
def create_func(session, user, firstname, lastname, email, role, password):
    try:
        collaborator = Collaborator.create(session, firstname, lastname, email, role, password)
        display_collaborator(collaborator)
    except ValueError as e:
        display_message(f"Error creating collaborator: {e}")


@login_required_admin
def read_func(session, user):
    try:
        list_collaborators = Collaborator.read(session)
        for collaborator in list_collaborators:
            display_collaborator(collaborator)
    except Exception as e:
        display_message(f"Error reading collaborators: {e}")


@login_required_admin
def get_by_id_func(session, user, collaborator_id):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            display_collaborator(collaborator)
        else:
            display_message("Collaborator not found.")
    except Exception as e:
        display_message(f"Error getting collaborator by ID: {e}")


@login_required_admin
def get_by_email_func(session, user, collaborator_email):
    try:
        collaborator = Collaborator.get_by_email(session, collaborator_email)
        if collaborator:
            display_collaborator(collaborator)
        else:
            display_message("Collaborator not found.")
    except Exception as e:
        display_message(f"Error getting collaborator by email: {e}")


@login_required_admin
def update_func(session, user, collaborator_id, firstname, lastname, email, password):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            collaborator.update(session, firstname=firstname, lastname=lastname, email=email, password=password)
            display_collaborator(collaborator)
        else:
            display_message("Collaborator not found.")
    except ValueError as e:
        display_message(f"Error updating collaborator: {e}")


@login_required_admin
def delete_func(session, user, collaborator_id):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            collaborator.delete(session)
            display_message("Collaborator deleted successfully.")
        else:
            display_message("Collaborator not found.")
    except Exception as e:
        display_message(f"Error deleting collaborator: {e}")
