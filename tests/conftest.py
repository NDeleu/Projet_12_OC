import pytest
import os

from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database


@pytest.fixture(scope='session')
def postgresql():
    """Fixture for PostgreSQL database."""
    # Détails de connexion

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
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

    yield info


@pytest.fixture
def db_session(postgresql):
    """Session for SQLAlchemy."""
    from app.models import Base

    # Créez la base de données temporaire en ajoutant "_test" au nom de la base de données existante
    test_db_name = f"{postgresql['dbname']}_test"

    if postgresql['dbname'] != 'database_name':
        db_url = f"postgresql://{postgresql['user']}:{postgresql['password']}@{postgresql['host']}:{postgresql['port']}/{test_db_name}"
    else:
        raise SQLAlchemyError("Database connection error. try to connect to the application database to configure the database and retry.")

    # Vérifiez si la base de données existe et créez-la si nécessaire
    if not database_exists(db_url):
        create_database(db_url)

    # Créez un moteur SQLAlchemy et une session
    engine = create_engine(db_url, echo=False, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Copiez les tables existantes vers la base de données temporaire
    Base.metadata.create_all(engine)

    # Si vous utilisez Alembic pour la gestion des migrations, vous pouvez exécuter les migrations ici

    yield session

    session.close()
    engine.dispose()

    # Supprimez la base de données temporaire une fois les tests terminés
    if database_exists(db_url):
        drop_database(db_url)
