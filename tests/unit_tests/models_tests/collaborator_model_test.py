from app.models import Collaborator


def test_create_collaborator(db_session):
    # Test creating a new collaborator
    new_collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    # Check if the collaborator was created successfully
    assert new_collaborator.id is not None
    assert new_collaborator.firstname == "John"
    assert new_collaborator.lastname == "Doe"
    assert new_collaborator.email == "john.doe@example.com"
    assert new_collaborator.role == Collaborator.RoleEnum.seller
    assert new_collaborator.verify_password("secret")

def test_read_collaborator(db_session):
    # Create some collaborators for testing
    collaborator1 = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=Collaborator.RoleEnum.seller, password="secret")
    collaborator2 = Collaborator.create(db_session, firstname="Jane", lastname="Smith", email="jane.smith@example.com", role=Collaborator.RoleEnum.administrator, password="password123")
    collaborator3 = Collaborator.create(db_session, firstname="Bob", lastname="Johnson", email="bob.johnson@example.com", role=Collaborator.RoleEnum.support, password="testpassword")

    # Test reading all collaborators
    all_collaborators = Collaborator.read(db_session)

    # Check if the collaborators were retrieved successfully
    assert len(all_collaborators) == 3

    # Check if all collaborators have the correct data
    assert all_collaborators[0].id == collaborator1.id
    assert all_collaborators[0].firstname == "John"
    assert all_collaborators[0].lastname == "Doe"
    assert all_collaborators[0].email == "john.doe@example.com"
    assert all_collaborators[0].role == Collaborator.RoleEnum.seller

    assert all_collaborators[1].id == collaborator2.id
    assert all_collaborators[1].firstname == "Jane"
    assert all_collaborators[1].lastname == "Smith"
    assert all_collaborators[1].email == "jane.smith@example.com"
    assert all_collaborators[1].role == Collaborator.RoleEnum.administrator

    assert all_collaborators[2].id == collaborator3.id
    assert all_collaborators[2].firstname == "Bob"
    assert all_collaborators[2].lastname == "Johnson"
    assert all_collaborators[2].email == "bob.johnson@example.com"
    assert all_collaborators[2].role == Collaborator.RoleEnum.support

def test_get_by_id_collaborator(db_session):
    # Test reading an existing collaborator from the database
    collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    read_collaborator = Collaborator.get_by_id(db_session, collaborator.id)

    # Check if the get by id operation returns the correct collaborator
    assert read_collaborator is not None
    assert read_collaborator.id == collaborator.id
    assert read_collaborator.firstname == "John"
    assert read_collaborator.lastname == "Doe"
    assert read_collaborator.email == "john.doe@example.com"
    assert read_collaborator.role == Collaborator.RoleEnum.seller


def test_get_by_email_collaborator(db_session):
    # Test reading an existing collaborator from the database
    collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    read_collaborator = Collaborator.get_by_email(db_session, collaborator.email)

    # Check if the get by email operation returns the correct collaborator
    assert read_collaborator is not None
    assert read_collaborator.id == collaborator.id
    assert read_collaborator.firstname == "John"
    assert read_collaborator.lastname == "Doe"
    assert read_collaborator.email == "john.doe@example.com"
    assert read_collaborator.role == Collaborator.RoleEnum.seller


def test_update_collaborator(db_session):
    # Test updating an existing collaborator
    collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    # Update the collaborator's email
    collaborator.update(db_session, email="john.doe.updated@example.com")

    # Check if the email was updated successfully
    updated_collaborator = Collaborator.get_by_id(db_session, collaborator.id)
    assert updated_collaborator.email == "john.doe.updated@example.com"


def test_delete_collaborator(db_session):
    # Test deleting an existing collaborator
    collaborator = Collaborator.create(db_session, firstname="John", lastname="Doe", email="john.doe@example.com", role=2, password="secret")

    # Delete the collaborator
    collaborator.delete(db_session)

    # Check if the collaborator was deleted successfully
    deleted_collaborator = Collaborator.get_by_id(db_session, collaborator.id)
    assert deleted_collaborator is None
