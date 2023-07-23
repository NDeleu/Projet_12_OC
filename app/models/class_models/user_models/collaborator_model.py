from sqlalchemy import Column, Integer, String, DateTime, Enum, text
import enum
from passlib.hash import bcrypt
from app.models.database_models.database import Base
from sqlalchemy.orm import relationship


class Collaborator(Base):

    class RoleEnum(enum.Enum):
        administrator = 1
        seller = 2
        support = 3

    __tablename__ = 'collaborators'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String)
    token = Column(String)
    token_expiration = Column(DateTime)
    customers = relationship("Customer", back_populates="collaborator", cascade="all, delete")
    events = relationship("Event", back_populates="collaborator", cascade="all, delete")

    def __init__(self, firstname, lastname, email, role, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_role(role)
        self.set_password(password)

    def set_role(self, role_value):
        try:
            self.role = self.RoleEnum(role_value)
        except ValueError:
            raise ValueError("Invalid role value")

    @classmethod
    def create(cls, session, firstname, lastname, email, role, password):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM collaborators WHERE email=:email) "
                "OR EXISTS (SELECT 1 FROM customers WHERE email=:email)"),
            {"email": email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "The email address already exists for an collaborators or customer.")

        collaborator = Collaborator(firstname=firstname, lastname=lastname,
                                    email=email, role=role, password=password)
        session.add(collaborator)
        session.commit()
        return collaborator

    @classmethod
    def get_by_id(cls, session, collaborator_id):
        collaborator = session.query(Collaborator).filter_by(id=collaborator_id).first()
        return collaborator

    @classmethod
    def get_by_email(cls, session, collaborator_email):
        collaborator = session.query(Collaborator).filter_by(email=collaborator_email).first()
        return collaborator

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

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if key == 'email':
                self.set_email(session, value)
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
