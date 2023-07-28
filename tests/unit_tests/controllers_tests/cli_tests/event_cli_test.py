from click.testing import CliRunner
import re
from app.controllers.business_controllers.event_controllers.event_cli import event, eventform
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from datetime import datetime
from unittest.mock import patch
import pytest



@pytest.fixture
def contracts(db_session, seller_user):

    # Create a Customer instance for Contract set up
    customer1 = Customer(firstname="Jean", lastname="Dupont", email="jean.dupont@exemple.com", phone="1234567890", company="La super boutique", collaborator=seller_user)
    db_session.add(customer1)

    # Create four Contract instances
    contract1 = Contract(total_amount=1000.0, left_to_pay=0, customer=customer1, signed=True)
    db_session.add(contract1)

    contract2 = Contract(total_amount=1500.0, left_to_pay=0, customer=customer1, signed=True)
    db_session.add(contract2)

    db_session.commit()

    return contract1, contract2


# Fonction pour supprimer les séquences d'échappement ANSI
def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def test_event_api_cli_create(db_session, contracts, seller_user):
    runner = CliRunner()

    # Test data
    name = "Test Event"
    event_start = "2023/07/26-10:00:00"
    event_end = "2023/07/26-14:00:00"
    location = "Test Location"
    attendees = "50"
    instruction = "Test Instruction"

    event_start_compared = "2023-07-26 10:00:00"
    event_end_compared = "2023-07-26 14:00:00"

    contract1, contract2 = contracts

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(event, ['create', name, event_start, event_end, location, attendees, instruction, str(contract1.id)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    # Check if the success message is displayed in the output
    assert "Event created successfully" in stripped_output

    assert f"{name}" in stripped_output
    assert f"{event_start_compared}" in stripped_output
    assert f"{event_end_compared}" in stripped_output
    assert f"{location}" in stripped_output
    assert f"{attendees}" in stripped_output
    assert f"{instruction}" in stripped_output
    assert f"{contract1.id}" in stripped_output


def test_event_api_cli_read(db_session, contracts, admin_user, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Create two Event instances
    event1 = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)
    event2 = Event(name="Event Two", event_start=datetime(2023, 10, 26, 10, 0),
                   event_end=datetime(2023, 10, 26, 14, 0),
                   location="Test Location Two", attendees=70,
                   instruction="Test Instruction Two", contract=contract2,
                   collaborator=support_user)

    db_session.add_all([event1, event2])
    db_session.commit()

    event1_start_compared = "2023-07-26 10:00:00"
    event1_end_compared = "2023-07-26 14:00:00"
    event2_start_compared = "2023-10-26 10:00:00"
    event2_end_compared = "2023-10-26 14:00:00"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(event, ['read', '--mine=False', '--is_supported=True'], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    # Verify that both contracts are listed
    assert f"{event1.id}" in stripped_output.replace("\n", "")
    assert f"{event2.id}" in stripped_output.replace("\n", "")


def test_event_api_cli_get_by_id(db_session, contracts, support_user, admin_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    event_start_compared = "2023-07-26 10:00:00"
    event_end_compared = "2023-07-26 14:00:00"

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(event, ['getbyid', str(event_instance.id)],
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    assert f"{event_instance.id}" in stripped_output
    assert f"{event_start_compared}" in stripped_output
    assert f"{event_end_compared}" in stripped_output
    assert f"{event_instance.location}" in stripped_output
    assert f"{event_instance.attendees}" in stripped_output
    assert f"{event_instance.instruction}" in stripped_output


def test_event_api_cli_update(db_session, contracts, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        new_name = "Test Event"
        new_event_start = "2020/05/25-09:00:00"
        new_event_end = "2020/05/25-12:00:00"
        new_location = "Test Location"
        new_attendees = "80"
        new_instruction = "Test Instruction"
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(event, ['update',
                                          str(event_instance.id),
                                          f"--name={new_name}",
                                          f"--event_start={new_event_start}",
                                          f"--event_end={new_event_end}",
                                          f"--location={new_location}",
                                          f"--attendees={new_attendees}",
                                          f"--instruction={new_instruction}"],
                               obj=db_session
                               )

    new_event_start_compared = "2020-05-25 09:00:00"
    new_event_end_compared = "2020-05-25 12:00:00"

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    assert f"{new_name}" in stripped_output
    assert f"{new_event_start_compared}" in stripped_output
    assert f"{new_event_end_compared}" in stripped_output
    assert f"{new_location}" in stripped_output
    assert f"{new_attendees}" in stripped_output
    assert f"{new_instruction}" in stripped_output


def test_event_api_cli_delete(db_session, contracts, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                           event_end=datetime(2023, 7, 26, 14, 0),
                           location="Test Location One", attendees=50,
                           instruction="Test Instruction One", contract=contract1,
                           collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(event, ['delete', str(event_instance.id)],
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "Event deleted successfully" in result.output.strip()

def test_event_createform(db_session, contracts, seller_user):
    runner = CliRunner()

    # Test data
    name = "Test Event"
    event_start = "2023/07/26-10:00:00"
    event_end = "2023/07/26-14:00:00"
    location = "Test Location"
    attendees = "50"
    instruction = "Test Instruction"

    event_start_compared = "2023-07-26 10:00:00"
    event_end_compared = "2023-07-26 14:00:00"

    contract1, contract2 = contracts

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        input_data = f"{name}\n{event_start}\n{event_end}\n{location}\n{attendees}\n{instruction}\n{contract1.id}\n"
        result = runner.invoke(eventform, ['createform'], input=input_data,obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    # Check if the success message is displayed in the output
    assert "Event created successfully" in stripped_output

    assert f"{name}" in stripped_output
    assert f"{event_start_compared}" in stripped_output
    assert f"{event_end_compared}" in stripped_output
    assert f"{location}" in stripped_output
    assert f"{attendees}" in stripped_output
    assert f"{instruction}" in stripped_output
    assert f"{contract1.id}" in stripped_output


def test_event_readform(db_session, contracts, admin_user, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Create two Event instances
    event1 = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)
    event2 = Event(name="Event Two", event_start=datetime(2023, 10, 26, 10, 0),
                   event_end=datetime(2023, 10, 26, 14, 0),
                   location="Test Location Two", attendees=70,
                   instruction="Test Instruction Two", contract=contract2,
                   collaborator=support_user)

    db_session.add_all([event1, event2])
    db_session.commit()

    event1_start_compared = "2023-07-26 10:00:00"
    event1_end_compared = "2023-07-26 14:00:00"
    event2_start_compared = "2023-10-26 10:00:00"
    event2_end_compared = "2023-10-26 14:00:00"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        input_data = f"False\nBoth\n"
        result = runner.invoke(eventform, ['readform'], input=input_data, obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    # Verify that both contracts are listed
    assert f"{event1.id}" in stripped_output.replace("\n", "")
    assert f"{event2.id}" in stripped_output.replace("\n", "")


def test_event_get_by_id_form(db_session, contracts, support_user, admin_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    event_start_compared = "2023-07-26 10:00:00"
    event_end_compared = "2023-07-26 14:00:00"

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        input_data = f"{event_instance.id}\n"
        result = runner.invoke(eventform, ['getbyidform'], input=input_data, obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    assert f"{event_instance.id}" in stripped_output
    assert f"{event_start_compared}" in stripped_output
    assert f"{event_end_compared}" in stripped_output
    assert f"{event_instance.location}" in stripped_output
    assert f"{event_instance.attendees}" in stripped_output
    assert f"{event_instance.instruction}" in stripped_output

def test_event_updateform(db_session, contracts, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                   event_end=datetime(2023, 7, 26, 14, 0),
                   location="Test Location One", attendees=50,
                   instruction="Test Instruction One", contract=contract1,
                   collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        new_name = "Test Event"
        new_event_start = "2020/05/25-09:00:00"
        unchanged_event_end = "None"
        unchanged_location = "None"
        unchanged_attendees = "None"
        new_instruction = "Test Instruction"
        unchanged_contract = "None"
        unchanged_support = "None"
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        input_data = f"{event_instance.id}\n{new_name}\n{new_event_start}\n{unchanged_event_end}\n{unchanged_location}\n{unchanged_attendees}\n{new_instruction}\n{unchanged_contract}\n{unchanged_support}\n"
        result = runner.invoke(eventform, ['updateform'], input=input_data, obj=db_session)

    new_event_start_compared = "2020-05-25 09:00:00"

    unchanged_event_location_compared = "Test Location One"
    unchanged_event_attendees_compared = 50
    unchanged_event_start_compared = "2023-07-26 14:00:00"

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Remove ANSI escape codes from the output
    stripped_output = remove_ansi_escape_codes(result.output)

    assert f"{new_name}" in stripped_output
    assert f"{new_event_start_compared}" in stripped_output
    assert f"{unchanged_event_start_compared}" in stripped_output
    assert f"{unchanged_event_location_compared}" in stripped_output
    assert f"{unchanged_event_attendees_compared}" in stripped_output
    assert f"{new_instruction}" in stripped_output


def test_event_deleteform(db_session, contracts, support_user):
    runner = CliRunner()

    contract1, contract2 = contracts

    # Test data
    event_instance = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                           event_end=datetime(2023, 7, 26, 14, 0),
                           location="Test Location One", attendees=50,
                           instruction="Test Instruction One", contract=contract1,
                           collaborator=support_user)

    db_session.add(event_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        input_data = f"{event_instance.id}\n"
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(eventform, ['deleteform'], input=input_data,
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "Event deleted successfully" in result.output.strip()
