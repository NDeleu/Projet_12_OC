from app.models import Event, Collaborator, Contract
from datetime import datetime
import pytest


def test_create_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test creating a new event
    new_event = Event.create(db_session, name="Conference", event_start=datetime(2023, 7, 22, 10, 0, 0),
                             event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                             instruction="Bring your IDs", contract=contract)

    # Check if the event was created successfully
    assert new_event.id is not None
    assert new_event.name == "Conference"
    assert str(new_event.event_start) == "2023-07-22 10:00:00"
    assert str(new_event.event_end) == "2023-07-22 18:00:00"
    assert new_event.location == "City Hall"
    assert new_event.attendees == 100
    assert new_event.instruction == "Bring your IDs"
    assert new_event.contract == contract
    assert new_event.collaborator is None

    # Test creating a new event with invalid input (empty name)
    with pytest.raises(ValueError, match="Name cannot be empty."):
        Event.create(db_session, name="", event_start=datetime(2023, 7, 22, 10, 0, 0),
                     event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                     instruction="Bring your IDs", contract=contract)


def test_read_events(db_session):
    # Test reading events from the database with optional filters

    # Create a new contract for event association
    contract1 = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)
    contract2 = Contract.create(db_session, total_amount=1500.0, left_to_pay=750.0, customer=None)

    # Create some events with and without collaborators
    event1 = Event.create(db_session, name="Conference1", event_start=datetime(2023, 7, 22, 10, 0, 0),
                          event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                          instruction="Bring your IDs", contract=contract1)

    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith",
                                       email="jane.smith@example.com", role=3, password="secret")

    event2 = Event.create(db_session, name="Conference2", event_start=datetime(2023, 7, 22, 10, 0, 0),
                          event_end=datetime(2023, 7, 22, 18, 0, 0), location="Convention Center", attendees=200,
                          instruction="Bring your badges", contract=contract2, collaborator=collaborator)

    # Test reading all events
    all_events = Event.read(db_session)
    assert len(all_events) == 2

    # Test reading events associated with a specific collaborator
    events_with_collaborator = Event.read(db_session, user_id=collaborator.id)
    assert len(events_with_collaborator) == 1
    assert events_with_collaborator[0] == event2

    # Test reading events with collaborators
    events_with_support = Event.read(db_session, is_supported=True)
    assert len(events_with_support) == 1
    assert events_with_support[0] == event2

    # Test reading events without collaborators
    events_without_support = Event.read(db_session, is_supported=False)
    assert len(events_without_support) == 1
    assert events_without_support[0] == event1

    # Test reading events with an invalid value for is_supported (not a boolean)
    with pytest.raises(TypeError, match="Is_supported must be either True, False, or None."):
        Event.read(db_session, is_supported="invalid_value")


def test_get_by_id_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test reading an existing event from the database
    event = Event.create(db_session, name="Conference", event_start=datetime(2023, 7, 22, 10, 0, 0),
                         event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    read_event = Event.get_by_id(db_session, event.id)

    # Check if the read operation returns the correct event
    assert read_event is not None
    assert read_event.id == event.id
    assert read_event.name == "Conference"
    assert str(read_event.event_start) == "2023-07-22 10:00:00"
    assert str(read_event.event_end) == "2023-07-22 18:00:00"
    assert read_event.location == "City Hall"
    assert read_event.attendees == 100
    assert read_event.instruction == "Bring your IDs"
    assert read_event.contract == contract
    assert read_event.collaborator is None

    # Test reading an event with an invalid event_id (non-existent event_id)
    non_existent_event_id = 999
    event = Event.get_by_id(db_session, non_existent_event_id)
    assert event is None


def test_update_event(db_session):
    # Create a new support for event association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=3, password="secret")

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test updating an existing event
    event = Event.create(db_session, name="Conference", event_start=datetime(2023, 7, 22, 10, 0, 0),
                         event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    # Update the event's name and location
    event.update(db_session, name="Updated Conference", location="Convention Center", collaborator=collaborator)

    # Check if the name and location were updated successfully
    updated_event = Event.get_by_id(db_session, event.id)
    assert updated_event.name == "Updated Conference"
    assert updated_event.location == "Convention Center"
    assert updated_event.collaborator == collaborator

    # Test updating an existing event with invalid collaborator (non-support collaborator)
    invalid_collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe",
                                               email="john.doe@example.com", role=2, password="secret")
    with pytest.raises(PermissionError, match="Only collaborators with the role of 'support' can be linked to a customer."):
        event.update(db_session, collaborator=invalid_collaborator)


def test_delete_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test deleting an existing event
    event = Event.create(db_session, name="Conference", event_start=datetime(2023, 7, 22, 10, 0, 0),
                         event_end=datetime(2023, 7, 22, 18, 0, 0), location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    # Delete the event
    event.delete(db_session)

    # Check if the event was deleted successfully
    deleted_event = Event.get_by_id(db_session, event.id)
    assert deleted_event is None




