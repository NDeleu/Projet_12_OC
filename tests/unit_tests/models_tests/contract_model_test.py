from app.models import Contract, Customer, Collaborator, Event
import pytest
from datetime import datetime
from sqlalchemy.exc import StatementError


def test_create_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test creating a new contract
    new_contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    # Check if the contract was created successfully
    assert new_contract.id is not None
    assert new_contract.total_amount == 1000.0
    assert new_contract.left_to_pay == 500.0
    assert new_contract.customer == customer


    # Test creating a new contract with invalid input (non-numeric total_amount)
    with pytest.raises(TypeError):
        Contract.create(db_session, total_amount="invalid", left_to_pay=500.0, customer=customer)

    # Test creating a new contract with invalid input (non-numeric left_to_pay)
    with pytest.raises(TypeError, match="Left to pay must be a numeric value."):
        Contract.create(db_session, total_amount=1000.0, left_to_pay="invalid", customer=customer)

    # Test creating a new contract with invalid input (non-boolean signed)
    with pytest.raises(TypeError, match="Signed must be a boolean value."):
        Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer, signed="invalid")


@pytest.fixture
def db_contract_data(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Create some test contracts
    contracts = [
        Contract.create(db_session, total_amount=1000.0, left_to_pay=0, customer=customer, signed=True),
        Contract.create(db_session, total_amount=1500.0, left_to_pay=750.0, customer=customer, signed=False),
        Contract.create(db_session, total_amount=2000.0, left_to_pay=1000.0, customer=customer, signed=True),
    ]

    # Create an event and associate it with one of the contracts
    event = Event(name="My Event", event_start=datetime(2023, 7, 22, 10, 0, 0),
                  event_end=datetime(2023, 7, 22, 18, 0, 0),
                  location="Paris", attendees=50,
                  instruction="Some instructions", contract=contracts[0])
    db_session.add(event)

    db_session.commit()

    return contracts


@pytest.mark.parametrize("user_id, signed, event, paid, expected_count", [
    # Test reading contracts with invalid input (non-boolean signed)
    (None, "invalid", None, None, TypeError),
    # Test reading contracts with invalid input (non-boolean event)
    (None, None, "invalid", None, TypeError),
    # Test reading contracts with invalid input (non-boolean paid)
    (None, None, None, "invalid", TypeError),
])
def test_read_contract_with_invalid_input(db_session, db_contract_data, user_id, signed, event, paid, expected_count):
    with pytest.raises(expected_count):
        Contract.read(db_session, user_id=user_id, signed=signed, event=event, paid=paid)


@pytest.mark.parametrize("user_id, signed, event, paid, expected_count", [
    (None, None, None, None, 3),                # Read all contracts
    (1, None, None, None, 3),                   # Read contracts for a specific user (customer) by user_id
    (None, True, None, None, 2),                # Read contracts by signed status (True)
    (None, None, True, None, 1),                # Read contracts by event status (True)
    (None, None, False, None, 2),               # Read contracts by event status (False)
    (None, None, None, True, 1),                # Read contracts by paid status (True)
    (None, None, None, False, 2),               # Read contracts by paid status (False)
])
def test_read_contract(db_session, db_contract_data, user_id, signed, event, paid, expected_count):
    contracts = Contract.read(db_session, user_id=user_id, signed=signed, event=event, paid=paid)
    assert len(contracts) == expected_count


def test_get_by_id_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test reading an existing contract from the database
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    read_contract = Contract.get_by_id(db_session, contract.id)

    # Check if the read operation returns the correct contract
    assert read_contract is not None
    assert read_contract.id == contract.id
    assert read_contract.total_amount == 1000.0
    assert read_contract.left_to_pay == 500.0
    assert read_contract.customer == customer

    # Test reading a contract with an invalid contract_id (non-existent contract_id)
    non_existent_contract_id = 999
    contract = Contract.get_by_id(db_session, non_existent_contract_id)
    assert contract is None


def test_update_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test updating an existing contract
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    # Update the contract's total_amount
    contract.update(db_session, total_amount=1500.0)

    # Check if the total_amount was updated successfully
    updated_contract = Contract.get_by_id(db_session, contract.id)
    assert updated_contract.total_amount == 1500.0

    # Test updating an existing contract with invalid input (non-boolean signed)
    with pytest.raises(StatementError):
        contract.update(db_session, signed="invalid")


def test_delete_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test deleting an existing contract
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    # Delete the contract
    contract.delete(db_session)

    # Check if the contract was deleted successfully
    deleted_contract = Contract.get_by_id(db_session, contract.id)
    assert deleted_contract is None
