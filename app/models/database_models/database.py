import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from configparser import ConfigParser
from sqlalchemy_utils import create_database, database_exists

from .set_url_database import set_url_config

from app.views.general_views.generic_message import display_message


def sql_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.dirname(script_dir)
    app_dir = os.path.dirname(models_dir)
    root_dir = os.path.dirname(app_dir)
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


def set_url_db():
    while True:
        sql_database_info = sql_database()
        if sql_database_info['dbname'] != 'database_name':
            db_url = f"postgresql://{sql_database_info['user']}:{sql_database_info['password']}@{sql_database_info['host']}:{sql_database_info['port']}/{sql_database_info['dbname']}"
            break
        else:
            display_message("Your database configuration is default, you need to change your set up.")
            if set_url_config():
                display_message("Successful database configuration change.")
            else:
                raise SQLAlchemyError("Error Database initialization. Try to fix it and retry later.")
    return db_url


def try_connect_bdd(engine):
    try:
        conn = engine.connect()
        conn.close()
        return True
    except SQLAlchemyError:
        return False


def db_engine():

    while True:
        db_url = set_url_db()

        if not database_exists(db_url):
            create_database(db_url)
            display_message("Database created")

        engine = create_engine(db_url)

        if try_connect_bdd(engine):
            break
        else:
            display_message("The configuration did not allow to connect to the database, you need to change your set up.")
            if set_url_config():
                display_message("Successful database configuration change.")
            else:
                raise SQLAlchemyError("Error Database initialization. Try to fix it and retry later.")

    return engine


def db_session(engine):

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def db_base():

    Base = declarative_base()

    return Base


engine = db_engine()
session = db_session(engine)
Base = db_base()
