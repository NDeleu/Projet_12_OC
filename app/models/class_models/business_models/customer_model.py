from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import re
from app.models.database_models.database import Base


class Customer(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(length=50))
    lastname = Column(String(length=50))
    email = Column(String(length=100), unique=True)
    phone = Column(Integer)
    company = Column(String(length=100))
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    collaborator_id = Column(Integer, ForeignKey('collaborators.id'))
    collaborator = relationship("Collaborator", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer", cascade="all, delete")

    def __init__(self, firstname, lastname, email, phone, company, collaborator):
        self.set_firstname(firstname)
        self.set_lastname(lastname)
        self.set_email(email)
        self.set_phone(phone)
        self.set_company(company)
        self.collaborator = collaborator

    def set_firstname(self, firstname):
        if not firstname:
            raise ValueError("Firstname cannot be empty.")
        if not re.match("^[a-zA-Z0-9]+$", firstname):
            raise ValueError(
                "Invalid input. Please enter a valid firstname without special characters or spaces.")
        self.firstname = firstname

    def set_lastname(self, lastname):
        if not lastname:
            raise ValueError("Lastname cannot be empty.")
        if not re.match("^[a-zA-Z0-9]+$", lastname):
            raise ValueError(
                "Invalid input. Please enter a valid lastname without special characters or spaces.")
        self.lastname = lastname

    def set_email(self, email):
        if not email:
            raise ValueError("Email cannot be empty.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        self.email = email

    def set_phone(self, phone):
        if not phone:
            raise ValueError("Phone cannot be empty.")
        if not isinstance(phone, int):
            raise TypeError("Invalid input. Phone should contain only integer.")
        self.phone = phone

    def set_company(self, company):
        if not company:
            raise ValueError("Company cannot be empty.")
        if not re.match("^[a-zA-Z0-9 ]+$", company):
            raise ValueError(
                "Invalid input. Please enter a valid company without special characters.")
        self.company = company

    @classmethod
    def create(cls, session, firstname, lastname, email, phone, company,
               collaborator):
        email_exists = session.query(cls).filter(
            (cls.email == email) | (cls.collaborator.has(email=email))
        ).first()

        if email_exists:
            raise ValueError(
                "The email address already exists for a collaborator or customer.")

        is_seller = collaborator.role == collaborator.__class__.RoleEnum.seller
        if not is_seller:
            raise PermissionError(
                f"Only collaborators with the role of 'seller' can be linked to a customer.")

        customer = Customer(firstname=firstname, lastname=lastname,
                            email=email, phone=phone,
                            company=company, collaborator=collaborator)

        session.add(customer)
        session.commit()
        return customer

    @classmethod
    def read(cls, session, user_id=None):
        query = session.query(Customer)

        if user_id is not None:
            query = query.filter(Customer.collaborator_id == user_id)

        list_customers = query.distinct().all()
        return list_customers

    @classmethod
    def get_by_id(cls, session, customer_id):
        customer = session.query(Customer).filter_by(id=customer_id).first()
        return customer

    @classmethod
    def get_by_email(cls, session, customer_email):
        customer = session.query(Customer).filter_by(email=customer_email).first()
        return customer

    def update(self, session, **kwargs):
        new_email = kwargs.get('email', self.email)
        email_exists = session.query(Customer).filter(
            (Customer.email == new_email) | (
                Customer.collaborator.has(email=new_email))
        ).filter(Customer.id != self.id).first()

        if email_exists:
            raise ValueError(
                "The email address already exists for a collaborator or customer.")

        for key, value in kwargs.items():
            if value is not None:
                if key == 'email':
                    self.set_email(value)
                elif key == 'collaborator':
                    is_seller = value.role == value.__class__.RoleEnum.seller
                    if not is_seller:
                        raise PermissionError(
                            f"Only collaborators with the role of 'seller' can be linked to a customer.")

                    self.collaborator = value
                else:
                    setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
