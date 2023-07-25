from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin
from app.views.class_views.collaborator_view import display_collaborator_detail, display_collaborator_summary, display_announce_collaborator_list
from app.views.general_views.generic_message import display_message_error, display_message_success


@login_required_admin
def create_func(session, user, firstname, lastname, email, role, password):
    try:
        collaborator = Collaborator.create(session, firstname, lastname, email, role, password)
        display_message_success("Collaborator created successfully.")
        display_collaborator_detail(collaborator)
    except ValueError as e:
        display_message_error(f"Error creating collaborator: {e}")


@login_required_admin
def read_func(session, user):
    try:
        list_collaborators = Collaborator.read(session)
        display_announce_collaborator_list()
        for collaborator in list_collaborators:
            display_collaborator_summary(collaborator)
    except Exception as e:
        display_message_error(f"Error reading collaborators: {e}")


@login_required_admin
def get_by_id_func(session, user, collaborator_id):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            display_collaborator_detail(collaborator)
        else:
            display_message_error("Collaborator not found.")
    except Exception as e:
        display_message_error(f"Error getting collaborator by ID: {e}")


@login_required_admin
def get_by_email_func(session, user, collaborator_email):
    try:
        collaborator = Collaborator.get_by_email(session, collaborator_email)
        if collaborator:
            display_collaborator_detail(collaborator)
        else:
            display_message_error("Collaborator not found.")
    except Exception as e:
        display_message_error(f"Error getting collaborator by email: {e}")


@login_required_admin
def update_func(session, user, collaborator_id, firstname, lastname, email, password):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            collaborator.update(session, firstname=firstname, lastname=lastname, email=email, password=password)
            display_message_success("Collaborator updated successfully.")
            display_collaborator_detail(collaborator)
        else:
            display_message_error("Collaborator not found.")
    except ValueError as e:
        display_message_error(f"Error updating collaborator: {e}")


@login_required_admin
def delete_func(session, user, collaborator_id):
    try:
        collaborator = Collaborator.get_by_id(session, collaborator_id)
        if collaborator:
            collaborator.delete(session)
            display_message_success("Collaborator deleted successfully.")
        else:
            display_message_error("Collaborator not found.")
    except Exception as e:
        display_message_error(f"Error deleting collaborator: {e}")
