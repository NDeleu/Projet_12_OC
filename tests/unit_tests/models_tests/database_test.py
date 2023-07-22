import os
from configparser import ConfigParser
from sqlalchemy import create_engine, text


def test_database_connection(db_session):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    unit_test_dir = os.path.dirname(script_dir)
    tests_dir = os.path.dirname(unit_test_dir)
    root_dir = os.path.dirname(tests_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    database_name = config.get('sql', 'database_name')

    # Vérifiez si la connexion à la base de données fonctionne

    # Exemple de requête pour vérifier si la connexion est réussie
    result = db_session.execute(text("SELECT 1"))

    # Vérifiez si la requête a renvoyé le résultat attendu
    assert result.scalar() == 1

    # Vérifier le nom de la base de données
    db_name_query = db_session.execute(text("SELECT current_database()"))
    db_name = db_name_query.scalar()

    # Mettez ici le nom de la base de données de test attendu (avec le suffixe "_test")
    expected_test_db_name = f"{database_name}_test"

    # Vérifiez si le nom de la base de données correspond à celui de la base de données de test attendue
    assert db_name == expected_test_db_name

    # Vous pouvez également effectuer d'autres vérifications, par exemple,
    # vérifier si une table spécifique existe ou si vous pouvez insérer et récupérer des données.

    # Exemple de vérification si une table spécifique existe
    table_exists = db_session.connection().execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='collaborators')")).scalar()

    # Vérifiez si la table existe
    assert table_exists

