from app.models import Customer, Collaborator


def test_create_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test creating a new customer
    new_customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                    phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Check if the customer was created successfully
    assert new_customer.id is not None
    assert new_customer.surname == "John"
    assert new_customer.lastname == "Doe"
    assert new_customer.email == "john.doe@example.com"
    assert new_customer.phone == 123456789
    assert new_customer.company == "ABC Corp"
    assert new_customer.collaborator == collaborator


def test_get_by_id_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test reading an existing customer from the database
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    read_customer = Customer.get_by_id(db_session, customer.id)

    # Check if the get by id operation returns the correct customer
    assert read_customer is not None
    assert read_customer.id == customer.id
    assert read_customer.surname == "John"
    assert read_customer.lastname == "Doe"
    assert read_customer.email == "john.doe@example.com"
    assert read_customer.phone == 123456789
    assert read_customer.company == "ABC Corp"
    assert read_customer.collaborator == collaborator


def test_get_by_email_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test reading an existing customer from the database
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    read_customer = Customer.get_by_email(db_session, customer.email)

    # Check if the get by email operation returns the correct customer
    assert read_customer is not None
    assert read_customer.id == customer.id
    assert read_customer.surname == "John"
    assert read_customer.lastname == "Doe"
    assert read_customer.email == "john.doe@example.com"
    assert read_customer.phone == 123456789
    assert read_customer.company == "ABC Corp"
    assert read_customer.collaborator == collaborator

def test_update_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test updating an existing customer
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Update the customer's email and phone
    customer.update(db_session, email="john.doe.updated@example.com", phone=987654321)

    # Check if the email and phone were updated successfully
    updated_customer = Customer.get_by_id(db_session, customer.id)
    assert updated_customer.email == "john.doe.updated@example.com"
    assert updated_customer.phone == 987654321


def test_delete_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, surname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test deleting an existing customer
    customer = Customer.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com",
                                phone=123456789, company="ABC Corp", collaborator=collaborator)

    # Delete the customer
    customer.delete(db_session)

    # Check if the customer was deleted successfully
    deleted_customer = Customer.get_by_id(db_session, customer.id)
    assert deleted_customer is None
