from app.models import Seller


def test_create_seller(db_session):
    # Test creating a new seller
    new_seller = Seller.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Check if the seller was created successfully
    assert new_seller.id is not None
    assert new_seller.surname == "John"
    assert new_seller.lastname == "Doe"
    assert new_seller.email == "john.doe@example.com"
    assert new_seller.verify_password("secret")


def test_read_seller(db_session):
    # Test reading an existing seller from the database
    seller = Seller.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    read_seller = Seller.read(db_session, seller.id)

    # Check if the read operation returns the correct seller
    assert read_seller is not None
    assert read_seller.id == seller.id
    assert read_seller.surname == "John"
    assert read_seller.lastname == "Doe"
    assert read_seller.email == "john.doe@example.com"


def test_update_seller(db_session):
    # Test updating an existing seller
    seller = Seller.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Update the seller's email
    seller.update(db_session, email="john.doe.updated@example.com")

    # Check if the email was updated successfully
    updated_seller = Seller.read(db_session, seller.id)
    assert updated_seller.email == "john.doe.updated@example.com"


def test_delete_seller(db_session):
    # Test deleting an existing seller
    seller = Seller.create(db_session, surname="John", lastname="Doe", email="john.doe@example.com", password="secret")

    # Delete the seller
    seller.delete(db_session)

    # Check if the seller was deleted successfully
    deleted_seller = Seller.read(db_session, seller.id)
    assert deleted_seller is None
