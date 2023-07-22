from app.controllers.first_init_database.check_empty_db import check_administrator_existence
from app.controllers.first_init_database.create_first_admin import create_first_administrator


if __name__ == '__main__':
    if check_administrator_existence():
        import app.models
        print("already 1 admin")
    else:
        create_first_administrator()
        import app.models
        print("no admin")
