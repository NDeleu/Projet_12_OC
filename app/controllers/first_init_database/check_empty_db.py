from app.models import Collaborator
from app.models import session


def check_administrator_existence():
    num_collaborators = session.query(Collaborator).count()

    return num_collaborators > 0
