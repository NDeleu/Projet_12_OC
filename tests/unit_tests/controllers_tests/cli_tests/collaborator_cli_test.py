from click.testing import CliRunner
from app.controllers.user_controllers.collaborator_controllers.collaborator_cli import collaborator, collaboratorform
from app.models.class_models.user_models.collaborator_model import Collaborator
from unittest.mock import patch
import pytest


def test_collaborator_api_cli_create(db_session, admin_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    firstname = "John"
    lastname = "Doe"
    email = "john.doe@example.com"
    role = "1"  # Administrator role
    password = "Test@123"  # A valid password

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(collaborator, ['create', firstname, lastname, email, role, password], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Collaborator created successfully" in result.output.strip()

    assert f"{firstname}" in result.output.strip()
    assert f"{lastname}" in result.output.strip()
    assert f"{role}" in result.output.strip()
    assert f"{email}" in result.output.strip()


def test_collaborator_api_cli_read(db_session, admin_user):
    runner = CliRunner()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(collaborator, ['read'], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{admin_user.id}" in result.output.strip()
    assert f"{admin_user.firstname}" in result.output.strip()
    assert f"{admin_user.lastname}" in result.output.strip()
    assert f"{admin_user.role}" in result.output.strip()
    assert f"{admin_user.email}" in result.output.strip()


# Test for 'get_by_id' function
def test_collaborator_api_get_by_id(db_session, admin_user):
    runner = CliRunner()

    collaborator_instance = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(collaborator, ['getbyid', str(collaborator_instance.id)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{collaborator_instance.id}" in result.output.strip()
    assert f"{collaborator_instance.firstname}" in result.output.strip()
    assert f"{collaborator_instance.lastname}" in result.output.strip()
    assert f"{collaborator_instance.role}" in result.output.strip()
    assert f"{collaborator_instance.email}" in result.output.strip()


# Test for 'get_by_email' function
def test_collaborator_api_get_by_email(db_session, admin_user):
    runner = CliRunner()

    # Replace the input argument with a specific collaborator_email for testing
    collaborator_email = admin_user.email

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(collaborator, ['getbyemail', collaborator_email], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{admin_user.id}" in result.output.strip()
    assert f"{admin_user.firstname}" in result.output.strip()
    assert f"{admin_user.lastname}" in result.output.strip()
    assert f"{admin_user.role}" in result.output.strip()
    assert f"{admin_user.email}" in result.output.strip()


# Test for 'update' function
def test_collaborator_api_update(db_session, admin_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    collaborator_id = admin_user.id
    new_firstname = "Updated John"
    new_lastname = "Updated Doe"
    new_email = "updated.john.doe@example.com"
    new_password = "NewPassword@456"  # A valid new password

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(
            collaborator,
            ['update', str(collaborator_id), '--firstname', new_firstname, '--lastname', new_lastname,
             '--email', new_email, '--password', new_password],
            obj=db_session
        )

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Collaborator updated successfully" in result.output.strip()

    assert f"{collaborator_id}" in result.output.strip()
    assert f"{new_firstname}" in result.output.strip()
    assert f"{new_lastname}" in result.output.strip()
    assert f"{new_email}" in result.output.strip()


# Test for 'delete' function
def test_collaborator_api_delete(db_session, admin_user):
    runner = CliRunner()

    # Replace the input argument with a specific collaborator_id for testing
    collaborator_id = admin_user.id

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(collaborator, ['delete', str(collaborator_id)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Collaborator deleted successfully" in result.output.strip()


# Test for 'createform' function
def test_collaborator_createform(db_session, admin_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    firstname = "John"
    lastname = "Doe"
    email = "john.doe@example.com"
    role = 1  # Administrator role
    password = "Test@123"  # A valid password

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{firstname}\n{lastname}\n{email}\n{role}\n{password}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `createform`
        result = runner.invoke(collaboratorform, ['createform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Vérifiez si le message de réussite est affiché dans la sortie
    assert "Collaborator created successfully" in result.output.strip()

    assert f"{firstname}" in result.output.strip()
    assert f"{lastname}" in result.output.strip()
    assert f"{role}" in result.output.strip()
    assert f"{email}" in result.output.strip()


# Test for 'readform' function
def test_collaborator_readform(db_session, admin_user):
    runner = CliRunner()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `readform`
        result = runner.invoke(collaboratorform, ['readform'], obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{admin_user.id}" in result.output.strip()
    assert f"{admin_user.firstname}" in result.output.strip()
    assert f"{admin_user.lastname}" in result.output.strip()
    assert f"{admin_user.role}" in result.output.strip()
    assert f"{admin_user.email}" in result.output.strip()


# Test for 'getbyidform' function
def test_collaborator_getbyidform(db_session, admin_user):
    runner = CliRunner()

    collaborator_instance = Collaborator(firstname="John", lastname="Doe", email="john.doe@example.com",
                                         role=Collaborator.RoleEnum.administrator, password="securepassword")
    db_session.add(collaborator_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{collaborator_instance.id}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `getbyidform`
        result = runner.invoke(collaboratorform, ['getbyidform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{collaborator_instance.id}" in result.output.strip()
    assert f"{collaborator_instance.firstname}" in result.output.strip()
    assert f"{collaborator_instance.lastname}" in result.output.strip()
    assert f"{collaborator_instance.role}" in result.output.strip()
    assert f"{collaborator_instance.email}" in result.output.strip()


# Test for 'getbyemailform' function
def test_collaborator_getbyemailform(db_session, admin_user):
    runner = CliRunner()

    # Replace the input argument with a specific collaborator_email for testing
    collaborator_email = admin_user.email

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{collaborator_email}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `getbyemailform`
        result = runner.invoke(collaboratorform, ['getbyemailform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{admin_user.id}" in result.output.strip()
    assert f"{admin_user.firstname}" in result.output.strip()
    assert f"{admin_user.lastname}" in result.output.strip()
    assert f"{admin_user.role}" in result.output.strip()
    assert f"{admin_user.email}" in result.output.strip()


# Test for 'updateform' function
def test_collaborator_updateform(db_session, admin_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    collaborator_id = admin_user.id
    new_firstname = "Updated John"
    new_lastname = "Updated Doe"
    new_email = "updated.john.doe@example.com"
    new_password = "NewPassword@456"  # A valid new password

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{collaborator_id}\n{new_firstname}\n{new_lastname}\n{new_email}\n{new_password}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `updateform`
        result = runner.invoke(collaboratorform, ['updateform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Vérifiez si le message de réussite est affiché dans la sortie
    assert "Collaborator updated successfully" in result.output.strip()

    assert f"{collaborator_id}" in result.output.strip()
    assert f"{new_firstname}" in result.output.strip()
    assert f"{new_lastname}" in result.output.strip()
    assert f"{new_email}" in result.output.strip()
