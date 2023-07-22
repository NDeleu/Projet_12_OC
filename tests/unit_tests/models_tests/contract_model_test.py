from app.models import Contract, Customer, Collaborator


def test_create_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test creating a new contract
    new_contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    # Check if the contract was created successfully
    assert new_contract.id is not None
    assert new_contract.total_amount == 1000.0
    assert new_contract.left_to_pay == 500.0
    assert new_contract.customer == customer


def test_get_by_id_contract(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
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
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
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
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Create a new customer for contract association
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Test deleting an existing contract
    contract = Contract.create(db_session, total_amount=1000.0, left_to_pay=500.0, customer=customer)

    # Delete the contract
    contract.delete(db_session)

    # Check if the contract was deleted successfully
    deleted_contract = Contract.get_by_id(db_session, contract.id)
    assert deleted_contract is None
