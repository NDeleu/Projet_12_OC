from app.controllers.business_controllers.customer_controllers.customer_controller import (
    create_func,
    read_func,
    get_by_id_func,
    get_by_email_func,
    update_func,
    delete_func,
)
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from unittest.mock import patch
import pytest


def test_customer_create_func(db_session, seller_user, capsys):
    # Test data
    firstname = "Nathalie"
    lastname = "Dowel"
    email = "nathalie.dowel@example.com"
    phone = "1234567890"
    company = "La grande marque"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Run the function
        create_func(db_session, firstname, lastname, email, phone, company)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was created in the database
    customer = Customer.get_by_email(db_session, email)
    assert customer is not None
    assert customer.firstname == firstname
    assert customer.lastname == lastname
    assert customer.email == email
    assert customer.phone == phone
    assert customer.company == company

    assert "Customer created successfully." in captured_stdout


def test_customer_read_as_seller_func(db_session, seller_user, capsys):
    # Test data
    customer1 = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    customer2 = Customer(firstname="George", lastname="Habingdom", email="george.habingdom@example.com", phone="9876543210", company="Le super marche", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        read_func(db_session, mine=True)

    captured_stdout = capsys.readouterr().out

    assert f"{customer1.id}" in captured_stdout.replace("\n", "")
    assert f"{customer2.id}" in captured_stdout.replace("\n", "")


def test_customer_read_as_other_func(db_session, admin_user, seller_user, capsys):
    # Test data
    customer1 = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    customer2 = Customer(firstname="George", lastname="Habingdom", email="george.habingdom@example.com", phone="0123456789", company="Le super marche", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        read_func(db_session, mine=True)

    captured_stdout = capsys.readouterr().out

    assert f"{customer1.id}" in captured_stdout.replace("\n", "")
    assert f"{customer2.id}" in captured_stdout.replace("\n", "")

    assert "Permission denied. Please login as a seller to access the mine option for customers. The full list of customers is selected instead." in captured_stdout.replace("\n", " ")

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=admin_user):
        read_func(db_session, mine=False)

    captured_stdout = capsys.readouterr().out

    assert f"{customer1.id}" in captured_stdout.replace("\n", "")
    assert f"{customer2.id}" in captured_stdout.replace("\n", "")


def test_customer_get_by_id_func(db_session, seller_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="0234567890",
                         company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Run the function
        get_by_id_func(db_session, customer.id)

    captured_stdout = capsys.readouterr().out

    assert f"{customer.id}" in captured_stdout.replace("\n", "")

    wrong_event_id = 250
    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Run the function
        get_by_id_func(db_session, wrong_event_id)

    captured_stdout = capsys.readouterr().out

    assert "Customer not found." in captured_stdout


def test_customer_get_by_email_func(db_session, seller_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="1234567890",
                         company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Run the function
        get_by_email_func(db_session, customer.email)

    captured_stdout = capsys.readouterr().out

    assert f"{customer.email}" in captured_stdout

    wrong_collaborator_email = "wrong.email@example.fr"
    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Run the function
        get_by_email_func(db_session, wrong_collaborator_email)

    captured_stdout = capsys.readouterr().out

    assert "Customer not found." in captured_stdout


def test_collaborator_update_func(db_session, seller_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel",
                         email="nathalie.dowel@example.com", phone="1234567890",
                         company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Run the function
        new_firstname = "Updated Nathalie"
        new_lastname = "Updated Dowel"
        new_email = "updated.nathalie.dowel@example.com"
        new_phone = "9876543210"
        new_company = "Plus grande que la grande marque"
        update_func(db_session, customer.id, new_firstname, new_lastname, new_email, new_phone, new_company)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator's data was updated in the database
    updated_customer = Customer.get_by_id(db_session, customer.id)
    assert updated_customer is not None
    assert updated_customer.firstname == new_firstname
    assert updated_customer.lastname == new_lastname
    assert updated_customer.email == new_email
    assert updated_customer.phone == new_phone
    assert updated_customer.company == new_company

    assert "Customer updated successfully." in captured_stdout


def test_delete_func(db_session, seller_user, capsys):
    # Test data
    customer = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    db_session.add(customer)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Run the function
        delete_func(db_session, customer.id)

    captured_stdout = capsys.readouterr().out

    # Verify that the event was deleted from the database
    deleted_customer = db_session.query(Customer).filter(
        Customer.id == customer.id).first()
    assert deleted_customer is None

    assert "Customer deleted successfully." in captured_stdout
