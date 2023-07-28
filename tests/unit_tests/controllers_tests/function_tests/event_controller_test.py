from app.controllers.business_controllers.event_controllers.event_controller import (
    create_func,
    read_func,
    get_by_id_func,
    update_func,
    delete_func,
)
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from unittest.mock import patch
import pytest
from datetime import datetime


@pytest.fixture
def contracts(db_session, seller_user):

    # Create one more seller_user instance of customer
    other_seller_user = Collaborator(firstname="OtherSeller", lastname="OtherUser", email="other.seller@example.com", role=2, password="password")
    db_session.add(other_seller_user)

    # Create two Customer instances for Contract set up
    customer1 = Customer(firstname="Jean", lastname="Dupont", email="jean.dupont@exemple.com", phone="1234567890", company="La super boutique", collaborator=seller_user)
    db_session.add(customer1)

    customer2 = Customer(firstname="Adrien", lastname="Lepuit", email="adrien.lepuit@exemple.com", phone="2134567890", company="Le super stock", collaborator=other_seller_user)
    db_session.add(customer1)

    # Create four Contract instances
    contract1 = Contract(total_amount=1000.0, left_to_pay=0, customer=customer1, signed=True)
    db_session.add(contract1)

    contract2 = Contract(total_amount=1500.0, left_to_pay=0, customer=customer1, signed=True)
    db_session.add(contract2)

    contract3 = Contract(total_amount=1500.0, left_to_pay=0, customer=customer2, signed=True)
    db_session.add(contract3)

    contract4 = Contract(total_amount=1500.0, left_to_pay=500.0, customer=customer1, signed=False)
    db_session.add(contract4)

    db_session.commit()

    return contract1, contract2, contract3, contract4


def test_event_create_good_contract_func(db_session, contracts, seller_user, capsys):
    # Test data
    name = "Test Event"
    event_start = datetime(2023, 7, 26, 10, 0)
    event_end = datetime(2023, 7, 26, 14, 0)
    location = "Test Location"
    attendees = 50
    instruction = "Test Instruction"

    contract1, contract2, contract3, contract4 = contracts



    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Run the function
        create_func(db_session, name, event_start, event_end, location, attendees, instruction, contract1.id)

    captured_stdout = capsys.readouterr().out

    # Verify that the event was created in the database
    event = db_session.query(Event).filter(Event.name == name).first()
    assert event is not None
    assert event.name == name
    assert event.event_start == event_start
    assert event.event_end == event_end
    assert event.location == location
    assert event.attendees == attendees
    assert event.instruction == instruction
    assert event.contract_id == contract1.id
    assert event.collaborator is None

    assert "Event created successfully." in captured_stdout


def test_event_create_wrong_contract_1_func(db_session, contracts, seller_user, capsys):
    # Test data
    name = "Test Event"
    event_start = datetime(2023, 7, 26, 10, 0)
    event_end = datetime(2023, 7, 26, 14, 0)
    location = "Test Location"
    attendees = 50
    instruction = "Test Instruction"

    contract1, contract2, contract3, contract4 = contracts


    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Run the function
        create_func(db_session, name, event_start, event_end, location, attendees, instruction, contract4.id)

    captured_stdout = capsys.readouterr().out

    assert "The contract is not signed. It must be signed to create a relative event." in captured_stdout


def test_event_create_wrong_contract_2_func(db_session, contracts, seller_user, capsys):
    # Test data
    name = "Test Event"
    event_start = datetime(2023, 7, 26, 10, 0)
    event_end = datetime(2023, 7, 26, 14, 0)
    location = "Test Location"
    attendees = 50
    instruction = "Test Instruction"

    contract1, contract2, contract3, contract4 = contracts

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Run the function
        create_func(db_session, name, event_start, event_end, location, attendees, instruction, contract3.id)

    captured_stdout = capsys.readouterr().out

    assert "The user is not the seller assigned to this contract. Only the designated seller can create an event relating to this contract." in captured_stdout


