from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database_models.database import Base


class Customer(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    phone = Column(Integer)
    company = Column(String)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    collaborator_id = Column(Integer, ForeignKey('collaborators.id'))
    collaborator = relationship("Collaborator", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer", cascade="all, delete")

    def __init__(self, surname, lastname, email, phone, company, collaborator):
        self.surname = surname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.company = company
        self.collaborator = collaborator

    @classmethod
    def create(cls, session, surname, lastname, email, phone, company,
               collaborator):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM collaborators WHERE email=:email) "
                "OR EXISTS (SELECT 1 FROM customers WHERE email=:email)"),
            {"email": email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "The email address already exists for a collaborator or customer.")

        is_seller = session.execute(
            text(
                "SELECT 1 FROM collaborators WHERE id=:collaborator_id AND role=:role"
            ),
            {"collaborator_id": collaborator.id, "role": "seller"}
        ).scalar()

        if not is_seller:
            raise ValueError(
                "Only collaborators with the role of 'seller' can be linked to a customer.")

        customer = Customer(surname=surname, lastname=lastname,
                            email=email, phone=phone,
                            company=company, collaborator=collaborator)
        session.add(customer)
        session.commit()
        return customer

    @classmethod
    def read(cls, session, customer_id):
        customer = session.query(Customer).filter_by(id=customer_id).first()
        return customer

    def set_email(self, session, new_email):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM collaborators WHERE email=:new_email) "
                "OR EXISTS (SELECT 1 FROM customers WHERE email=:new_email)"),
            {"new_email": new_email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "The email address already exists for an collaborators or customer.")

        self.email = new_email

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if key == 'email':
                self.set_email(session, value)
            elif key == 'collaborator':
                is_seller = session.execute(
                    text(
                        "SELECT 1 FROM collaborators WHERE id=:collaborator_id AND role=:role"
                    ),
                    {"collaborator_id": value.id, "role": "seller"}
                ).scalar()

                if not is_seller:
                    raise ValueError("Only collaborators with the role of 'seller' can be linked to a customer.")

                self.collaborator = value
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.surname} {self.lastname}'
