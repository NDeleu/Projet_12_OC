import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import functools
import jwt
import enum
from configparser import ConfigParser
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import (
    generate_token,
    get_logged_as_user,
    save_token_to_file,
    get_token_from_file,
    clear_token_from_file,
    login_required_admin,
    login_required_seller,
    login_required_support,
    login_required_admin_or_seller,
    login_required_admin_or_support,
    login_required
)

script_dir = os.path.dirname(os.path.abspath(__file__))
controllers_dir = os.path.dirname(script_dir)
unit_tests_dir = os.path.dirname(controllers_dir)
tests_dir = os.path.dirname(unit_tests_dir)
root_dir = os.path.dirname(tests_dir)
config_file = os.path.join(root_dir, 'config.ini')

config = ConfigParser()
config.read(config_file)

SECRET_KEY = config.get('jwt', 'secret_key_jwt')


# Mock de la classe Collaborator pour les tests
class CollaboratorMock:

    class RoleEnum(enum.Enum):
        administrator = 1
        seller = 2
        support = 3

        def __json__(self):
            return self.value

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = self.RoleEnum(role)


@pytest.mark.parametrize("user_id, role", [(1, CollaboratorMock.RoleEnum.administrator), (2, CollaboratorMock.RoleEnum.seller), (3, CollaboratorMock.RoleEnum.support)])
def test_generate_token(user_id, role):
    # Appeler la fonction et générer le token
    token = generate_token(user_id, role)

    # Vérifier que le token n'est pas vide
    assert token is not None

    # Décoder le token pour obtenir la charge utile (payload)
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    # Vérifier que la charge utile contient le bon user_id et role
    assert decoded_payload.get("user_id") == user_id
    assert decoded_payload.get("role") == role.value

    # Vérifier que le temps d'expiration du token est dans les 10 prochaines minutes
    expiration_time = datetime.utcfromtimestamp(decoded_payload.get("exp"))
    assert expiration_time >= datetime.utcnow()
    assert expiration_time <= datetime.utcnow() + timedelta(minutes=10)


def test_get_token_from_file_success():
    # Token d'exemple pour les tests
    token = "example_token"

    # Sauvegarder le token dans le fichier
    with open("token.txt", "w") as file:
        file.write(token)

    # Appeler la fonction get_token_from_file pour récupérer le token
    read_token = get_token_from_file()

    # Vérifier que le token lu correspond au token original
    assert read_token == token

    # Nettoyage en supprimant le fichier
    os.remove("token.txt")

def test_get_token_from_file_file_not_found():
    # Token d'exemple pour les tests
    token = "example_token"

    # Sauvegarder le token dans le fichier
    with open("token.txt", "w") as file:
        file.write(token)

    # Nettoyage en supprimant le fichier
    os.remove("token.txt")

    # Appeler la fonction get_token_from_file lorsque le fichier n'existe pas
    read_token = get_token_from_file()

    # Vérifier que le token renvoyé est None lorsque le fichier n'existe pas
    assert read_token is None


def test_save_and_get_token():
    # Token d'exemple pour les tests
    token = "token_d_exemple"

    # Sauvegarder le token dans le fichier
    save_token_to_file(token)

    # Lire le token depuis le fichier
    read_token = get_token_from_file()

    # Vérifier que le token lu correspond au token original
    assert read_token == token

    # Nettoyage en supprimant le fichier
    os.remove("token.txt")


def test_clear_token():
    # Token d'exemple pour les tests
    token = "token_d_exemple"

    # Sauvegarder le token dans le fichier
    save_token_to_file(token)

    # Effacer le token du fichier
    clear_token_from_file()

    # Lire le token depuis le fichier
    read_token = get_token_from_file()

    # Vérifier que le token lu est None après l'effacement
    assert read_token == ''


