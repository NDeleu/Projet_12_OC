from click.testing import CliRunner
from app.controllers.business_controllers.customer_controllers.customer_cli import customer, customerform
from app.models.class_models.business_models.customer_model import Customer
from unittest.mock import patch
import pytest


def test_customer_api_cli_create(db_session, seller_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    firstname = "Nathalie"
    lastname = "Dowel"
    email = "nathalie.dowel@example.com"
    phone = "1234567890"
    company = "La grande marque"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customer, ['create', firstname, lastname, email, phone, company], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Customer created successfully" in result.output.strip()

    assert f"{firstname}" in result.output.strip()
    assert f"{lastname}" in result.output.strip()
    assert f"{email}" in result.output.strip()
    assert f"{phone}" in result.output.strip()
    assert f"{company}" in result.output.strip()
    assert f"{seller_user.email}" in result.output.strip()


def test_customer_api_cli_read(db_session, seller_user):
    runner = CliRunner()

    customer1 = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    customer2 = Customer(firstname="George", lastname="Habingdom", email="george.habingdom@example.com", phone="0123456789", company="Le super marche", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customer, ['read', '--mine=True'], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer1.id}" in result.output.strip().replace("\n", "")

    assert f"{customer2.id}" in result.output.strip().replace("\n", "")


# Test for 'get_by_id' function
def test_customer_api_get_by_id(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customer, ['getbyid', str(customer_instance.id)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{customer_instance.firstname}" in result.output.strip()
    assert f"{customer_instance.lastname}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"{customer_instance.phone}" in result.output.strip()
    assert f"{customer_instance.company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


# Test for 'get_by_email' function
def test_customer_api_get_by_email(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customer, ['getbyemail', customer_instance.email], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{customer_instance.firstname}" in result.output.strip()
    assert f"{customer_instance.lastname}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"{customer_instance.phone}" in result.output.strip()
    assert f"{customer_instance.company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


# Test for 'update' function
def test_customer_api_update(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Replace the input arguments with specific values for testing
    new_firstname = "Jean"
    new_lastname = "Duflot"
    new_email = "jean.duflot@example.com"
    new_company = "Les grands habits"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(
            customer,
            ['update', str(customer_instance.id), '--firstname', new_firstname, '--lastname', new_lastname,
             '--email', new_email, '--company', new_company],
            obj=db_session
        )

    unchanged_phone_compared = "1234567890"

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Customer updated successfully" in result.output.strip()

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{new_firstname}" in result.output.strip()
    assert f"{new_lastname}" in result.output.strip()
    assert f"{new_email}" in result.output.strip()
    assert f"{unchanged_phone_compared}" in result.output.strip()
    assert f"{new_company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


# Test for 'delete' function
def test_customer_api_delete(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customer, ['delete', str(customer_instance.id)], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Customer deleted successfully" in result.output.strip()


# Test for 'createform' function
def test_customer_createform(db_session, seller_user):
    runner = CliRunner()

    # Replace the input arguments with specific values for testing
    # Replace the input arguments with specific values for testing
    firstname = "Nathalie"
    lastname = "Dowel"
    email = "nathalie.dowel@example.com"
    phone = "1234567890"
    company = "La grande marque"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{firstname}\n{lastname}\n{email}\n{phone}\n{company}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `createform`
        result = runner.invoke(customerform, ['createform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Customer created successfully" in result.output.strip()

    assert f"{firstname}" in result.output.strip()
    assert f"{lastname}" in result.output.strip()
    assert f"{email}" in result.output.strip()
    assert f"{phone}" in result.output.strip()
    assert f"{company}" in result.output.strip()
    assert f"{seller_user.email}" in result.output.strip()


# Test for 'readform' function
def test_customer_readform(db_session, seller_user):
    runner = CliRunner()

    customer1 = Customer(firstname="Nathalie", lastname="Dowel", email="nathalie.dowel@example.com", phone="1234567890", company="La grande marque", collaborator=seller_user)
    customer2 = Customer(firstname="George", lastname="Habingdom", email="george.habingdom@example.com", phone="0123456789", company="Le super marche", collaborator=seller_user)
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `readform`
        result = runner.invoke(customerform, ['readform'], input=f"{True}\n", obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer1.id}" in result.output.strip().replace("\n", "")

    assert f"{customer2.id}" in result.output.strip().replace("\n", "")


# Test for 'getbyidform' function
def test_customer_getbyidform(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{customer_instance.id}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `getbyidform`
        result = runner.invoke(customerform, ['getbyidform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{customer_instance.firstname}" in result.output.strip()
    assert f"{customer_instance.lastname}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"{customer_instance.phone}" in result.output.strip()
    assert f"{customer_instance.company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


# Test for 'getbyemailform' function
def test_customer_getbyemailform(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{customer_instance.email}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `getbyemailform`
        result = runner.invoke(customerform, ['getbyemailform'], input=input_data, obj=db_session)

    # Assurez-vous que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{customer_instance.firstname}" in result.output.strip()
    assert f"{customer_instance.lastname}" in result.output.strip()
    assert f"{customer_instance.email}" in result.output.strip()
    assert f"{customer_instance.phone}" in result.output.strip()
    assert f"{customer_instance.company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


# Test for 'updateform' function
def test_customer_updateform(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Replace the input arguments with specific values for testing
    new_firstname = "Jean"
    new_lastname = "Duflot"
    new_email = "jean.duflot@example.com"
    unchanged_phone = "None"
    new_company = "Les grands habits"

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=seller_user):
        # Utilisez `input` pour fournir les saisies utilisateur requises par la sous-commande
        input_data = f"{customer_instance.id}\n{new_firstname}\n{new_lastname}\n{new_email}\n{unchanged_phone}\n{new_company}\n"

        # Utilisez `invoke` pour appeler la commande principale `collaborator` avec la sous-commande `updateform`
        result = runner.invoke(customerform, ['updateform'], input=input_data, obj=db_session)

    unchanged_phone_compared = "1234567890"

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    # Check if the success message is displayed in the output
    assert "Customer updated successfully" in result.output.strip()

    assert f"{customer_instance.id}" in result.output.strip()
    assert f"{new_firstname}" in result.output.strip()
    assert f"{new_lastname}" in result.output.strip()
    assert f"{new_email}" in result.output.strip()
    assert f"{unchanged_phone_compared}" in result.output.strip()
    assert f"{new_company}" in result.output.strip()
    assert f"{customer_instance.collaborator.email}" in result.output.strip()


def test_customer_delete_form(db_session, seller_user):
    runner = CliRunner()

    customer_instance = Customer(firstname="Nathalie", lastname="Dowel",
                                 email="nathalie.dowel@example.com",
                                 phone="1234567890",
                                 company="La grande marque",
                                 collaborator=seller_user)

    db_session.add(customer_instance)
    db_session.commit()

    # Mock the get_logged_as_user function to return the admin_user
    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            return_value=seller_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(customerform, ['deleteform'],
                               input=f"{customer_instance.id}\n",
                               obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "Customer deleted successfully" in result.output.strip()
