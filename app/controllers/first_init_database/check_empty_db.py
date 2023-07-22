from app.models import Administrator
from app.models import session


def check_administrator_existence():
    num_administrators = session.query(Administrator).count()

    return num_administrators > 0
