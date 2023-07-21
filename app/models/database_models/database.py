import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser
from sqlalchemy_utils import create_database, database_exists

from app.views.general_views.generic_message import display_message


def sql_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(models_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    username = config.get('sql', 'username')
    password = config.get('sql', 'password')
    database_name = config.get('sql', 'database_name')

    info = {
        'user': f'{username}',
        'password': f'{password}',
        'host': 'localhost',
        'port': 5432,
        'dbname': f'{database_name}',
    }

    return info


def db_session(sql_database_info):

    Base = declarative_base()

    if sql_database_info['database_name'] != "database_name":
        db_url = f"postgresql://{sql_database_info['username']}:{sql_database_info['password']}@{sql_database_info['host']}:{sql_database_info['port']}/{sql_database_info['database_name']}"
    else:
        display_message(
            "Database not found. Please check your configuration and retry.")
        sys.exit(1)

    # Vérifiez si la base de données existe et créez-la si nécessaire
    if not database_exists(db_url):
        create_database(db_url)

    # Créez un moteur SQLAlchemy et une session
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session, Base, engine


session, Base, engine = db_session(sql_database())