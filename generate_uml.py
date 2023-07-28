import os
import sys

from app.models import Base, Collaborator, Customer, Contract, Event


from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy.orm import class_mapper

def generate_erd():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, 'models.py')

    if not os.path.exists(models_dir):
        print("The models.py file does not exist.")
        sys.exit(1)

    engine = create_engine('postgresql://your_username:your_password@localhost:5432/your_database_name')

    if not database_exists(engine.url):
        print("The specified database does not exist.")
        sys.exit(1)

    Base.metadata.reflect(bind=engine)

    codegen = CodeGenerator(Base.metadata)
    code = codegen.render()

    with open('erd.py', 'w') as f:
        f.write(code)

if __name__ == '__main__':
    generate_erd()
