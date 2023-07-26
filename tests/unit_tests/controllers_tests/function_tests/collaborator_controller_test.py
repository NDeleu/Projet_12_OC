from app.controllers.user_controllers.collaborator_controllers.collaborator_controller import (
    create_func,
    read_func,
    get_by_id_func,
    get_by_email_func,
    update_func,
    delete_func,
)
from app.models.class_models.user_models.collaborator_model import Collaborator
from unittest.mock import patch
import pytest


def test_collaborator_create_func(db_session, admin_user, capsys):
    # Test data
    firstname = "John"
    lastname = "Doe"
    email = "john.doe@example.com"
    role = Collaborator.RoleEnum.administrator
    password = "securepassword"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        create_func(db_session, firstname, lastname, email, role, password)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was created in the database
    collaborator = Collaborator.get_by_email(db_session, email)
    assert collaborator is not None
    assert collaborator.firstname == firstname
    assert collaborator.lastname == lastname
    assert collaborator.role == role
    assert collaborator.verify_password(password)

    assert "SUCCESS: Collaborator created successfully." in captured_stdout


def test_collaborator_read_func(db_session, admin_user, capsys):
    # Test data
    collaborator = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        read_func(db_session)

    captured_stdout = capsys.readouterr().out

    assert f"{collaborator.id}" in captured_stdout
    assert f"{collaborator.firstname}" in captured_stdout
    assert f"{collaborator.lastname}" in captured_stdout
    assert f"{collaborator.role}" in captured_stdout
    assert f"{collaborator.email}" in captured_stdout


def test_collaborator_get_by_id_func(db_session, admin_user, capsys):
    # Test data
    collaborator = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        get_by_id_func(db_session, collaborator.id)

    captured_stdout = capsys.readouterr().out

    assert f"{collaborator.id}" in captured_stdout
    assert f"{collaborator.firstname}" in captured_stdout
    assert f"{collaborator.lastname}" in captured_stdout
    assert f"{collaborator.email}" in captured_stdout
    assert f"{collaborator.role}" in captured_stdout

    wrong_collaborator_id = 250

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        get_by_id_func(db_session, wrong_collaborator_id)

    captured_stdout = capsys.readouterr().out

    assert "Collaborator not found." in captured_stdout


def test_collaborator_get_by_email_func(db_session, admin_user, capsys):
    # Test data
    collaborator = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        get_by_email_func(db_session, collaborator.email)

    captured_stdout = capsys.readouterr().out

    assert f"{collaborator.id}" in captured_stdout
    assert f"{collaborator.firstname}" in captured_stdout
    assert f"{collaborator.lastname}" in captured_stdout
    assert f"{collaborator.email}" in captured_stdout
    assert f"{collaborator.role}" in captured_stdout

    wrong_collaborator_email = "wrong.email@example.fr"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        get_by_email_func(db_session, wrong_collaborator_email)

    captured_stdout = capsys.readouterr().out

    assert "Collaborator not found." in captured_stdout


def test_collaborator_update_func(db_session, admin_user, capsys):
    # Test data
    collaborator = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        new_firstname = "Updated John"
        new_lastname = "Updated Doe"
        new_email = "updated.john.doe@example.com"
        new_password = "newsecurepassword"
        update_func(db_session, collaborator.id, new_firstname, new_lastname, new_email, new_password)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator's data was updated in the database
    updated_collaborator = Collaborator.get_by_id(db_session, collaborator.id)
    assert updated_collaborator is not None
    assert updated_collaborator.firstname == new_firstname
    assert updated_collaborator.lastname == new_lastname
    assert updated_collaborator.email == new_email
    assert updated_collaborator.verify_password(new_password)

    assert "SUCCESS: Collaborator updated successfully." in captured_stdout


def test_collaborator_delete_func(db_session, admin_user, capsys):
    # Test data
    collaborator = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Run the function
        delete_func(db_session, collaborator.id)

    captured_stdout = capsys.readouterr().out

    # Verify that the collaborator was deleted from the database
    deleted_collaborator = Collaborator.get_by_id(db_session, collaborator.id)
    assert deleted_collaborator is None

    assert "SUCCESS: Collaborator deleted successfully." in captured_stdout
