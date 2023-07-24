import click
from app.models.class_models.business_models.event_model import Event
from app.controllers.auth_controllers.permission_controller import login_required_admin_or_support, login_required_with_role
from app.views.class_views.event_view import display_event
from app.views.general_views.generic_message import display_message






@login_required_with_role
def read_events(session, user_role, user_id, supported, mine):

    if user_role == 'support' and mine is True:
        events = Event.read(session, user_id=user_id, supported=supported)
        if events:
            for event in events:
                display_event(event)
        else:
            display_message("No events found")

    else:
        events = Event.read(session, user_id=None, supported=supported)
        if events:
            for event in events:
                display_event(event)
        else:
            display_message("No events found")
