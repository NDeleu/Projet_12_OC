from app.controllers.business_controllers.contract_controllers.contract_controller import (
    create_func,
    read_func,
    get_by_id_func,
    update_func,
    delete_func,
)
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from datetime import datetime
from unittest.mock import patch


def test_contract_create_func(db_session, admin_user, seller_user, capsys):
    # Create a customer for contract
    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com", phone="1234567890",
                                 company="La grande marque", collaborator=seller_user)
    db_session.add(customer_instance)
    db_session.commit()

    # Test data
    total_amount = 9876543.21
    left_to_pay = 50
    customer_id = customer_instance.id
    signed = False

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        create_func(db_session, total_amount, left_to_pay, customer_id, signed)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was created in the database
    contract = db_session.query(Contract).filter(Contract.total_amount == total_amount).first()
    assert contract is not None
    assert float(contract.total_amount) == total_amount
    assert float(contract.left_to_pay) == left_to_pay
    assert contract.customer_id == customer_instance.id
    assert contract.signed == signed

    assert "Contract created successfully." in captured_stdout


def test_contract_read_func(db_session, admin_user, seller_user, support_user, capsys):
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
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Run the function with no filters
        read_func(db_session, mine=False, is_signed=None, with_event=None,
                  is_paid=None)

    captured_stdout = capsys.readouterr().out

    # Verify that both contracts are listed
    assert f"{contract1.id}" and f"{contract1.total_amount}" and f"{contract1.left_to_pay}" and f"{customer1.email}" and "Signed: Yes" in captured_stdout
    assert f"{contract2.id}" and f"{contract2.total_amount}" and f"{contract2.left_to_pay}" and f"{customer2.email}" and "Signed: No" in captured_stdout


    # Run the function with filters
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        read_func(db_session, mine=True, is_signed=True, with_event=True,
                  is_paid=None)

    captured_stdout = capsys.readouterr().out

    # Verify that the filtered contract (contract1) is listed
    assert f"{contract1.id}" and f"{contract1.total_amount}" and f"{contract1.left_to_pay}" and f"{customer1.email}" and "Signed: Yes" in captured_stdout
    assert f"{contract2.id}" and f"{contract2.total_amount}" and f"{contract2.left_to_pay}" and f"{customer2.email}" and "Signed: No" not in captured_stdout

    assert "Permission denied. Please log in as a seller to access the mine option for events. The full list of contracts is selected instead." in captured_stdout

    # Verify that the filtered contract (contract2) is listed
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        read_func(db_session, mine=True, is_signed=False, with_event=False,
                  is_paid=None)

    captured_stdout = capsys.readouterr().out

    assert f"{contract1.id}" and f"{contract1.total_amount}" and f"{contract1.left_to_pay}" and f"{customer1.email}" and "Signed: Yes" not in captured_stdout
    assert f"{contract2.id}" and f"{contract2.total_amount}" and f"{contract2.left_to_pay}" and f"{customer2.email}" and "Signed: No" in captured_stdout


def test_contract_get_by_id_func(db_session, support_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="0234567890",
                         company="La grande marque", collaborator=support_user)
    db_session.add(customer)
    db_session.commit()

    contract = Contract(total_amount=5432, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        get_by_id_func(db_session, contract.id)

    captured_stdout = capsys.readouterr().out

    assert f"{contract.id}" and f"{contract.total_amount}" and f"{contract.left_to_pay}" and f"{customer.email}" in captured_stdout

    contract_found = db_session.query(Contract).filter(Contract.id == contract.id).first()
    assert contract_found is not None
    assert float(contract_found.total_amount) == contract.total_amount
    assert float(contract_found.left_to_pay) == contract.left_to_pay
    assert contract_found.customer_id == customer.id
    assert contract_found.signed == contract.signed

    wrong_contract_id = 250
    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=support_user):
        # Run the function
        get_by_id_func(db_session, wrong_contract_id)

    captured_stdout = capsys.readouterr().out

    assert "Contract not found." in captured_stdout


def test_contract_update_func(db_session, admin_user, seller_user, capsys):
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
    contract = Contract(total_amount=total_amount, left_to_pay=left_to_pay, customer=customer_instance, signed=signed)
    db_session.add(contract)
    db_session.commit()

    # Test case 1: Update contract as an administrator
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        new_total_amount = 8765
        new_left_to_pay = 4000
        new_signed = True
        update_func(db_session, contract.id, new_total_amount, new_left_to_pay, new_signed)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was updated in the database
    new_contract = db_session.query(Contract).filter(Contract.id == contract.id).first()
    assert new_contract is not None
    assert float(new_contract.total_amount) == new_total_amount
    assert float(new_contract.left_to_pay) == new_left_to_pay
    assert new_contract.signed == new_signed

    assert "Contract updated successfully." in captured_stdout

    # Test case 2: Update contract as the referring seller
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        new_total_amount = 7654
        new_left_to_pay = 3000
        new_signed = False
        update_func(db_session, contract.id, new_total_amount, new_left_to_pay, new_signed)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was updated in the database
    new_contract = db_session.query(Contract).filter(Contract.id == contract.id).first()
    assert new_contract is not None
    assert float(new_contract.total_amount) == new_total_amount
    assert float(new_contract.left_to_pay) == new_left_to_pay
    assert new_contract.signed == new_signed

    assert "Contract updated successfully." in captured_stdout

    # Test case 3: Update contract with non-existing ID
    wrong_contract_id = 250

    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        new_total_amount = 6543
        new_left_to_pay = 4500
        new_signed = True
        update_func(db_session, wrong_contract_id, new_total_amount, new_left_to_pay, new_signed)

    captured_stdout = capsys.readouterr().out

    assert "Contract not found." in captured_stdout

    # Test case 4: Attempt to update contract as a different seller
    other_seller_user = Collaborator(firstname="Other", lastname="Seller", email="other@example.com", role=Collaborator.RoleEnum.seller, password="otherpassword")
    db_session.add(other_seller_user)
    db_session.commit()

    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=other_seller_user):
        new_total_amount = 5432
        new_left_to_pay = 3750
        new_signed = False
        update_func(db_session, contract.id, new_total_amount, new_left_to_pay, new_signed)

    captured_stdout = capsys.readouterr().out

    assert "Only an administrator or the referring seller can update the contract." in captured_stdout


def test_delete_func(db_session, admin_user, seller_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    contract = Contract(total_amount=5000, left_to_pay=2000, customer=customer, signed=True)
    db_session.add(contract)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        # Run the function
        delete_func(db_session, contract.id)

    captured_stdout = capsys.readouterr().out

    # Verify that the event was deleted from the database
    deleted_contract = db_session.query(Contract).filter(
        Contract.id == contract.id).first()
    assert deleted_contract is None

    assert "Contract deleted successfully." in captured_stdout
