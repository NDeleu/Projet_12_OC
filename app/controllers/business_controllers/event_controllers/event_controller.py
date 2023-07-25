from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin_or_support, login_required_seller, login_required, login_required_support
from app.views.class_views.event_view import display_event_detail, display_event_summary, display_announce_event_list
from app.views.general_views.generic_message import display_message_error, display_message_success, display_message_correction


@login_required_seller
def create_func(session, user, name, event_start, event_end, location, attendees, instruction, contract):
    try:
        contract_instance = Contract.get_by_id(session, contract)
        if contract_instance:
            if contract_instance.signed:
                if contract_instance.customer.collaborator_id == user.id:
                    event = Event.create(session, name, event_start, event_end, location, attendees, instruction, contract,)
                    display_message_success("Event created successfully.")
                    display_event_detail(event)
                else:
                    display_message_error("The user is not the seller assigned to this contract. Only the designated seller can create an event relating to this contract.")
            else:
                display_message_error("The contract is not signed. It must be signed to create a relative event.")
        else:
            display_message_error("Contract not found.")
    except ValueError as e:
        display_message_error(f"Error creating collaborator: {e}")


@login_required
def read_func(session, user, mine, is_supported):
    try:
        if mine:
            if user.role == 'support':
                list_events = Event.read(session, user.id, is_supported=is_supported)
            else:
                display_message_correction("Permission denied. Please log in as a support to access the mine option for events. The full list of events is selected instead.")
                list_events = Event.read(session, is_supported=is_supported)
        else:
            list_events = Event.read(session, is_supported=is_supported)

        display_announce_event_list()
        for event in list_events:
            display_event_summary(event)
    except Exception as e:
        display_message_error(f"Error reading events: {e}")


@login_required
def get_by_id_func(session, user, event_id):
    try:
        event = Event.get_by_id(session, event_id)
        if event:
            display_event_detail(event)
        else:
            display_message_error("Event not found.")
    except Exception as e:
        display_message_error(f"Error getting collaborator by ID: {e}")


@login_required_admin_or_support
def update_func(session, user, event_id, name, event_start, event_end, location, attendees, instruction, contract, support):
    try:
        event = Event.get_by_id(session, event_id)
        if event:
            if user.role == "administrator":
                if support is not None:
                    support_collaborator = Collaborator.get_by_id(session, support)
                    if support_collaborator and support_collaborator.role == Collaborator.RoleEnum.support:
                        event.update(session, collaborator=support_collaborator)
                        display_message_correction("Support field has been updated but CARE : administrator can only update event support field. Any other changes will be ignored.")
                    else:
                        display_message_error("Invalid support ID. Please provide a valid support collaborator.")
                else:
                    display_message_error("Administrator can only update event support field. Any other changes will be ignored.")
            else:
                if user.role == "support":
                    if event.collaborator:
                        if event.collaborator_id == user.id:
                            event.update(session, name=name, event_start=event_start,
                                         event_end=event_end, location=location,
                                         attendees=attendees, instruction=instruction,
                                         contract=contract)
                            display_message_correction("Fields have been updated but not the support field as only Administrator has permission.")
                        else:
                            display_message_error("The user is not the support assigned to this event. Only designated support can update these fields.")
                    else:
                        display_message_error("The event has no assigned support. Only designated support can update these fields.")
            display_event_detail(event)
        else:
            display_message_error("Event not found.")
    except ValueError as e:
        display_message_error(f"Error updating collaborator: {e}")


@login_required_support
def delete_func(session, user, event_id):
    try:
        event = Event.get_by_id(session, event_id)
        if event:
            event.delete(session)
            display_message_success("Event deleted successfully.")
        else:
            display_message_error("Event not found.")
    except Exception as e:
        display_message_error(f"Error deleting collaborator: {e}")
