from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
import re
from passlib.hash import bcrypt
from app.models.database_models.database import Base
from sqlalchemy.orm import relationship


class Collaborator(Base):

    class RoleEnum(enum.Enum):
        administrator = 1
        seller = 2
        support = 3

        def __json__(self):
            return self.value

    __tablename__ = 'collaborators'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(length=50))
    lastname = Column(String(length=50))
    email = Column(String(length=50), unique=True)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String(length=60)) # The hashed password will always be 60 characters
    token = Column(String)
    token_expiration = Column(DateTime)
    customers = relationship("Customer", back_populates="collaborator", cascade="all, delete")
    events = relationship("Event", back_populates="collaborator", cascade="all, delete")

    def __init__(self, firstname, lastname, email, role, password):
        self.set_firstname(firstname)
        self.set_lastname(lastname)
        self.set_email(email)
        self.set_role(role)
        self.set_password(password)

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

    def set_role(self, role_value):
        try:
            self.role = self.RoleEnum(role_value)
        except ValueError:
            raise ValueError("Invalid role value")

    def set_password(self, password):
        if not password:
            raise ValueError("Invalid input. Password cannot be empty.")
        if not password.strip():
            raise ValueError("Invalid input. Password cannot be empty.")
        if not re.match("^[a-zA-Z0-9!@#$%^&*()_-]+$", password):
            raise ValueError("Invalid input. Please enter a non-empty password containing only letters, numbers, and a limited set of special characters (!@#$%^&*()_-).")
        self.password = bcrypt.hash(password)

    @classmethod
    def create(cls, session, firstname, lastname, email, role, password):
        email_exists = session.query(cls).filter(
            (cls.email == email) | (cls.customers.any(email=email))
        ).first()

        if email_exists:
            raise ValueError(
                "The email address already exists for a collaborator or customer.")

        collaborator = Collaborator(firstname=firstname, lastname=lastname,
                                    email=email, role=role, password=password)
        session.add(collaborator)
        session.commit()
        return collaborator

    @classmethod
    def read(cls, session):
        list_collaborators = session.query(Collaborator).all()
        return list_collaborators

    @classmethod
    def get_by_id(cls, session, collaborator_id):
        collaborator = session.query(Collaborator).filter_by(id=collaborator_id).first()
        return collaborator

    @classmethod
    def get_by_email(cls, session, collaborator_email):
        collaborator = session.query(Collaborator).filter_by(email=collaborator_email).first()
        return collaborator

    def update(self, session, **kwargs):
        new_email = kwargs.get('email', self.email)
        email_exists = session.query(Collaborator).filter(
            (Collaborator.email == new_email) | (
                Collaborator.customers.any(email=new_email))
        ).filter(Collaborator.id != self.id).first()

        if email_exists:
            raise ValueError(
                "The email address already exists for a collaborator or customer.")

        for key, value in kwargs.items():
            if value is not None:
                if key == 'email':
                    self.set_email(value)
                elif key == 'password':
                    self.set_password(value)
                elif key == 'role':
                    raise ValueError("Role cannot be updated.")
                else:
                    setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.role}'
