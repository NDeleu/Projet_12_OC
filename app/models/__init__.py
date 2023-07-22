from .class_models.user_models.collaborator_model import Collaborator
from .class_models.business_models.customer_model import Customer
from .class_models.business_models.contract_model import Contract
from .class_models.business_models.event_model import Event

from .database_models.database import engine, session, Base
from .database_models.set_secret_jwt import set_jwt_secret


Base.metadata.create_all(engine)
set_jwt_secret()
