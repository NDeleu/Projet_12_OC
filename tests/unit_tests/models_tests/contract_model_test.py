from app.models import Contract, Customer, Collaborator, Event
import pytest


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
    event = Event(name="My Event", event_start="2023-07-22 10:00:00",
                  event_end="2023-07-22 18:00:00",
                  location="Paris", attendees=50,
                  instruction="Some instructions", contract=contracts[0])
    db_session.add(event)

    db_session.commit()

    return contracts


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
