from click.testing import CliRunner
from app.controllers.business_controllers.contract_controllers.contract_cli import contract, contractform
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from datetime import datetime
from unittest.mock import patch
import pytest


def test_contract_api_cli_create(db_session, admin_user, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com", phone="1234567890",
                                 company="La grande marque", collaborator=seller_user)
    db_session.add(customer_instance)
    db_session.commit()

    # Replace the input arguments with specific values for testing
    total_amount = 1000.00
    left_to_pay = 500.00
    customer = customer_instance.id
    signed = False

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contract, ['create', str(total_amount), str(left_to_pay), str(customer), str(signed)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Contract created successfully" in result.output.strip()

    assert f"{total_amount}" in result.output.strip()
    assert f"{left_to_pay}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"No" in result.output.strip()


def test_contract_api_cli_read(db_session, seller_user, support_user):
    runner = CliRunner()

    # Create some customer instances for contracts
    customer1 = Customer(firstname="Customer1", lastname="Smith",
                         email="customer1@example.com", phone="1234567890",
                         company="Company A", collaborator=seller_user)
    customer2 = Customer(firstname="Customer2", lastname="Johnson",
                         email="customer2@example.com", phone="9876543210",
                         company="Company B", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Create some contract instances
    contract1 = Contract(total_amount=5000, left_to_pay=2000, customer=customer1, signed=True)
    contract2 = Contract(total_amount=8000, left_to_pay=3000, customer=customer2, signed=False)
    db_session.add_all([contract1, contract2])
    db_session.commit()

    # Create an event instance for contracts
    event = Event(name="Event Test", event_start=datetime(2023, 7, 26, 10, 0), event_end=datetime(2023, 7, 26, 14, 0), location="Test Location", attendees=50, instruction="Test Instruction", contract=contract1, collaborator=support_user)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contract, ['read', '--mine=False'], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Verify that both contracts are listed
    assert f"{contract1.id}" and f"{contract1.total_amount}" and f"{contract1.left_to_pay}" and f"{customer1.email}" and "Yes" in result.output.strip().replace("\n", "")
    assert f"{contract2.id}" and f"{contract2.total_amount}" and f"{contract2.left_to_pay}" and f"{customer2.email}" and "No" in result.output.strip().replace("\n", "")


def test_contract_api_cli_get_by_id(db_session, support_user, admin_user):
    runner = CliRunner()

    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="0234567890",
                         company="La grande marque", collaborator=support_user)
    db_session.add(customer)
    db_session.commit()

    contract_instance = Contract(total_amount=5432, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contract, ['getbyid', str(contract_instance.id)],
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{contract_instance.id}" in result.output.strip()
    assert f"{contract_instance.total_amount}" in result.output.strip()
    assert f"{contract_instance.left_to_pay}" in result.output.strip()
    assert f"{contract_instance.customer.email}" in result.output.strip()
    assert f"Yes" in result.output.strip()


def test_contract_api_cli_update(db_session, seller_user, admin_user):
    runner = CliRunner()

    # Create a customer for contract
    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com", phone="1234567890",
                                 company="La grande marque", collaborator=seller_user)
    db_session.add(customer_instance)
    db_session.commit()

    # Create a contract
    total_amount = 10000
    left_to_pay = 5000
    signed = False
    contract_instance = Contract(total_amount=total_amount, left_to_pay=left_to_pay, customer=customer_instance, signed=signed)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        new_total_amount = 8765
        new_left_to_pay = 4000
        new_signed = True
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contract, ['update',
                                          str(contract_instance.id),
                                          f"--total_amount={new_total_amount}",
                                          f"--left_to_pay={new_left_to_pay}",
                                          f"--signed={new_signed}"],
                               obj=db_session
                               )

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{contract_instance.id}" in result.output.strip()
    assert f"{new_total_amount}" in result.output.strip()
    assert f"{new_left_to_pay}" in result.output.strip()
    assert f"Yes" in result.output.strip()


