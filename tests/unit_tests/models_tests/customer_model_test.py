from app.models import Customer, Collaborator
import pytest


def test_create_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test creating a new customer
    new_customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                    phone="0123456789", company="ABC Corp", collaborator=collaborator)

    # Check if the customer was created successfully
    assert new_customer.id is not None
    assert new_customer.firstname == "John"
    assert new_customer.lastname == "Doe"
    assert new_customer.email == "john.doe@example.com"
    assert new_customer.phone == "0123456789"
    assert new_customer.company == "ABC Corp"
    assert new_customer.collaborator == collaborator

    # Test creating a new customer with an email that already exists for another customer or collaborator
    existing_email = "john.doe@example.com"
    with pytest.raises(ValueError,
                       match="The email address already exists for a collaborator or customer."):
        Customer.create(db_session, firstname="Alice", lastname="Smith",
                        email=existing_email,
                        phone="9876543210", company="XYZ Corp",
                        collaborator=collaborator)


def test_read_customers(db_session):
    # Create a new seller for customer association
    collaborator1 = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")
    collaborator2 = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    # Create some customers with different collaborators
    customer1 = Customer.create(db_session, firstname="Smith", lastname="Johnson", email="smith.johnson@example.com",
                                 phone="111111111", company="ABC Corp", collaborator=collaborator1)

    customer2 = Customer.create(db_session, firstname="Doe", lastname="Williams", email="doe.williams@example.com",
                                 phone="222222222", company="XYZ Inc", collaborator=collaborator1)

    customer3 = Customer.create(db_session, firstname="Smith", lastname="Brown", email="smith.brown@example.com",
                                 phone="333333333", company="123 Industries", collaborator=collaborator2)

    # Test reading all customers
    all_customers = Customer.read(db_session)
    assert len(all_customers) == 3
    assert customer1 in all_customers
    assert customer2 in all_customers
    assert customer3 in all_customers

    # Test reading customers associated with a specific collaborator
    collaborator1_customers = Customer.read(db_session, user_id=collaborator1.id)
    assert len(collaborator1_customers) == 2
    assert customer1 in collaborator1_customers
    assert customer2 in collaborator1_customers
    assert customer3 not in collaborator1_customers

    collaborator2_customers = Customer.read(db_session, user_id=collaborator2.id)
    assert len(collaborator2_customers) == 1
    assert customer1 not in collaborator2_customers
    assert customer2 not in collaborator2_customers
    assert customer3 in collaborator2_customers


def test_get_by_id_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test reading an existing customer from the database
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone="123456789", company="ABC Corp", collaborator=collaborator)

    read_customer = Customer.get_by_id(db_session, customer.id)

    # Check if the get by id operation returns the correct customer
    assert read_customer is not None
    assert read_customer.id == customer.id
    assert read_customer.firstname == "John"
    assert read_customer.lastname == "Doe"
    assert read_customer.email == "john.doe@example.com"
    assert read_customer.phone == "123456789"
    assert read_customer.company == "ABC Corp"
    assert read_customer.collaborator == collaborator

    # Test reading a customer with an invalid customer_id (non-existent customer_id)
    non_existent_customer_id = 999
    customer = Customer.get_by_id(db_session, non_existent_customer_id)
    assert customer is None


def test_get_by_email_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test reading an existing customer from the database
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone="123456789", company="ABC Corp", collaborator=collaborator)

    read_customer = Customer.get_by_email(db_session, customer.email)

    # Check if the get by email operation returns the correct customer
    assert read_customer is not None
    assert read_customer.id == customer.id
    assert read_customer.firstname == "John"
    assert read_customer.lastname == "Doe"
    assert read_customer.email == "john.doe@example.com"
    assert read_customer.phone == "123456789"
    assert read_customer.company == "ABC Corp"
    assert read_customer.collaborator == collaborator

    # Test reading a customer with an invalid customer_email (non-existent email)
    non_existent_email = "non_existent@example.com"
    customer = Customer.get_by_email(db_session, non_existent_email)
    assert customer is None


def test_update_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test updating an existing customer
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone="123456789", company="ABC Corp", collaborator=collaborator)

    # Use a different email address for the updated email
    customer.update(db_session, email="john.doe.updated@example.com", phone="987654321")

    # Check if the email and phone were updated successfully
    updated_customer = Customer.get_by_id(db_session, customer.id)
    assert updated_customer.email == "john.doe.updated@example.com"
    assert updated_customer.phone == "987654321"

    # Test updating an existing customer with an email that already exists for another customer or collaborator
    customer2 = Customer.create(db_session, firstname="Customer", lastname="Two", email="customer.two@example.com",
                                phone="555555555", company="XYZ Corp", collaborator=collaborator)
    with pytest.raises(ValueError, match="The email address already exists for a collaborator or customer."):
        customer.update(db_session, email="customer.two@example.com")


def test_delete_customer(db_session):
    # Create a new seller for customer association
    collaborator = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=2, password="secret")

    # Test deleting an existing customer
    customer = Customer.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com",
                                phone="123456789", company="ABC Corp", collaborator=collaborator)

    # Delete the customer
    customer.delete(db_session)

    # Check if the customer was deleted successfully
    deleted_customer = Customer.get_by_id(db_session, customer.id)
    assert deleted_customer is None
