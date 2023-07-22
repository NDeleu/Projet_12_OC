from .class_models.user_models.administrator_models import Administrator
from .class_models.user_models.seller_models import Seller
from .class_models.user_models.support_models import Support
from .class_models.business_models.customer_models import Customer
from .class_models.business_models.contract_models import Contract
from .class_models.business_models.event_models import Event

from .database_models.database import engine, session, Base
from .database_models.set_secret_jwt import set_jwt_secret


Base.metadata.create_all(engine)
set_jwt_secret()