def test_event_read_as_support_func(db_session, contracts, support_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event1 = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0), event_end=datetime(2023, 7, 26, 14, 0), location="Test Location 1", attendees=50, instruction="Test Instruction 1", contract=contract1, collaborator=support_user)
    event2 = Event(name="Event Two", event_start=datetime(2023, 8, 26, 10, 0), event_end=datetime(2023, 8, 26, 14, 0), location="Test Location 2", attendees=70, instruction="Test Instruction 2", contract=contract2, collaborator=support_user)
    db_session.add_all([event1, event2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        read_func(db_session, mine=True, is_supported=None)

    captured_stdout = capsys.readouterr().out

    assert f"{event1.name}" in captured_stdout
    assert f"{event2.name}" in captured_stdout


def test_event_read_as_other_func(db_session, contracts, admin_user, support_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event1 = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location 1", attendees=50,
                   instruction="Test Instruction 1", contract=contract1,
                   collaborator=support_user)
    event2 = Event(name="Event Two", event_start=datetime(2023, 8, 26, 10, 0),
                   event_end=datetime(2023, 8, 26, 14, 0),
                   location="Test Location 2", attendees=70,
                   instruction="Test Instruction 2", contract=contract2,
                   collaborator=support_user)
    db_session.add_all([event1, event2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        read_func(db_session, mine=True, is_supported=None)

    captured_stdout = capsys.readouterr().out

    assert f"{event1.name}" in captured_stdout
    assert f"{event2.name}" in captured_stdout

    assert "Permission denied. Please log in as a support to access the mine option for events. The full list of events is selected instead." in captured_stdout

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        read_func(db_session, mine=False, is_supported=True)

    captured_stdout = capsys.readouterr().out

    assert f"{event1.name}" in captured_stdout
    assert f"{event2.name}" in captured_stdout


def test_event_get_by_id_func(db_session, contracts, support_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0),
                  location="Test Location 1", attendees=50,
                  instruction="Test Instruction 1", contract=contract1,
                  collaborator=support_user)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        get_by_id_func(db_session, event.id)

    captured_stdout = capsys.readouterr().out

    assert f"{event.name}" in captured_stdout

    wrong_event_id = 250
    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        get_by_id_func(db_session, wrong_event_id)

    captured_stdout = capsys.readouterr().out

    assert "Event not found." in captured_stdout


def test_event_update_as_support_func(db_session, contracts, support_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0),
                  location="Test Location 1", attendees=50,
                  instruction="Test Instruction 1", contract=contract1,
                  collaborator=support_user)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        new_name = "Updated Event"
        new_event_start = datetime(2023, 7, 27, 12, 0)
        new_event_end = datetime(2023, 7, 27, 16, 0)
        new_location = "Updated Location"
        new_attendees = 100
        new_instruction = "Updated Instruction"
        new_contract = contract2.id
        new_collaborator = None
        update_func(db_session, event.id, new_name,
                    new_event_start, new_event_end, new_location,
                    new_attendees, new_instruction, new_contract, new_collaborator)

    captured_stdout = capsys.readouterr().out

    # Verify that the event's data was updated in the database
    updated_event = db_session.query(Event).filter(
        Event.id == event.id).first()
    assert updated_event is not None
    assert updated_event.name == new_name
    assert updated_event.event_start == new_event_start
    assert updated_event.event_end == new_event_end
    assert updated_event.location == new_location
    assert updated_event.attendees == new_attendees
    assert updated_event.instruction == new_instruction
    assert updated_event.contract_id == contract2.id
    assert updated_event.collaborator_id == support_user.id

    assert "Fields have been updated but not the support field as only Administrator has permission." in captured_stdout


def test_event_update_as_admin_func(db_session, contracts, support_user, admin_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0),
                  location="Test Location 1", attendees=50,
                  instruction="Test Instruction 1", contract=contract1,
                  collaborator=None)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Run the function
        new_name = "Updated Event"
        new_event_start = datetime(2023, 7, 27, 12, 0)
        new_event_end = datetime(2023, 7, 27, 16, 0)
        new_location = "Updated Location"
        new_attendees = 100
        new_instruction = "Updated Instruction"
        new_contract = contract2.id
        new_collaborator = support_user.id
        update_func(db_session, event.id, new_name,
                    new_event_start, new_event_end, new_location,
                    new_attendees, new_instruction, new_contract,
                    new_collaborator)

    captured_stdout = capsys.readouterr().out

    # Verify that the event's data was updated in the database
    updated_event = db_session.query(Event).filter(
        Event.id == event.id).first()
    assert updated_event is not None
    assert updated_event.name == event.name
    assert updated_event.event_start == event.event_start
    assert updated_event.event_end == event.event_end
    assert updated_event.location == event.location
    assert updated_event.attendees == event.attendees
    assert updated_event.instruction == event.instruction
    assert updated_event.contract_id == event.contract_id
    assert updated_event.collaborator_id == support_user.id

    assert "Support field has been updated but CARE : administrator can only update event support field. Any other changes will be ignored." in captured_stdout


def test_delete_func(db_session, contracts, support_user, capsys):

    # Set contracts for create event
    contract1, contract2, contract3, contract4 = contracts

    # Test data
    event = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0),
                  location="Test Location 1", attendees=50,
                  instruction="Test Instruction 1", contract=contract1,
                  collaborator=support_user)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        delete_func(db_session, event.id)

    captured_stdout = capsys.readouterr().out

    # Verify that the event was deleted from the database
    deleted_event = db_session.query(Event).filter(
        Event.id == event.id).first()
    assert deleted_event is None

    assert "Event deleted successfully." in captured_stdout