def test_contract_api_cli_delete(db_session, seller_user, admin_user):
    runner = CliRunner()

    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    contract_instance = Contract(total_amount=5000, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contract, ['delete', str(contract_instance.id)],
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "Contract deleted successfully" in result.output.strip()


def test_contract_createform(db_session, admin_user, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com", phone="1234567890",
                                 company="La grande marque", collaborator=seller_user)
    db_session.add(customer_instance)
    db_session.commit()

    # Replace the input arguments with specific values for testing
    total_amount = 1000.00
    left_to_pay = 500.00
    customer = customer_instance.id
    signed = False

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        input_data = f"{total_amount}\n{left_to_pay}\n{customer}\n{signed}\n"
        result = runner.invoke(contractform, ['createform'], input=input_data, obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Contract created successfully" in result.output.strip()

    assert f"{total_amount}" in result.output.strip()
    assert f"{left_to_pay}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"No" in result.output.strip()


def test_contract_readform(db_session, seller_user, support_user):
    runner = CliRunner()

    # Create some customer instances for contracts
    customer1 = Customer(firstname="Customer1", lastname="Smith",
                         email="customer1@example.com", phone="1234567890",
                         company="Company A", collaborator=seller_user)
    customer2 = Customer(firstname="Customer2", lastname="Johnson",
                         email="customer2@example.com", phone="9876543210",
                         company="Company B", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Create some contract instances
    contract1 = Contract(total_amount=5000, left_to_pay=2000, customer=customer1, signed=True)
    contract2 = Contract(total_amount=8000, left_to_pay=3000, customer=customer2, signed=False)
    db_session.add_all([contract1, contract2])
    db_session.commit()

    # Create an event instance for contracts
    event = Event(name="Event Test", event_start=datetime(2023, 7, 26, 10, 0), event_end=datetime(2023, 7, 26, 14, 0), location="Test Location", attendees=50, instruction="Test Instruction", contract=contract1, collaborator=support_user)
    db_session.add(event)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        input_data = "False\nBoth\nBoth\nBoth\n"
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contractform, ['readform'], input=input_data, obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Verify that both contracts are listed
    assert f"{contract1.id}" and f"{contract1.total_amount}" and f"{contract1.left_to_pay}" and f"{customer1.email}" and "Yes" in result.output.strip().replace("\n", "")
    assert f"{contract2.id}" and f"{contract2.total_amount}" and f"{contract2.left_to_pay}" and f"{customer2.email}" and "No" in result.output.strip().replace("\n", "")


def test_contract_get_by_id_form(db_session, support_user, admin_user):
    runner = CliRunner()

    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="0234567890",
                         company="La grande marque", collaborator=support_user)
    db_session.add(customer)
    db_session.commit()

    contract_instance = Contract(total_amount=5432, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contractform, ['getbyidform'], input=f"{contract_instance.id}\n", obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{contract_instance.id}" in result.output.strip()
    assert f"{contract_instance.total_amount}" in result.output.strip()
    assert f"{contract_instance.left_to_pay}" in result.output.strip()
    assert f"{contract_instance.customer.email}" in result.output.strip()
    assert f"Yes" in result.output.strip()


# Test for 'updateform' function
def test_contract_update_form(db_session, support_user, admin_user):
    runner = CliRunner()

    # Create a customer for contract
    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com", phone="1234567890",
                                 company="La grande marque", collaborator=support_user)
    db_session.add(customer_instance)
    db_session.commit()

    # Create a contract
    total_amount = 10000
    left_to_pay = 5000
    signed = False
    contract_instance = Contract(total_amount=total_amount, left_to_pay=left_to_pay, customer=customer_instance, signed=signed)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        new_total_amount = 8765
        new_left_to_pay = 4000
        new_signed = True
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contractform, ['updateform'],
                               input=f"{contract_instance.id}\n{new_total_amount}\n{new_left_to_pay}\n{new_signed}\n",
                               obj=db_session
                               )

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{contract_instance.id}" in result.output.strip()
    assert f"{new_total_amount}" in result.output.strip()
    assert f"{new_left_to_pay}" in result.output.strip()
    assert f"Yes" in result.output.strip()


# Test for 'deleteform' function
def test_contract_delete_form(db_session, support_user, admin_user):
    runner = CliRunner()

    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=support_user)
    db_session.add(customer)
    db_session.commit()

    contract_instance = Contract(total_amount=5000, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(contractform, ['deleteform'],
                               input=f"{contract_instance.id}\n",
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "Contract deleted successfully" in result.output.strip()