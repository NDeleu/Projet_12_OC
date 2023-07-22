from app.models import Administrator


def test_create_administrator(db_session):
    # Test creating a new administrator
    new_administrator = Administrator.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Check if the administrator was created successfully
    assert new_administrator.id is not None
    assert new_administrator.surname == "John"
    assert new_administrator.lastname == "Doe"
    assert new_administrator.email == "john.doe@example.com"
    assert new_administrator.verify_password("secret")


def test_read_administrator(db_session):
    # Test reading an existing administrator from the database
    administrator = Administrator.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    read_administrator = Administrator.read(db_session, administrator.id)

    # Check if the read operation returns the correct administrator
    assert read_administrator is not None
    assert read_administrator.id == administrator.id
    assert read_administrator.surname == "John"
    assert read_administrator.lastname == "Doe"
    assert read_administrator.email == "john.doe@example.com"


def test_update_administrator(db_session):
    # Test updating an existing administrator
    administrator = Administrator.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Update the administrator's email
    administrator.update(db_session, email="john.doe.updated@example.com")

    # Check if the email was updated successfully
    updated_administrator = Administrator.read(db_session, administrator.id)
    assert updated_administrator.email == "john.doe.updated@example.com"


def test_delete_administrator(db_session):
    # Test deleting an existing administrator
    administrator = Administrator.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Delete the administrator
    administrator.delete(db_session)

    # Check if the administrator was deleted successfully
    deleted_administrator = Administrator.read(db_session, administrator.id)
    assert deleted_administrator is None
