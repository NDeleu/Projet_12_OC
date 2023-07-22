from app.models import Event, Support, Contract


def test_create_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test creating a new event
    new_event = Event.create(db_session, name="Conference", event_start="2023-07-22 10:00:00",
                             event_end="2023-07-22 18:00:00", location="City Hall", attendees=100,
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
    assert new_event.support is None


def test_read_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test reading an existing event from the database
    event = Event.create(db_session, name="Conference", event_start="2023-07-22 10:00:00",
                         event_end="2023-07-22 18:00:00", location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    read_event = Event.read(db_session, event.id)

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
    assert read_event.support is None


def test_update_event(db_session):
    # Create a new support for event association
    support = Support.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", password="secret")

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test updating an existing event
    event = Event.create(db_session, name="Conference", event_start="2023-07-22 10:00:00",
                         event_end="2023-07-22 18:00:00", location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    # Update the event's name and location
    event.update(db_session, name="Updated Conference", location="Convention Center", support=support)

    # Check if the name and location were updated successfully
    updated_event = Event.read(db_session, event.id)
    assert updated_event.name == "Updated Conference"
    assert updated_event.location == "Convention Center"
    assert updated_event.support == support


def test_delete_event(db_session):

    # Create a new contract for event association
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=None)

    # Test deleting an existing event
    event = Event.create(db_session, name="Conference", event_start="2023-07-22 10:00:00",
                         event_end="2023-07-22 18:00:00", location="City Hall", attendees=100,
                         instruction="Bring your IDs", contract=contract)

    # Delete the event
    event.delete(db_session)

    # Check if the event was deleted successfully
    deleted_event = Event.read(db_session, event.id)
    assert deleted_event is None




