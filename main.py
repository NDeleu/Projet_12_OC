import app.models
from app.controllers.first_init_database.check_empty_db import check_administrator_existence
from app.controllers.first_init_database.create_first_admin import create_first_administrator
from app.controllers.cli_controller import cli


if __name__ == '__main__':
    session = app.models.session

    if check_administrator_existence():
        cli(obj=session)

    else:
        create_first_administrator()
        cli(obj=session)
