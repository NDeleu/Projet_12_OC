import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import jwt
import enum
from configparser import ConfigParser
from app.controllers.auth_controllers.permission_controller import (
    generate_token,
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


def fonction_fictive(session, user, *args, **kwargs):
    if user.role != CollaboratorMock.RoleEnum.administrator:
        return None
    return "Fonction fictive appelée"


def test_login_required_admin():
    # Collaborator fictif avec le rôle "administrateur"
    user = CollaboratorMock(1, CollaboratorMock.RoleEnum.administrator)

    # Session fictive
    session = MagicMock()

    # Appliquer le décorateur à la fonction fictive
    fonction_decoree = login_required_admin(fonction_fictive)

    # Appeler la fonction décorée avec le bon rôle utilisateur
    resultat = fonction_decoree(session, user)

    # Vérifier que la fonction fictive est appelée et renvoie la valeur attendue
    assert resultat == "Fonction fictive appelée"

    # Collaborator fictif avec le rôle "vendeur"
    user = CollaboratorMock(2, CollaboratorMock.RoleEnum.seller)

    # Utiliser @patch pour remplacer display_message_error par un mock
    with patch("app.views.general_views.generic_message.display_message_error") as mock_display_message_error:
        # Appeler la fonction décorée avec le mauvais rôle utilisateur
        resultat = fonction_decoree(session, user)

        # Vérifier que la fonction display_message_error a été appelée avec le message approprié
        mock_display_message_error.assert_called_once_with(
            "Permission denied. Please log in as an administrator."
        )