def test_get_logged_as_user():
    # Token d'exemple pour les tests
    token = "example_token"

    # Collaborator fictif avec l'ID "user_id"
    user_id = 1
    user = CollaboratorMock(user_id, CollaboratorMock.RoleEnum.administrator)

    # Session fictive
    session = MagicMock()

    # Définir une fonction de simulation pour jwt.decode
    # Cette fonction renverra le payload avec l'ID de l'utilisateur correspondant au token d'exemple
    def mock_jwt_decode(token, secret_key, algorithms):
        return {"user_id": user_id}

    # Définir une fonction de simulation pour Collaborator.get_by_id
    # Cette fonction renverra l'utilisateur fictif avec l'ID spécifié
    def mock_get_by_id(session, user_id):
        return user

    # Utiliser patch pour remplacer jwt.decode par la fonction de simulation
    with patch("app.controllers.auth_controllers.permission_controller.jwt.decode", mock_jwt_decode):
        # Utiliser patch pour remplacer Collaborator.get_by_id par la fonction de simulation
        with patch("app.controllers.auth_controllers.permission_controller.Collaborator.get_by_id", mock_get_by_id):
            # Sauvegarder le token dans le fichier
            with open("token.txt", "w") as file:
                file.write(token)

            # Appeler la fonction get_logged_as_user pour récupérer l'utilisateur
            logged_user = get_logged_as_user(session)

            # Vérifier que l'utilisateur renvoyé correspond à l'utilisateur fictif
            assert logged_user.user_id == user_id

            # Nettoyage en supprimant le fichier
            os.remove("token.txt")


def test_get_logged_as_user_expired_token():
    # Token d'exemple pour les tests
    token = "expired_token"

    # Session fictive
    session = MagicMock()

    # Définir une fonction de simulation pour jwt.decode
    # Cette fonction lèvera jwt.ExpiredSignatureError
    def mock_jwt_decode(token, secret_key, algorithms):
        raise jwt.ExpiredSignatureError("Token has expired")

    # Utiliser patch pour remplacer jwt.decode par la fonction de simulation
    with patch("app.controllers.auth_controllers.permission_controller.jwt.decode", mock_jwt_decode):
        # Sauvegarder le token dans le fichier
        with open("token.txt", "w") as file:
            file.write(token)

        # Appeler la fonction get_logged_as_user pour récupérer l'utilisateur
        logged_user = get_logged_as_user(session)

        # Vérifier que l'utilisateur renvoyé est None après l'expiration du token
        assert logged_user is None

        # Nettoyage en supprimant le fichier
        os.remove("token.txt")


# Mock the get_logged_as_user function to return a user with the specified role
def mock_get_logged_as_user(session, role):
    class UserMock:
        def __init__(self, user_id, user_role):
            self.user_id = user_id
            self.role = user_role

    if role is None:
        return None
    else:
        return UserMock(1, role)


def test_login_required_admin():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required_admin(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.administrator)):
        decorated_function = login_required_admin(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."


def test_login_required_seller():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required_seller(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.seller)):
        decorated_function = login_required_seller(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."


def test_login_required_support():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required_support(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.support)):
        decorated_function = login_required_support(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."


def test_login_required_admin_or_seller():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required_admin_or_seller(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.administrator)):
        decorated_function = login_required_admin_or_seller(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.seller)):
        decorated_function = login_required_admin_or_seller(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."


def test_login_required_admin_or_support():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required_admin_or_support(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.administrator)):
        decorated_function = login_required_admin_or_support(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role=Collaborator.RoleEnum.support)):
        decorated_function = login_required_admin_or_support(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."


def test_login_required():
    session = MagicMock()

    def test_function(session, user):
        return "Test function executed successfully."

    with pytest.raises(PermissionError):
        with patch(
                "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
                functools.partial(mock_get_logged_as_user, role=None)):
            decorated_function = login_required(test_function)
            decorated_function(session)

    with patch(
            "app.controllers.auth_controllers.permission_controller.get_logged_as_user",
            functools.partial(mock_get_logged_as_user, role="any_role")):
        decorated_function = login_required(test_function)
        result = decorated_function(session)
        assert result == "Test function executed successfully."