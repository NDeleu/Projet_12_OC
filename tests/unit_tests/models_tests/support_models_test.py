from app.models import Support


def test_create_support(db_session):
    # Test creating a new support
    new_support = Support.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Check if the support was created successfully
    assert new_support.id is not None
    assert new_support.surname == "John"
    assert new_support.lastname == "Doe"
    assert new_support.email == "john.doe@example.com"
    assert new_support.verify_password("secret")


def test_read_support(db_session):
    # Test reading an existing support from the database
    support = Support.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    read_support = Support.read(db_session, support.id)

    # Check if the read operation returns the correct support
    assert read_support is not None
    assert read_support.id == support.id
    assert read_support.surname == "John"
    assert read_support.lastname == "Doe"
    assert read_support.email == "john.doe@example.com"


def test_update_support(db_session):
    # Test updating an existing support
    support = Support.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Update the support's email
    support.update(db_session, email="john.doe.updated@example.com")

    # Check if the email was updated successfully
    updated_support = Support.read(db_session, support.id)
    assert updated_support.email == "john.doe.updated@example.com"


def test_delete_support(db_session):
    # Test deleting an existing support
    support = Support.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Delete the support
    support.delete(db_session)

    # Check if the support was deleted successfully
    deleted_support = Support.read(db_session, support.id)
    assert deleted_support is None
