from .class_models.user_models.collaborator_model import Collaborator
from .class_models.business_models.customer_model import Customer
from .class_models.business_models.contract_model import Contract
from .class_models.business_models.event_model import Event

from .database_models.database import engine, session, Base
from .database_models.set_secret_jwt import set_jwt_secret

import graphviz

Base.metadata.create_all(engine)
set_jwt_secret()


def create_uml_graph(classes):
    graph = graphviz.Digraph(format='png')

    # Composants UML
    with graph.subgraph(name='cluster_UML') as cluster_uml:
        cluster_uml.attr(label='Diagramme UML')
        for cls in classes:
            class_name = cls.__name__
            label = f'{{ {class_name} |'
            for column in cls.__table__.columns:
                label += f' {column.name} : {column.type} |'
            label += ' }'
            cluster_uml.node(class_name, shape='record', label=label)

    # Composants ERD
    with graph.subgraph(name='cluster_ERD') as cluster_erd:
        cluster_erd.attr(label='Diagramme Entité-Relation')

        # Collaborator -> Customer (One-to-Many)
        cluster_erd.edge('Collaborator', 'Customer', label='1..*', arrowhead='crow')

        # Collaborator -> Event (One-to-Many)
        cluster_erd.edge('Collaborator', 'Event', label='1..*', arrowhead='crow')

        # Event -> Contract (One-to-One)
        cluster_erd.edge('Event', 'Contract', label='1', arrowhead='none')

        # Customer -> Contract (One-to-Many)
        cluster_erd.edge('Customer', 'Contract', label='1..*', arrowhead='crow')

    return graph


def generate_uml_graph():
    graph = create_uml_graph([Collaborator, Customer, Contract, Event])
    graph.render('uml_diagram', view=True)

